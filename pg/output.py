"""this module prints outputs for the user and returns json"""

import json


def print_bip39(mnemonic_words, base_entropy):
    print("** WALLET HD Bip39 24 words mnemonic **\n")
    print("Generated Entropy 256bits\n%s\n" % str(base_entropy))
    print("Single line output\n%s\n" % mnemonic_words)
    print("Json output")
    hd_bip39_wallet = {n: word for n, word in enumerate(mnemonic_words.split(" "), start=1)}
    print(json.dumps(hd_bip39_wallet, indent=4, sort_keys=False, separators=(',', ': ')))
    # TODO bip85 (needs mnemonic and btc-hd-wallet)
    return json.dumps(hd_bip39_wallet)


def print_single(wallet):
    print("** WALLET JBOK/single **\n")
    print(json.dumps(wallet, indent=4, sort_keys=False, separators=(',', ': ')))
    return json.dumps(wallet)
