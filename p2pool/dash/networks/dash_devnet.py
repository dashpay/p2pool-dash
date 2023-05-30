import os
import platform

from twisted.internet import defer

from .. import data, helper
from p2pool.util import pack


P2P_PREFIX = 'e2caffce'.decode('hex')
P2P_PORT = 19799
ADDRESS_VERSION = 140
SCRIPT_ADDRESS_VERSION = 19
RPC_PORT = 19798
RPC_CHECK = defer.inlineCallbacks(lambda dashd: defer.returnValue(
            (yield helper.check_block_header(dashd, '000008ca1832a4baf228eb1553c03d3a2c8e02399550dd6ea8d65cec3ef23d2e')) and
            (yield dashd.rpc_getblockchaininfo())['chain'] == 'devnet'
        ))
BLOCKHASH_FUNC = lambda data: pack.IntType(256).unpack(__import__('dash_hash').getPoWHash(data))
POW_FUNC = lambda data: pack.IntType(256).unpack(__import__('dash_hash').getPoWHash(data))
BLOCK_PERIOD = 150 # s
SYMBOL = 'tDASH'
CONF_FILE_FUNC = lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'DashCore') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/DashCore/') if platform.system() == 'Darwin' else os.path.expanduser('~/.dashcore'), 'dash.conf')
BLOCK_EXPLORER_URL_PREFIX = 'https://dev.explorer.dash.org/block/' # TODO
ADDRESS_EXPLORER_URL_PREFIX = 'https://dev.explorer.dash.org/address/' # TODO
TX_EXPLORER_URL_PREFIX = 'https://dev.explorer.dash.org/tx/' # TODO
SANE_TARGET_RANGE = (2**256//2**32//1000000 - 1, 2**256//2**20 - 1)
DUST_THRESHOLD = 0.001e8
