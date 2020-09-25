#!/usr/bin/python3

import subprocess,hashlib

""" check if sounddevice lib is available, if it is then gets imported """
try:
    import sounddevice
    mode='sd'
except ImportError:
    mode='arec'

""" system constants """

NOISE_SAMPLE        = 30    # main sampling seconds
SHA256_ROUNDS       = 2048  # sha256 rounds (number)
NOISE_SAMPLE_SALT   = 5     # salt sampling seconds
SAMPLE_RATE         = 44100 # samplerate
SAMPLING_FMT        = 'wav'


def getsha256(z):
    return hashlib.sha256(z.encode('utf-8')).hexdigest()


def getRandNoise():
    """
    creating unique noise by sampling entropy and salting it for SHA256_ROUNDS / use arecord+sha256 OS commands
    this function is better when no equivalent library is available. Returns sha256 salt hashed noise
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
    return noise


