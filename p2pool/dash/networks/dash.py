import os
import platform

from twisted.internet import defer

from .. import data, helper
from p2pool.util import pack


P2P_PREFIX = 'bf0c6bbd'.decode('hex')
P2P_PORT = 9999
ADDRESS_VERSION = 76
SCRIPT_ADDRESS_VERSION = 16
RPC_PORT = 9998
RPC_CHECK = defer.inlineCallbacks(lambda dashd: defer.returnValue(
            (yield helper.check_block_header(dashd, '00000ffd590b1485b3caadc19b22e6379c733355108f107a430458cdf3407ab6')) and
            (yield dashd.rpc_getblockchaininfo())['chain'] == 'main'
        ))
BLOCKHASH_FUNC = lambda data: pack.IntType(256).unpack(__import__('dash_hash').getPoWHash(data))
POW_FUNC = lambda data: pack.IntType(256).unpack(__import__('dash_hash').getPoWHash(data))
BLOCK_PERIOD = 150 # s
SYMBOL = 'DASH'
CONF_FILE_FUNC = lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'DashCore') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/DashCore/') if platform.system() == 'Darwin' else os.path.expanduser('~/.dashcore'), 'dash.conf')
BLOCK_EXPLORER_URL_PREFIX = 'https://chainz.cryptoid.info/dash/block.dws?'
ADDRESS_EXPLORER_URL_PREFIX = 'https://chainz.cryptoid.info/dash/address.dws?'
TX_EXPLORER_URL_PREFIX = 'https://chainz.cryptoid.info/dash/tx.dws?'
SANE_TARGET_RANGE = (2**256//2**32//1000000 - 1, 2**256//2**32 - 1)
DUST_THRESHOLD = 0.001e8
