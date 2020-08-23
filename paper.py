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
import subprocess

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


(rnd_len, sha_rounds,slt_len)=(5,2048,2)
net="mainnet"

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
print("**Results**")
print("network: %s" % net)
print("private key: %s" % (str(hex_k)))
print("public key: %s" % (str(hex_K)))
print("hash160: %s " % str(hex_hash160) )
print("WIF: %s" % str (key.to_wif() ) )
print("P2PKH address: %s" % str (key.address ) )
print("P2SH address: %s" % str (key.segwit_address ) )
print("bech32 address: %s " % str ( bech32))



