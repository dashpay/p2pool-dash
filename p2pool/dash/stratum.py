import random
import sys

from twisted.internet import protocol, reactor
from twisted.python import log

from p2pool.dash import data as dash_data, getwork
from p2pool.util import expiring_dict, jsonrpc, pack


class StratumRPCMiningProvider(object):
    def __init__(self, wb, other, transport):
        self.wb = wb
        self.other = other
        self.transport = transport
        
        self.username = None
        self.handler_map = expiring_dict.ExpiringDict(300)
        
        self.watch_id = self.wb.new_work_event.watch(self._send_work)
    
    def rpc_subscribe(self, miner_version=None, session_id=None):
        reactor.callLater(0, self._send_work)
        
        return [
            ["mining.notify", "ae6812eb4cd7735a302a8a9dd95cf71f"], # subscription details
            "", # extranonce1
            self.wb.COINBASE_NONCE_LENGTH, # extranonce2_size
        ]
    
    def rpc_authorize(self, username, password):
        self.username = username
        
        reactor.callLater(0, self._send_work)
        return True
    
    def _send_work(self):
        try:
            x, got_response = self.wb.get_work(*self.wb.preprocess_request('' if self.username is None else self.username))
        except:
            log.err()
            self.transport.loseConnection()
            return
        jobid = str(random.randrange(2**128))
        self.other.svc_mining.rpc_set_difficulty(dash_data.target_to_difficulty(x['share_target'])).addErrback(lambda err: None)
        self.other.svc_mining.rpc_notify(
            jobid, # jobid
            getwork._swap4(pack.IntType(256).pack(x['previous_block'])).encode('hex'), # prevhash
            x['coinb1'].encode('hex'), # coinb1
            x['coinb2'].encode('hex'), # coinb2
            [pack.IntType(256).pack(s).encode('hex') for s in x['merkle_link']['branch']], # merkle_branch
            getwork._swap4(pack.IntType(32).pack(x['version'])).encode('hex'), # version
            getwork._swap4(pack.IntType(32).pack(x['bits'].bits)).encode('hex'), # nbits
            getwork._swap4(pack.IntType(32).pack(x['timestamp'])).encode('hex'), # ntime
            True, # clean_jobs
        ).addErrback(lambda err: None)
        self.handler_map[jobid] = x, got_response
    
    def rpc_submit(self, worker_name, job_id, extranonce2, ntime, nonce):
        if job_id not in self.handler_map:
            print >>sys.stderr, '''Couldn't link returned work's job id with its handler. This should only happen if this process was recently restarted!'''
            return False
        x, got_response = self.handler_map[job_id]
        coinb_nonce = extranonce2.decode('hex')
        assert len(coinb_nonce) == self.wb.COINBASE_NONCE_LENGTH
        new_packed_gentx = x['coinb1'] + coinb_nonce + x['coinb2']
        header = dict(
            version=x['version'],
            previous_block=x['previous_block'],
            merkle_root=dash_data.check_merkle_link(dash_data.hash256(new_packed_gentx), x['merkle_link']),
            timestamp=pack.IntType(32).unpack(getwork._swap4(ntime.decode('hex'))),
            bits=x['bits'],
            nonce=pack.IntType(32).unpack(getwork._swap4(nonce.decode('hex'))),
        )
        res = got_response(header, worker_name, coinb_nonce)

        # Disconnect miners with large DOA rates to prevent DoS
        if len(self.wb._inner.my_share_hashes) > 20:
            if float(len(self.wb._inner.my_doa_share_hashes)) / float(len(self.wb._inner.my_share_hashes)) > 0.60:
                self.transport.loseConnection()

        # Disconnect miners with large hash > target to prevent DoS
        if self.wb._inner.total_hashes > 20:
            if float(self.wb._inner.invalid_hashes) / float(self.wb._inner.total_hashes) > 0.05:
                self.transport.loseConnection()

        return res

    def close(self):
        self.wb.new_work_event.unwatch(self.watch_id)

class StratumProtocol(jsonrpc.LineBasedPeer):
    def connectionMade(self):
        self.svc_mining = StratumRPCMiningProvider(self.factory.wb, self.other, self.transport)
    
    def connectionLost(self, reason):
        self.svc_mining.close()

class StratumServerFactory(protocol.ServerFactory):
    protocol = StratumProtocol
    
    def __init__(self, wb):
        self.wb = wb
