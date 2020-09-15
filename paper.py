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


import bit,sys
import bech32, binascii, hashlib
import subprocess, argparse, sounddevice
from sty import fg, bg, ef, rs

""" parsing arguments """
def parseArguments():
    global args
    parser = argparse.ArgumentParser("papergen.py")
    parser.add_argument("-n","--network", help="Specify network. Choose \
                    mainnet or testnet, default mainnet", type=str, required=True, choices=['mainnet','testnet'],default='mainnet')
    args = parser.parse_args()


def title(color, name):
    print()
    bgc = bg(color) if isinstance(color,str) else bg(*color)
    print(bgc + ef.bold + "{:^20}".format(name) + rs.bg + rs.bold_dim)

def hash160(keyobj):
    ripemd160=hashlib.new("ripemd160")
    ripemd160.update(hashlib.sha256(keyobj.public_key).digest())
    return ripemd160.digest()

def bech32enc(ohash160,network='mainnet'):
        bechenc=bech32.encode("bc",0,ohash160) if network=='mainnet' else bech32.encode("tb",0,ohash160)
        return bechenc

def getsha256(z):
    return hashlib.sha256(z.encode('utf-8')).hexdigest()

def getRandNoise():
    mycmd=subprocess.getoutput('arecord -d %s -f dat -t wav -q | sha256sum -b' %  str(rnd_len) )
    hash0=mycmd[:64]
    mysalt=subprocess.getoutput('arecord -d %s -f dat -t wav -q | sha256sum -b' %  str(slt_len) )
    salt0=mysalt[:64]
    for i in range(0,sha_rounds):
        hash0=getsha256(hash0+salt0)
    return hash0

def getNoise(sec):
    sound = sounddevice.rec(int(SAMPLE_RATE * sec), samplerate=SAMPLE_RATE, channels=2, blocking=True)
    return hashlib.sha256(bytearray(b''.join(sound))).hexdigest()

parseArguments()
net=args.network

(rnd_len, sha_rounds,slt_len)=(5,2048,2)

print("Getting randomness from mic.. please wait")
priv=getRandNoise()

""" define the key object """
key=bit.Key.from_hex(priv) if net=='mainnet' else bit.PrivateKeyTestnet.from_hex(priv)

""" private and public key values in hex format """
hex_k=key.to_hex()
hex_K=bit.utils.bytes_to_hex(key.public_key,True)

""" calculate hash160 and bech32 address """
hex_hash160=hash160(key).hex()
bech32=bech32enc(hash160(key), net) 

""" printing results """
title((255, 150, 50), "\tBitcoin Paper wallet generated")
print("\tNetwork:                   ", net)
print("\tPrivate key:               ", (str(hex_k)))
print("\tPublic key:                ", (str(hex_K)))
print("\tHash160:                   ", str(hex_hash160) )
print("\tWIF:                       ", str (key.to_wif() ) )
print("\tp2pkh address:             ", str (key.address ) )
print("\tp2wpkh-p2sh address:       ", str (key.segwit_address ) )
print("\tp2wpkh(bech32) address:    ", str ( bech32))

try:
    c=subprocess.getoutput('qr %s > %s' %  (key.to_wif(), 'wif.png')  )
    c=subprocess.getoutput('qr %s > %s' %  (str(key.segwit_address), 'p2wpkh-p2sh.png')  )
    c=subprocess.getoutput('qr %s > %s' %  (str(bech32), 'p2wpkh.png')  )
    print("\tQRcode images:             ","Created")
except:
    print("\tQRcode images:             ","Error")

