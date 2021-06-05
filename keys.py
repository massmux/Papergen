#!/usr/bin/python3

#   Copyright (C) 2019-2020 Denali Sàrl www.denali.swiss, Massimo Musumeci, @massmux
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
#   MNEMONIC CALCULATION WAS PROVIDED BY COLDCARD


import hashlib

import bech32
import bit
import qrcode

from wordslist import wl

"""this class creates either standalone jbok one-address Wallet or bip39 24-words mnemonic sequence, based on the 
Entropy given as input. """


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

    def set_entropy(self, wEntropy):
        self.entropy = wEntropy
        return wEntropy

    def set_wallet_name(self, wName):
        self.wallet_name = wName
        return wName

    def _hash160(self, keyobj):
        ripemd160 = hashlib.new("ripemd160")
        ripemd160.update(hashlib.sha256(keyobj.public_key).digest())
        return ripemd160.digest()

    def _bech32enc(self, ohash160, network='mainnet'):
        bechenc = bech32.encode("bc", 0, ohash160) if network == 'mainnet' else bech32.encode("tb", 0, ohash160)
        return bechenc

    def _getsha256(self, z):
        return hashlib.sha256(z.encode('utf-8')).hexdigest()

    def qr_gen(self):
        """ generate QR codes for WIF key and addresses """
        try:
            (qr_wif, qr_addr, qr_segwit, qr_bech32) = (qrcode.make(self.wallet['WIF']),
                                                       qrcode.make(self.wallet['p2pkh']),
                                                       qrcode.make(self.wallet['p2wpkh-ps2h']),
                                                       qrcode.make(self.wallet['p2wpkh'])
                                                       )
            # qr_wif.save(self.wallet_name + "-WIF.png")
            qr_addr.save(self.wallet_name + "-p2pkh.png")
            qr_segwit.save(self.wallet_name + "-p2wpkh-p2sh.png")
            qr_bech32.save(self.wallet_name + "-p2wpkh.png")
            return True
        except:
            return False

    def get_jbok(self):
        """ creates a 1 key standalone JBOK Wallet """

        """ define the key object """
        key = bit.Key.from_hex(self.entropy) if self.network == 'mainnet' else bit.PrivateKeyTestnet.from_hex(
            self.entropy)

        """ private and public key values in hex format """
        hex_k = key.to_hex()
        hex_K = bit.utils.bytes_to_hex(key.public_key, True)

        """ calculate hash160 and bech32 address """
        hex_hash160 = self._hash160(key).hex()
        bech32 = self._bech32enc(self._hash160(key), self.network)

        wallet = {'name': self.wallet_name,
                  'network': 'bitcoin ' + self.network,
                  'private': hex_k,
                  'public': hex_K,
                  'hash160': hex_hash160,
                  'WIF': key.to_wif(),
                  'p2pkh': key.address,
                  'p2wpkh-ps2h': key.segwit_address,
                  'p2wpkh': bech32
                  }
        self.wallet = wallet
        return wallet

    def get_bip39(self):
        r = self.entropy
        # Calc sha256
        h = hashlib.sha256(r.encode()).digest()

        # Apply BIP39 to convert into seed words
        v = int.from_bytes(h, 'big') << 8
        w = []
        for i in range(24):
            v, m = divmod(v, 2048)
            w.insert(0, m)
        assert not v

        # final 8 bits are a checksum
        w[-1] |= hashlib.sha256(h).digest()[0]

        words = ' '.join('%s' % (wl[i]) for n, i in enumerate(w))
        self.words = words
        return words
