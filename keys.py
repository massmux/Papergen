#!/usr/bin/python3

#   Copyright (C) 2019-2020 Denali Sàrl www.denali.swiss, Massimo Musumeci, @massmux
#
#   This file is a script to calculate a paper wallet by mic gathered randomness
#
#   It is subject to the license terms in the LICENSE file found in the top-level
#   directory of this distribution.
#
#   No part of this software, including this file, may be copied, modified,
#   propagated, or distributed except according to the terms contained in the
#   LICENSE file.
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER



import bit,bech32, binascii, hashlib
from mnemonic import Mnemonic
from binascii import hexlify, unhexlify
import qrcode

"""
this class creates either standalone jbok one-address wallet or bip39 24-words mnemonic sequence,
based on the entropy given as input.
"""

class wallet():

    def __init__(self,wType,wName='default',net='mainnet'):
        self.type=wType
        self.wallet_name=wName
        self.network=net
        self.wallet={}
        return

    def setNetwork(self,net='mainnet'):
        self.network=net
        return net

    def setEntropy(self,wEntropy):
        self.entropy=wEntropy
        return wEntropy

    def setWalletName(self,wName):
        self.wallet_name=wName
        return wName

    def _hash160(self,keyobj):
        ripemd160=hashlib.new("ripemd160")
        ripemd160.update(hashlib.sha256(keyobj.public_key).digest())
        return ripemd160.digest()

    def _bech32enc(self,ohash160,network='mainnet'):
        bechenc=bech32.encode("bc",0,ohash160) if network=='mainnet' else bech32.encode("tb",0,ohash160)
        return bechenc

    def _getsha256(self,z):
        return hashlib.sha256(z.encode('utf-8')).hexdigest()

    def qrGen(self):
        """ generate QR codes for WIF key and addresses """
        try:
            (qr_wif,qr_addr,qr_segwit,qr_bech32) =(qrcode.make(self.wallet['WIF']),
                                            qrcode.make(self.wallet['p2pkh'] ),
                                            qrcode.make(self.wallet['p2wpkh-ps2h']),
                                            qrcode.make(self.wallet['p2wpkh'])
                                            )
            qr_wif.save(self.wallet_name+"-WIF.png")
            qr_addr.save(self.wallet_name+"-p2pkh.png")
            qr_segwit.save(self.wallet_name+"-p2wpkh-p2sh.png")
            qr_bech32.save(self.wallet_name+"-p2wpkh.png")
            return True
        except:
            return False

    
    def getJBOK(self):
      """ creates a 1 key standalone JBOK wallet """

      """ define the key object """
      key=bit.Key.from_hex(self.entropy) if self.network=='mainnet' else bit.PrivateKeyTestnet.from_hex(self.entropy)

      """ private and public key values in hex format """
      hex_k=key.to_hex()
      hex_K=bit.utils.bytes_to_hex(key.public_key,True)

      """ calculate hash160 and bech32 address """
      hex_hash160=self._hash160(key).hex()
      bech32=self._bech32enc(self._hash160(key), self.network)

      wallet={  'name': self.wallet_name,
            'network': 'bitcoin '+ self.network,
            'private': hex_k,
            'public': hex_K,
            'hash160': hex_hash160,
            'WIF': key.to_wif(),
            'p2pkh': key.address,
            'p2wpkh-ps2h': key.segwit_address,
            'p2wpkh': bech32
            }
      self.wallet=wallet
      return wallet


    def getBip39(self):
        """ creates a bip39 full entropic mnemonic as a HD wallet """
        mnemo = Mnemonic('english')
        hash0=self._getsha256(self.entropy)
        entropy_b = bytearray(hash0, 'utf-8')
        entropy_hash =hashlib.sha256(entropy_b).digest()
        entropy = hexlify(entropy_hash)
        words = mnemo.to_mnemonic(entropy_hash)
        self.words=words
        return words

