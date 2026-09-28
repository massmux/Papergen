#!/usr/bin/env python3

import argparse
import sys

import pg.entropy as ee
import pg.keys as keys

from pg.utils import clear
from pg.output import print_bip39, print_single

""" parsing arguments """


def parse_arguments():
    parser = argparse.ArgumentParser("papergen.py")
    parser.add_argument("-t", "--type", help="Specify Wallet type. Choose \
                        'single' standalone address or 'bip39' HD(mnemonic), default single", type=str, required=False,
                        choices=['single', 'bip39'], default='single')
    parser.add_argument("-n", "--network", help="Specify network. Choose \
                        mainnet or testnet, default mainnet", type=str, required=False, choices=['mainnet', 'testnet'],
                        default='mainnet')
    parser.add_argument("-d", "--denomination", help="Specify a name for your Wallet.", type=str, required=False, default='default')
    parser.add_argument("-e", "--entropy", help="Specify Entropy source. Choose \
                        mic or photo, default mic", type=str, required=False, choices=['mic', 'photo'], default='mic')
    parser.add_argument("-w", "--write", help="Specify the recipient public key to use for \
                        creating an gpg encrypted file with the Wallet", type=str, required=False, default='')
    return parser.parse_args()


def write_encrypted(fname, data, recipient):
    """ if a gpg recipient is specified then writing an encrypted file with Wallet """
    import pg.encryption as enc
    ok, status = enc.enc_data(fname, data, recipient)
    if ok:
        print("Wrote armored gpg file %s to recipient key %s " % (fname, recipient))
    else:
        print("GPG error (%s), check keys!" % status)


def main(args):
    a = ee.Entropy(args.entropy)
    clear()
    print("Getting data from %s.. please wait" % ('mic' if args.entropy == 'mic' else 'webcam'))
    priv = a.get_entropy()
    if not priv:
        print("Error: %s, aborted" % a.error)
        sys.exit(1)
    clear()
    if args.type == 'single':
        """Wallet: Jbok/single"""
        jwallet = keys.Wallet(args.type, args.denomination, args.network)
        jwallet.set_entropy(priv)
        wallet_json = print_single(jwallet.get_jbok())
        """ QR codes contain only the public addresses """
        try:
            jwallet.qr_gen()
            print("QRCODES: {:12}".format("Created"))
        except Exception as e:
            print("QRCODES: {:12} ({})".format("Error", e))
    else:
        """Wallet bip39"""
        jwallet = keys.Wallet(args.type)
        jwallet.set_entropy(priv)
        wallet_json = print_bip39(jwallet.get_bip39(), priv)
    print("Entropy check: %s noise %.2f bits/sample (min-entropy estimate), mixed with OS CSPRNG"
          % (args.entropy, a.estimate))
    if args.write:
        write_encrypted(args.denomination + ".asc", wallet_json, args.write)


if __name__ == "__main__":
    main(parse_arguments())
