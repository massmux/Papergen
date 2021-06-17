#!/usr/bin/env python


# https://pypi.org/project/btc-hd-wallet/
# implementation of BIP85

from btc_hd_wallet import BIP85DeterministicEntropy

xprv = "xprv9s21ZrQH143K2n9ryKS5EXxvQaNSbCxrVHSUigxG9ywY6GVQYsrk6n8e9j6m9z9LvBULFnSyjcLFxbG6WtXoeYRF19f1FY23nni39XSLPWm"
# create new deterministic entropy object from extended private key

bip85 = BIP85DeterministicEntropy.from_xprv(xprv=xprv)


# bip39 mnemonic
print("mnemonic 24: "+bip85.bip39_mnemonic(word_count=24, index=0))
print("mnemonic 12: "+bip85.bip39_mnemonic(word_count=12, index=0))
print("mnemonic 15: "+bip85.bip39_mnemonic(word_count=15, index=1))

# wallet import format (WIF)
print("wif0: "+bip85.wif(index=0))
print("wif1: "+bip85.wif(index=1))

# extended private key (XPRV)
print("xpriv0: "+bip85.xprv(index=0))
print("xpriv1: "+bip85.xprv(index=1))

# hex
print("hex0: "+bip85.hex(index=0))
print("hex1: "+bip85.hex(num_bytes=64, index=0))

# bip85 is also available in BaseWallet class as its attribute
from btc_hd_wallet.base_wallet import BaseWallet

w = BaseWallet.new_wallet()
type(w.bip85) == BIP85DeterministicEntropy

#print(BIP85DeterministicEntropy.bip39_mnemonic(12,0))
