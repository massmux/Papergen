"""
Gathers 256 bits of entropy suitable for a production bitcoin private key or bip39 mnemonic.

The raw physical samples (mic or webcam) are first checked for quality: a conservative min-entropy
estimate (NIST SP 800-90B "most common value", computed on the differences between consecutive
samples so that the static part of the signal is ignored) must show real noise. A muted mic, digital
silence, a covered or frozen webcam are rejected instead of silently producing a predictable key.

The accepted samples are conditioned with sha256 and then mixed with 256 bits from the operating
system CSPRNG. The result is at least as strong as the stronger of the two sources: a weak or
tampered physical device cannot make the key worse than os.urandom, and a compromised OS RNG is
still covered by the physical noise.
"""

import hashlib
import math
import os

import numpy as np

""" system constants """

NOISE_SAMPLE = 30  # mic sampling seconds
SAMPLE_RATE = 44100  # samplerate
MIC_WARMUP = 0.5  # seconds discarded at the beginning of the recording (device start-up)
IMG_SAMPLES = 64  # webcam frames used
IMG_WARMUP = 8  # webcam frames discarded (auto exposure start-up)

MIN_ENTROPY_PER_SAMPLE = {'mic': 1.0, 'photo': 0.5}  # bits, min-entropy estimate required per sample
CREDIT_FRACTION = 0.001  # only 1/1000 of the estimate is trusted, to account for correlated samples
REQUIRED_BITS = 1024  # credited bits required, 4x the 256 bits we extract
MIX_LABEL = b'papergen-entropy-v2'


class EntropyError(Exception):
    pass


def min_entropy_mcv(values):
    """ NIST SP 800-90B 6.3.1 most common value estimate, in bits per sample """
    n = len(values)
    if n < 2:
        return 0.0
    _, counts = np.unique(values, return_counts=True)
    p = counts.max() / n
    p_upper = min(1.0, p + 2.576 * math.sqrt(p * (1.0 - p) / (n - 1)))
    return max(0.0, -math.log2(p_upper))


def check_quality(source, series):
    """ series: list of 1-D int arrays of consecutive samples. Returns (per-sample estimate, credited bits) """
    estimates, total = [], 0
    for s in series:
        deltas = np.diff(s.astype(np.int32))
        estimates.append(min_entropy_mcv(deltas))
        total += len(deltas)
    h = min(estimates)
    credited = h * total * CREDIT_FRACTION
    if h < MIN_ENTROPY_PER_SAMPLE[source] or credited < REQUIRED_BITS:
        raise EntropyError("%s noise too poor (%.2f bits/sample estimated, %.2f required): "
                           "device muted, covered, frozen or not working"
                           % (source, h, MIN_ENTROPY_PER_SAMPLE[source]))
    return h, credited


class Entropy:

    def __init__(self, source='mic'):
        self.source = source
        self.entropy = False
        self.error = None
        self.estimate = None
        return

    def _get_mic_samples(self):
        """ records raw 16 bit samples from the default input device, one array per channel """
        import sounddevice
        rec = sounddevice.rec(int(SAMPLE_RATE * NOISE_SAMPLE), samplerate=SAMPLE_RATE, channels=2,
                              dtype='int16', blocking=True)
        rec = rec[int(SAMPLE_RATE * MIC_WARMUP):]
        return rec.tobytes(), [rec[:, c] for c in range(rec.shape[1])]

    def _get_photo_samples(self):
        """ takes multiple photos from webcam (device 0), returns raw data and one array per frame pair """
        import cv2
        camera = cv2.VideoCapture(0)
        try:
            if not camera.isOpened():
                raise EntropyError("webcam not available")
            frames = []
            for i in range(IMG_WARMUP + IMG_SAMPLES):
                ok, image = camera.read()
                if not ok or image is None:
                    raise EntropyError("webcam read failed")
                if i >= IMG_WARMUP:
                    frames.append(image)
        finally:
            camera.release()
        # temporal noise: pixel differences between consecutive frames
        series = [(b.astype(np.int16) - a.astype(np.int16)).ravel() for a, b in zip(frames, frames[1:])]
        return b''.join(f.tobytes() for f in frames), series

    def get_entropy(self):
        """ returns 256 bits entropy as hex string from the chosen source, False on failure (see self.error) """
        try:
            if self.source == 'mic':
                raw, series = self._get_mic_samples()
            elif self.source == 'photo':
                raw, series = self._get_photo_samples()
            else:
                raise EntropyError("unknown entropy source %s" % self.source)
            self.estimate, _ = check_quality(self.source, series)
            physical = hashlib.sha256(raw).digest()
            self.entropy = hashlib.sha256(MIX_LABEL + physical + os.urandom(32)).hexdigest()
        except Exception as e:
            self.error = str(e)
            self.entropy = False
        return self.entropy
