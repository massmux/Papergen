
#   Copyright (C) 2019-2020 Denali Sàrl www.denali.swiss, Massimo Musumeci, @massmux
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


import hashlib

import base64
import cv2
import sounddevice
import binascii

""" system constants """

NOISE_SAMPLE = 30  # main sampling seconds
SHA256_ROUNDS = 2048  # sha256 rounds (number)
NOISE_SAMPLE_SALT = 5  # salt sampling seconds
SAMPLE_RATE = 44100  # samplerate
SAMPLING_FMT = 'wav'
IMG_SAMPLES = 64
IMG_SAMPLES_SALT = 8


class Entropy:

    def __init__(self, source='mic'):
        self.source = source
        self.entropy = 1
        return

    def _getsha256(self, z):
        return hashlib.sha256(z.encode('utf-8')).hexdigest()

    def _get_mic_sd(self):
        """ creating 256bits entropy from mic. then returns final entropy by using pbkdf2_hmac. """
        try:
            # sampling randomness from device
            noise0 = sounddevice.rec(int(SAMPLE_RATE * NOISE_SAMPLE), samplerate=SAMPLE_RATE, channels=2, blocking=True)
            salt0 = sounddevice.rec(int(SAMPLE_RATE * NOISE_SAMPLE_SALT), samplerate=SAMPLE_RATE, channels=2, blocking=True)
            # hashing the randomness gathered to get 256bits entropy
            (mic_noise, mic_salt) = (   hashlib.sha256(bytearray(b''.join(noise0))).hexdigest(),
                                        hashlib.sha256(bytearray(b''.join(salt0))).hexdigest()
                                    )
            # building final entropy as 256bits
            noise = hashlib.pbkdf2_hmac('sha256', bytes.fromhex(mic_noise), bytes.fromhex(mic_salt), SHA256_ROUNDS)
            noise = binascii.hexlify(bytearray(noise)).decode()
        except:
            noise = False
        return noise


    def _get_img_rnd(self):
        """ creating 256bits entropy from sampling camera. then returns final entropy by using pbkdf2_hmac. """
        img_rnd = self._getsha256(str(self.img_rnd['base']))
        img_salt = self._getsha256(str(self.img_rnd['salt']))
        # returns bytearray
        img_rnd_result_bytes = hashlib.pbkdf2_hmac('sha256', bytes.fromhex(img_rnd), bytes.fromhex(img_salt), SHA256_ROUNDS)
        # from bytearray to hex string
        img_rnd_result = binascii.hexlify(bytearray(img_rnd_result_bytes)).decode()
        return img_rnd_result



    def _take_photo(self):
        """ taking multiple photos from webcam in order to create randomness. Returns data and salt. used device 0 """
        try:
            camera = cv2.VideoCapture(0)
            (all_data, all_salt) = ("", "")
            for i in range(IMG_SAMPLES):
                return_value, image = camera.read()
                ocurrent = base64.b64encode(image)
                all_data = all_data + str(ocurrent)
            for z in range(IMG_SAMPLES_SALT):
                return_value, image = camera.read()
                ocurrent = base64.b64encode(image)
                all_salt = all_salt + str(ocurrent)
            del (camera)
            self.img_rnd = {'base': all_data,
                            'salt': all_salt
                            }
        except:
            self.img_rnd = False
        return self.img_rnd

    def get_entropy(self):
        """ returns true Entropy from chosen source """
        if self.source == 'mic':
            self.entropy = self._get_mic_sd()
        elif self.source == 'photo':
            if self._take_photo():
                self.entropy = self._get_img_rnd()
            else:
                self.entropy = False
        return self.entropy
