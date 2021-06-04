#!/usr/bin/python3

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



import subprocess,os
import hashlib
import cv2,base64
import sounddevice


""" system constants """

NOISE_SAMPLE        = 30    # main sampling seconds
SHA256_ROUNDS       = 2048  # sha256 rounds (number)
NOISE_SAMPLE_SALT   = 5     # salt sampling seconds
SAMPLE_RATE         = 44100 # samplerate
SAMPLING_FMT        = 'wav'
IMG_SAMPLES         = 64
IMG_SAMPLES_SALT    = 8

class entropy():

    def __init__(self,source='mic'):
        self.source=source
        self.entropy=0
        return


    def _getsha256(self,z):
        return hashlib.sha256(z.encode('utf-8')).hexdigest()


    def _getMicSd(self):
        """
        creating unique noise by sampling entropy and salting it for SHA256_ROUNDS. Returns sha256 salt hashed noise.
        """
        try:
            noise0 = sounddevice.rec(int(SAMPLE_RATE * NOISE_SAMPLE), samplerate=SAMPLE_RATE, channels=2, blocking=True)
            salt0 = sounddevice.rec(int(SAMPLE_RATE * NOISE_SAMPLE_SALT), samplerate=SAMPLE_RATE, channels=2, blocking=True)
            (noise,salt) =( hashlib.sha256(bytearray(b''.join(noise0))).hexdigest() , hashlib.sha256(bytearray(b''.join(salt0))).hexdigest() )
            for i in range(0,SHA256_ROUNDS):
                noise=self._getsha256(noise+salt)
        except:
            # errore gathering noise. then probably device not present or not working
            noise=False
        return noise


    def _getImgRnd(self):
        # if false was returned, the device is not working, then exit function
        if self.img_rnd==False:
            return False
        """ salt hashing and converting image data into 256 bits final hash """
        img_rnd_result= self._getsha256( str(self.img_rnd['base'] ) ) 
        salt = self._getsha256(str( self.img_rnd['salt'] ) )
        for i in range(0,2048):
            img_rnd_result=self._getsha256(img_rnd_result+salt)
        return img_rnd_result


    def _takePhoto(self):
        """ taking multiple photos from webcam in order to create randomness. Returns data and salt """
        try:
            camera = cv2.VideoCapture(0)
            (all_data,all_salt)=("","")
            for i in range(IMG_SAMPLES):
                return_value, image = camera.read()
                ocurrent = base64.b64encode(image)
                all_data=all_data+str(ocurrent)
            for z in range(IMG_SAMPLES_SALT):
                return_value, image = camera.read()
                ocurrent = base64.b64encode(image)
                all_salt=all_salt+str(ocurrent)
            del(camera)
            self.img_rnd={  'base': all_data,
                            'salt': all_salt
                        }
        except:
            # in this case probably we dont have webcam or device not working
            self.img_rnd=False
        return self.img_rnd


    def getEntropy(self):
        """ returns true entropy from chosen source """
        if self.source=='mic':
            self.entropy=self._getMicSd()
        elif self.source=='photo':
            self._takePhoto()
            self.entropy=self._getImgRnd()
        return self.entropy
    
