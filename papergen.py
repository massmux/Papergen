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


import bit,sys,os
import bech32, binascii, hashlib
import subprocess, argparse,qrcode

""" check if sounddevice lib is available, if it is then gets imported """
try:
    import sounddevice
    mode='sd'
except ImportError:
    mode='arec'

""" system constants """

NOISE_SAMPLE        = 30     # main sampling seconds
SHA256_ROUNDS       = 2048  # sha256 rounds (number)
NOISE_SAMPLE_SALT   = 5     # salt sampling seconds
SAMPLE_RATE         = 44100 # samplerate
SAMPLING_FMT        = 'wav'

""" global """
wallet={}

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

def clear():
    """ clear screen """
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

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

clear()

wallet={'network': 'bitcoin '+net,
        'private': hex_k,
        'public': hex_K,
        'hash160': hex_hash160,
        'WIF': key.to_wif(),
        'p2pkh': key.address,
        'p2wpkh-ps2h': key.segwit_address,
        'p2wpkh': bech32
        }


""" printing formatted wallet """
print("**WALLET**\n")
for i in wallet.keys():
    print ("{:12}: {:12}".format(i, wallet[i]))
print()


""" creating png qrcodes images """
try:
    qr_wif,qr_addr,qr_segwit,qr_bech32 = qrcode.make(wallet['WIF']), qrcode.make(wallet['p2pkh'] ), qrcode.make(wallet['p2wpkh-ps2h']), qrcode.make(wallet['p2wpkh'])
    qr_wif.save("WIF.png")
    qr_addr.save("p2pkh.png")
    qr_segwit.save("p2wpkh-p2sh.png")
    qr_bech32.save("p2wpkh.png")
    print ("QRCODES: {:12}".format("Created"))
except:
    print ("QRCODES: {:12}".format("Error"))



