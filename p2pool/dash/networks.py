import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(dashd, genesis_block_hash):
    try:
        yield dashd.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    dash=math.Object(
        P2P_PREFIX='bf0c6bbd'.decode('hex'),
        P2P_PORT=9999,
        ADDRESS_VERSION=76,
        SCRIPT_ADDRESS_VERSION=16,
        RPC_PORT=9998,
        RPC_CHECK=defer.inlineCallbacks(lambda dashd: defer.returnValue(
            'dashaddress' in (yield dashd.rpc_help()) and
            not (yield dashd.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda nBits, height: __import__('darkcoin_subsidy').GetBlockBaseValue(nBits, height),
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('darkcoin_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('darkcoin_hash').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='DASH',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Dash') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Dash/') if platform.system() == 'Darwin' else os.path.expanduser('~/.dash'), 'dash.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.dashninja.pl/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.dashninja.pl/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.dashninja.pl/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),
    dash_testnet=math.Object(
        P2P_PREFIX='cee2caff'.decode('hex'),
        P2P_PORT=19999,
        ADDRESS_VERSION=139,
        SCRIPT_ADDRESS_VERSION=19,
        RPC_PORT=19998,
        RPC_CHECK=defer.inlineCallbacks(lambda dashd: defer.returnValue(
            'dashaddress' in (yield dashd.rpc_help()) and
            (yield dashd.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda nBits, height: __import__('darkcoin_subsidy').GetBlockBaseValue_testnet(nBits, height),
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('darkcoin_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('darkcoin_hash').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='tDASH',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Dash') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Dash/') if platform.system() == 'Darwin' else os.path.expanduser('~/.dash'), 'dash.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://test.explorer.dashninja.pl/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://test.explorer.dashninja.pl/address/',
        TX_EXPLORER_URL_PREFIX='http://test.explorer.dashninja.pl/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
