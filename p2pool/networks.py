from p2pool.dash import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    dash=math.Object(
        PARENT=networks.nets['dash'],
        SHARE_PERIOD=20, # seconds
        CHAIN_LENGTH=24*60*60//20, # shares
        REAL_CHAIN_LENGTH=24*60*60//20, # shares
        TARGET_LOOKBEHIND=100, # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
        SPREAD=10, # blocks
        IDENTIFIER='7242ef345e1bed6b'.decode('hex'),
        PREFIX='3b3e1286f446b891'.decode('hex'),
        COINBASEEXT='0D2F5032506F6F6C2D444153482F'.decode('hex'),
        P2P_PORT=8999,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=True,
        WORKER_PORT=7903,
        BOOTSTRAP_ADDRS='p2pool.dashninja.pl dash.p2pools.us eu.p2pool.pl dash01.p2poolmining.us p2pool.2sar.ru mining.asia'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-dash',
        VERSION_CHECK=lambda v: v >= 110217,
    ),
    dash_testnet=math.Object(
        PARENT=networks.nets['dash_testnet'],
        SHARE_PERIOD=20, # seconds
        CHAIN_LENGTH=24*60*60//20, # shares
        REAL_CHAIN_LENGTH=24*60*60//20, # shares
        TARGET_LOOKBEHIND=100, # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
        SPREAD=10, # blocks
        IDENTIFIER='b6deb1e543fe2427'.decode('hex'),
        PREFIX='198b644f6821e3b3'.decode('hex'),
        COINBASEEXT='0E2F5032506F6F6C2D74444153482F'.decode('hex'),
        P2P_PORT=18999,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=17903,
        BOOTSTRAP_ADDRS='p2pool.dashninja.pl test.p2pool.masternode.io test.p2pool.dash.siampm.com'.split(' '),
        ANNOUNCE_CHANNEL='',
        VERSION_CHECK=lambda v: True,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
