import x11_hash
from binascii import unhexlify, hexlify

import unittest

# dash block #1
# moo@b1:~/.dash$ dashd getblockhash 1
# 000007d91d1254d60e2dd1ae580383070a4ddffa4c64c2eeb4a2f9ecc0414343
# moo@b1:~/.dash$ dashd getblock 000007d91d1254d60e2dd1ae580383070a4ddffa4c64c2eeb4a2f9ecc0414343
# {
#     "hash" : "000007d91d1254d60e2dd1ae580383070a4ddffa4c64c2eeb4a2f9ecc0414343",
#     "confirmations" : 169888,
#     "size" : 186,
#     "height" : 1,
#     "version" : 2,
#     "merkleroot" : "ef3ee42b51e2a19c4820ef182844a36db1201c61eb0dec5b42f84be4ad1a1ca7",
#     "tx" : [
#         "ef3ee42b51e2a19c4820ef182844a36db1201c61eb0dec5b42f84be4ad1a1ca7"
#     ],
#     "time" : 1390103681,
#     "nonce" : 128987,
#     "bits" : "1e0ffff0",
#     "difficulty" : 0.00024414,
#     "previousblockhash" : "00000ffd590b1485b3caadc19b22e6379c733355108f107a430458cdf3407ab6",
#     "nextblockhash" : "00000bafcc571ece7c5c436f887547ef41b574e10ef7cc6937873a74ef1efeae"
# }

header_hex = ("02000000" +
    "b67a40f3cd5804437a108f105533739c37e6229bc1adcab385140b59fd0f0000" +
    "a71c1aade44bf8425bec0deb611c20b16da3442818ef20489ca1e2512be43eef"
    "814cdb52" +
    "f0ff0f1e" +
    "dbf70100")

best_hash = '434341c0ecf9a2b4eec2644cfadf4d0a07830358aed12d0ed654121dd9070000'

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.block_header = unhexlify(header_hex)
        self.best_hash = best_hash

    def test_x11_hash(self):
        self.pow_hash = hexlify(x11_hash.getPoWHash(self.block_header))
        self.assertEqual(self.pow_hash, self.best_hash)


if __name__ == '__main__':
    unittest.main()

