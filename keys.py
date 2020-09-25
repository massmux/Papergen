#!/usr/bin/python3

import bit,bech32, binascii, hashlib
from mnemonic import Mnemonic
from binascii import hexlify, unhexlify



""" helper functions """
def hash160(keyobj):
    ripemd160=hashlib.new("ripemd160")
    ripemd160.update(hashlib.sha256(keyobj.public_key).digest())
    return ripemd160.digest()

def bech32enc(ohash160,network='mainnet'):
        bechenc=bech32.encode("bc",0,ohash160) if network=='mainnet' else bech32.encode("tb",0,ohash160)
        return bechenc

""" hash assist """
def getsha256(z):
    return hashlib.sha256(z.encode('utf-8')).hexdigest()


def getJBOK(private_key,network='mainnet',wallet_name='default'):
  """ creates a 1 key standalone JBOK wallet """

  """ define the key object """
  key=bit.Key.from_hex(private_key) if network=='mainnet' else bit.PrivateKeyTestnet.from_hex(private_key)

  """ private and public key values in hex format """
  hex_k=key.to_hex()
  hex_K=bit.utils.bytes_to_hex(key.public_key,True)

  """ calculate hash160 and bech32 address """
  hex_hash160=hash160(key).hex()
  bech32=bech32enc(hash160(key), network)

  wallet={  'name': wallet_name,
            'network': 'bitcoin '+network,
            'private': hex_k,
            'public': hex_K,
            'hash160': hex_hash160,
            'WIF': key.to_wif(),
            'p2pkh': key.address,
            'p2wpkh-ps2h': key.segwit_address,
            'p2wpkh': bech32
        }
  return wallet


def getBip39(entropy):
    """ creates a bip39 full entropic mnemonic as a HD wallet """

    mnemo = Mnemonic('english')
    hash0=getsha256(entropy)
    entropy_b = bytearray(hash0, 'utf-8')
    entropy_hash =hashlib.sha256(entropy_b).digest()
    entropy = hexlify(entropy_hash)
    words = mnemo.to_mnemonic(entropy_hash)
    return words

