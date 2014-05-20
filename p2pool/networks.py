from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    darkcoin=math.Object(
        PARENT=networks.nets['darkcoin'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//15, # shares
        REAL_CHAIN_LENGTH=24*60*60//15, # shares
        TARGET_LOOKBEHIND=200, # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
        SPREAD=30, # blocks
        IDENTIFIER='f81032cd6f17bd47'.decode('hex'),
        PREFIX='3ac7ea90238a321f'.decode('hex'),
        P2P_PORT=8999,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=8998,
        BOOTSTRAP_ADDRS='drk.altmine.net'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-drk',
        VERSION_CHECK=lambda v: True,
    ),
    darkcoin_testnet=math.Object(
        PARENT=networks.nets['darkcoin_testnet'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//15, # shares
        REAL_CHAIN_LENGTH=24*60*60//15, # shares
        TARGET_LOOKBEHIND=200, # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
        SPREAD=30, # blocks
        IDENTIFIER='9cc6a1cf283d3a88'.decode('hex'),
        PREFIX='c72ce3e2878eb6ae'.decode('hex'),
        P2P_PORT=18999,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=18998,
        BOOTSTRAP_ADDRS=''.split(' '),
        ANNOUNCE_CHANNEL='',
        VERSION_CHECK=lambda v: True,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
