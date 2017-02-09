from p2pool.dash import networks

PARENT = networks.nets['dash']
SHARE_PERIOD = 20 # seconds
CHAIN_LENGTH = 24*60*60//20 # shares
REAL_CHAIN_LENGTH = 24*60*60//20 # shares
TARGET_LOOKBEHIND = 100 # shares  //with that the pools share diff is adjusting faster, important if huge hashing power comes to the pool
SPREAD = 10 # blocks
IDENTIFIER = '7242ef345e1bed6b'.decode('hex')
PREFIX = '3b3e1286f446b891'.decode('hex')
COINBASEEXT = '0D2F5032506F6F6C2D444153482F'.decode('hex')
P2P_PORT = 8999
MIN_TARGET = 0
MAX_TARGET = 2**256//2**20 - 1
PERSIST = True
WORKER_PORT = 7903
BOOTSTRAP_ADDRS = 'dash01.p2poolmining.us p2pool.2sar.ru dash02.p2poolmining.us p2pool.dash.siampm.com dash03.p2poolmining.us crypto.office-on-the.net dash04.p2poolmining.us'.split(' ')
ANNOUNCE_CHANNEL = '#p2pool-dash'
VERSION_CHECK = lambda v: v >= 120100
