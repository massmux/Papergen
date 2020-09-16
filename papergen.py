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
import subprocess, argparse,qrcode

""" check if sounddevice lib is available, if it is then gets imported """
try:
    import sounddevice
    mode='sd'
except ImportError:
    mode='arec'

""" system constants """

NOISE_SAMPLE        = 5     # main sampling seconds
SHA256_ROUNDS       = 2048  # sha256 rounds (number)
NOISE_SAMPLE_SALT   = 3     # salt sampling seconds
SAMPLE_RATE         = 44100 # samplerate
SAMPLING_FMT        = 'wav'

""" parsing arguments """
def parseArguments():
    global args
    parser = argparse.ArgumentParser("papergen.py")
    parser.add_argument("-n","--network", help="Specify network. Choose \
                    mainnet or testnet, default mainnet", type=str, required=True, choices=['mainnet','testnet'],default='mainnet')
    args = parser.parse_args()


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
    """
    creating unique noise by sampling entropy and salting it for SHA256_ROUNDS / use arecord+sha256 OS commands
    this function is better when no equivalent library is available.
    Returns sha256 salt hashed noise
    """
    mycmd=subprocess.getoutput('arecord -d %s -f dat -t %s -q | sha256sum -b' %  (str(NOISE_SAMPLE),SAMPLING_FMT ))
    hash0=mycmd[:64]
    mysalt=subprocess.getoutput('arecord -d %s -f dat -t %s -q | sha256sum -b' %  (str(NOISE_SAMPLE_SALT),SAMPLING_FMT ))
    salt0=mysalt[:64]
    for i in range(0,SHA256_ROUNDS):
        hash0=getsha256(hash0+salt0)
    return hash0


def getNoise256():
    """
    creating unique noise by sampling entropy and salting it for SHA256_ROUNDS / use python lib
    Returns sha256 salt hashed noise
    """
    noise0 = sounddevice.rec(int(SAMPLE_RATE * NOISE_SAMPLE), samplerate=SAMPLE_RATE, channels=2, blocking=True)
    salt0 = sounddevice.rec(int(SAMPLE_RATE * NOISE_SAMPLE_SALT), samplerate=SAMPLE_RATE, channels=2, blocking=True)
    (noise,salt) =( hashlib.sha256(bytearray(b''.join(noise0))).hexdigest() , hashlib.sha256(bytearray(b''.join(salt0))).hexdigest() )
    for i in range(0,SHA256_ROUNDS):
        noise=getsha256(noise+salt)
        ##print ("noise %s salt %s" % (noise,salt))
    return noise


parseArguments()
net=args.network

""" use sounddevice if available, otherwise use arec command """
print("Getting randomness from mic.. please wait")
priv=getRandNoise() if mode=='arec' else getNoise256()

""" define the key object """
key=bit.Key.from_hex(priv) if net=='mainnet' else bit.PrivateKeyTestnet.from_hex(priv)

""" private and public key values in hex format """
hex_k=key.to_hex()
hex_K=bit.utils.bytes_to_hex(key.public_key,True)

""" calculate hash160 and bech32 address """
hex_hash160=hash160(key).hex()
bech32=bech32enc(hash160(key), net) 

""" printing results """
print("\n\tBitcoin Paper wallet generated")
print("\tNetwork:                   ", net)
print("\tPrivate key:               ", (str(hex_k)))
print("\tPublic key:                ", (str(hex_K)))
print("\tHash160:                   ", str(hex_hash160) )
print("\tWIF:                       ", str (key.to_wif() ) )
print("\tp2pkh address:             ", str (key.address ) )
print("\tp2wpkh-p2sh address:       ", str (key.segwit_address ) )
print("\tp2wpkh(bech32) address:    ", str ( bech32))

""" creating png qrcodes images """
try:
    qr_wif= qrcode.make(key.to_wif())
    qr_wif.save("wif.png")
    qr_segwit_addr= qrcode.make(str(key.segwit_address))
    qr_wif.save("p2wpkh-p2sh.png")
    qr_addr= qrcode.make( str(key.address) )
    qr_wif.save("p2pkh.png")
    qr_bech32= qrcode.make( str(bech32) )
    qr_wif.save("p2wpkh.png")
    print("\tQRcode images:             ","Created")
except:
    print("\tQRcode images:             ","Error")



