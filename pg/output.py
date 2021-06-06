
import json

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
    return bip39_json

def print_single(wallet):
    print("** WALLET JBOK/single **\n")
    print(json.dumps(wallet, indent=4, sort_keys=False, separators=(',', ': ')))
    single_wallet_json = json.dumps(wallet)
    return single_wallet_json
