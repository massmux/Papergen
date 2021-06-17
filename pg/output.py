
import json
from mnemonic import Mnemonic
from btc_hd_wallet import BIP85DeterministicEntropy

"""this module prints outputs for the user and returns json"""

def print_bip39(mnemonic_words,base_entropy):
    print("** WALLET HD Bip39 24 words mnemonic **\n")
    print("Generated Entropy 256bits\n%s\n" % str(base_entropy))
    print("Single line output\n%s\n" % mnemonic_words)
    print("Json output")
    n = 1
    hd_bip39_wallet = {}
    for i in mnemonic_words.split(" "):
        hd_bip39_wallet[n] = i
        n += 1
    bip39_json = json.dumps(hd_bip39_wallet)
    print(json.dumps(hd_bip39_wallet, indent=4, sort_keys=False, separators=(',', ': ')))
    m = Mnemonic("english")
    seed = Mnemonic.to_seed(mnemonic_words)
    xprv = Mnemonic.to_hd_master_key(seed)
    print("xprv: "+ xprv)
    bip85 = BIP85DeterministicEntropy.from_xprv(xprv=xprv)
    print("bip85 mnemonic 12, index 0: " + bip85.bip39_mnemonic(word_count=12, index=0))
    return bip39_json

def print_single(wallet):
    print("** WALLET JBOK/single **\n")
    print(json.dumps(wallet, indent=4, sort_keys=False, separators=(',', ': ')))
    single_wallet_json = json.dumps(wallet)
    return single_wallet_json
