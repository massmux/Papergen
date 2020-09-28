#!/usr/bin/python3


#   Copyright (C) 2019-2020 Denali Sàrl www.denali.swiss, Massimo Musumeci, @massmux
#
#   This file is a script to calculate a paper wallet by mic gathered randomness
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


import sys,os,argparse
import entropy as ee
import keys
import encryption as enc


""" parsing arguments """
def parseArguments():
    global args
    parser = argparse.ArgumentParser("papergen.py")
    parser.add_argument("-t","--type", help="Specify wallet type. Choose \
                        'single' standalone address or 'bip39' HD(mnemonic), default single", type=str, required=False, choices=['single','bip39'],default='single')
    parser.add_argument("-n","--network", help="Specify network. Choose \
                        mainnet or testnet, default mainnet", type=str, required=False, choices=['mainnet','testnet'],default='mainnet')
    parser.add_argument("-d","--denomination", help="Specify a name for your wallet.", \
                        type=str, required=False, default='default')
    parser.add_argument("-e","--entropy", help="Specify entropy source. Choose \
                        mic or photo, default mic", type=str, required=False, choices=['mic','photo'],default='mic')
    parser.add_argument("-w","--write", help="Specify the recipient public key to use for \
                        creating an gpg encrypted file with the wallet", type=str, required=False, default='')
    args = parser.parse_args()


""" just helper func """
def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def main():
  a = ee.entropy(entropy_source)
  working_message="Getting randomness from mic.. please wait" if entropy_source=='mic' else "Getting randomness from webcam.. please wait"
  print (working_message)
  priv = a.getEntropy()
  oWallet=""
  clear()
  if wType=='single':
     jwallet=keys.wallet(wType,wName,net)
     jwallet.setEntropy(priv)
     wallet=jwallet.getJBOK()

     """ printing formatted wallet """
     print("** WALLET JBOK/single **\n")
     for i in wallet.keys():
        print ("{:12}: {:12}".format(i, wallet[i]))
        oWallet+="{:12}: {:12}\n".format(i, wallet[i])
     print()

     """ if a gpg recipient is specified then writing an encrypted file with wallet and omitting writing qrcodes """
     if gpg_recipient != "":
         if enc.encData(wName+".asc",oWallet,gpg_recipient):
            print("wrote gpg file %s to recipient key %s " % (wName+".asc", gpg_recipient) )
         else:
            print("GPG error, check keys!")
     else:
        """ just check if qrcodes are generated correctly """
        mess="QRCODES: {:12}".format("Created") if jwallet.qrGen() else "QRCODES: {:12}".format("Error")
        print(mess)

  else:
     print("** WALLET HD Bip39 24 words mnemonic **\n")
     jwallet=keys.wallet(wType)
     jwallet.setEntropy(priv)
     words=jwallet.getBip39()
     print("[] Single line output")
     print(words+"\n")
     oWallet=words+"\n"
     words_arr=words.split(" ")
     print("[] Numbered list output")
     n=1
     for i in words_arr:
        print ("{:12}: {:12}".format(n, i))
        oWallet+="{:12}: {:12}\n".format(n, i)
        n+=1
     if gpg_recipient != "":
         if enc.encData(wName+".asc",oWallet,gpg_recipient):
            print("wrote gpg file %s to recipient key %s " % (wName+".asc", gpg_recipient) )
         else:
            print("GPG error, check keys!")


if __name__ == "__main__":
    parseArguments()
    (net,wName,wType,entropy_source,gpg_recipient)=(args.network,args.denomination,args.type,args.entropy,args.write)
    main()

