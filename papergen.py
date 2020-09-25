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


import sys,os,argparse
import qrcode
import mic
import keys


""" parsing arguments """
def parseArguments():
    global args
    parser = argparse.ArgumentParser("papergen.py")
    parser.add_argument("-t","--type", help="Specify wallet type. Choose \
                        jbok (single standalone address) or bip39 HD(mnemonic), default JBOK", type=str, required=False, choices=['jbok','bip39'],default='jbok')
    parser.add_argument("-n","--network", help="Specify network. Choose \
                        mainnet or testnet for jbok type, default mainnet", type=str, required=False, choices=['mainnet','testnet'],default='mainnet')
    parser.add_argument("-d","--denomination", help="Specify a name for your wallet.", \
                        type=str, required=False, default='default')
    args = parser.parse_args()


def clear():
    """ clears screen """
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def qrGen(oWallet,wName):
   """ generate QR codes for WIF key and addresses """
   try:
      (qr_wif,qr_addr,qr_segwit,qr_bech32) =(qrcode.make(oWallet['WIF']), 
                                            qrcode.make(oWallet['p2pkh'] ), 
                                            qrcode.make(oWallet['p2wpkh-ps2h']),
                                            qrcode.make(oWallet['p2wpkh'])
                                            )
      qr_wif.save(wName+"-WIF.png")
      qr_addr.save(wName+"-p2pkh.png")
      qr_segwit.save(wName+"-p2wpkh-p2sh.png")
      qr_bech32.save(wName+"-p2wpkh.png")
      return True
   except:
      return False

def main():
  print("Getting randomness from mic.. please wait")
  priv=mic.getRandNoise() if mic.mode=='arec' else mic.getNoise256()
  clear()
  if wType=='jbok':
     wallet=keys.getJBOK(priv,net,wName)

     """ printing formatted wallet """
     print("** WALLET JBOK **\n")
     for i in wallet.keys():
        print ("{:12}: {:12}".format(i, wallet[i]))
     print()

     """ just tell if qrcodes are generated correctly """
     mess="QRCODES: {:12}".format("Created") if qrGen(wallet,wName) else "QRCODES: {:12}".format("Error")
     print(mess)
  else:
     print("** WALLET HD Bip39 24 words mnemonic **\n")
     words=keys.getBip39(priv)
     print("[] Single line output")
     print(words+"\n")
     words_arr=words.split(" ")
     print("[] Numbered list output")
     n=1
     for i in words_arr:
        print ("{:12}: {:12}".format(n, i))
        n+=1


if __name__ == "__main__":
    parseArguments()
    (net,wName,wType)=(args.network,args.denomination,args.type)
    main()

