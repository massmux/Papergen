#!/usr/bin/env python

#   Copyright (C) 2019-2020 Denali Sàrl www.denali.swiss, Massimo Musumeci, @massmux
#
#   This file is a script to calculate a paper Wallet by mic gathered randomness
#   or by webcam generated randomness
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


import argparse
import sys

import pg.encryption as enc
import pg.entropy as ee
import pg.keys as keys

from pg.utils import clear
from pg.output import *

""" parsing arguments """


def parse_arguments():
    global args
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
    args = parser.parse_args()


def main():
    a = ee.Entropy(entropy_source)
    clear()
    working_message = "Getting data from mic.. please wait" if entropy_source == 'mic' else "Getting data from " \
                                                                                            "webcam.. please wait "
    print(working_message)
    priv = a.get_entropy()
    if not priv:
        print("Error: sound or video devices not working, aborted")
        sys.exit()
    clear()
    """Wallet: Jbok/single"""
    if w_type == 'single':
        jwallet = keys.Wallet(w_type, w_name, net)
        jwallet.set_entropy(priv)
        wallet_single = jwallet.get_jbok()
        single_json=print_single(wallet_single)
        mess = "QRCODES: {:12}".format("Created") if jwallet.qr_gen() else "QRCODES: {:12}".format("Error")
        print(mess)
        """ if a gpg recipient is specified then writing an encrypted file with Wallet and omitting writing qrcodes """
        if gpg_recipient != "":
            if enc.enc_data(w_name + ".asc", single_json, gpg_recipient):
                print("Wrote armored gpg file %s to recipient key %s " % (w_name + ".asc", gpg_recipient))
            else:
                print("GPG error, check keys!")

    else:
        """Wallet bip39"""
        jwallet = keys.Wallet(w_type)
        jwallet.set_entropy(priv)
        words = jwallet.get_bip39()
        bip39_json=print_bip39(words,priv)
        if gpg_recipient != "":
            if enc.enc_data(w_name + ".asc", bip39_json, gpg_recipient):
                print("Wrote armored gpg file %s to recipient key %s " % (w_name + ".asc", gpg_recipient))
            else:
                print("GPG error, check keys!")


if __name__ == "__main__":
    parse_arguments()
    (net, w_name, w_type, entropy_source, gpg_recipient) = (
        args.network, args.denomination, args.type, args.entropy, args.write)
    main()
