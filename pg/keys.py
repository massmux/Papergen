
import hashlib

import base58
import bech32
import coincurve
import qrcode

from ripemd.ripemd160 import ripemd160

import pg.wordslist as wordslist

"""
this module creates either standalone jbok one-address Wallet or bip39 24-words mnemonic sequence, based on the
Entropy given as input.
ripemd160 comes from the ripemd package, so no OpenSSL legacy provider is needed.
"""

SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

NETWORKS = {
    'mainnet': {'wif': b'\x80', 'p2pkh': b'\x00', 'p2sh': b'\x05', 'hrp': 'bc'},
    'testnet': {'wif': b'\xef', 'p2pkh': b'\x6f', 'p2sh': b'\xc4', 'hrp': 'tb'},
}


def hash160(data):
    return ripemd160(hashlib.sha256(data).digest())


def b58check(payload):
    return base58.b58encode_check(payload).decode()


class Wallet:

    def __init__(self, wType, wName='default', net='mainnet'):
        self.type = wType
        self.wallet_name = wName
        self.network = net
        self.wallet = {}
        return

    def set_network(self, net='mainnet'):
        self.network = net
        return net

    def set_entropy(self, w_entropy):
        self.entropy = w_entropy
        return w_entropy

    def set_wallet_name(self, w_name):
        self.wallet_name = w_name
        return w_name

    def qr_gen(self):
        """ generate QR codes for addresses """
        for addr_type in ('p2pkh', 'p2wpkh-p2sh', 'p2wpkh'):
            qrcode.make(self.wallet[addr_type]).save("%s-%s.png" % (self.wallet_name, addr_type))
        return True

    def get_jbok(self):
        """ creates a 1 key standalone JBOK Wallet """
        net = NETWORKS[self.network]
        k = bytes.fromhex(self.entropy)
        if len(k) != 32 or not 0 < int.from_bytes(k, 'big') < SECP256K1_N:
            raise ValueError("entropy is not a valid secp256k1 private key")

        """ compressed public key and its hash160 """
        pub = coincurve.PrivateKey(k).public_key.format(compressed=True)
        h160 = hash160(pub)
        redeem_script = b'\x00\x14' + h160

        wallet = {'name': self.wallet_name,
                  'network': 'bitcoin ' + self.network,
                  'private': k.hex(),
                  'public': pub.hex().upper(),
                  'hash160': h160.hex(),
                  'WIF': b58check(net['wif'] + k + b'\x01'),
                  'p2pkh': b58check(net['p2pkh'] + h160),
                  'p2wpkh-p2sh': b58check(net['p2sh'] + hash160(redeem_script)),
                  'p2wpkh': bech32.encode(net['hrp'], 0, h160)
                  }
        self.wallet = wallet
        return wallet

    def get_bip39(self):
        """ bip39 24 words mnemonic from the 256 bits entropy as is """
        ent = bytes.fromhex(self.entropy)
        if len(ent) != 32:
            raise ValueError("bip39 24 words needs 256 bits entropy")

        # 256 bits entropy + 8 bits checksum = 24 words of 11 bits
        v = (int.from_bytes(ent, 'big') << 8) | hashlib.sha256(ent).digest()[0]
        words = ' '.join(wordslist.wl[(v >> (11 * i)) & 0x7ff] for i in reversed(range(24)))
        self.words = words
        return words
