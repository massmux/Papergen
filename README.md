# Papergen

Bitcoin paperwallet generator using entropy from the microphone or the webcam.

Papergen generates either a standalone single-key bitcoin wallet or a 24-word bip39 HD mnemonic. The entropy is gathered from physical noise (microphone or webcam), quality-checked, and mixed with the operating system CSPRNG, so the result is suitable for production keys.

It must run on an offline system, for example a live distro like Tails without persistence and without any Internet connection. The script does not need to be online for any purpose.

## Features

- **Single wallet** (`-t single`): one private key with WIF, public key, hash160 and the addresses p2pkh, p2wpkh-p2sh and p2wpkh. QR codes of the addresses (public data only) are written as PNG files.
- **bip39 HD wallet** (`-t bip39`): a 24-word mnemonic (256 bits entropy + 8 bits checksum). The printed 256-bit entropy is exactly the bip39 entropy of the mnemonic, so it can be verified with any standard bip39 tool. The network choice has no influence here.
- **Entropy source** (`-e mic` or `-e photo`): microphone noise or webcam sensor noise.
- **Networks** (`-n mainnet` or `-n testnet`).
- **Encrypted output** (`-w <gpg recipient>`): the wallet is shown on screen and also written as an armored gpg file encrypted to the given public key. The filename is the wallet denomination with the `.asc` extension.
- No external library for bip39 and no network dependency. ripemd160 comes from the `ripemd-hash` package, so no OpenSSL legacy provider configuration is needed.

## How the entropy is generated

1. **Sampling.**
   - Mic: 30 seconds of raw 16-bit stereo audio at 44.1 kHz; the first 0.5 s are discarded (device start-up).
   - Webcam: 64 frames after 8 warm-up frames (auto exposure start-up).
2. **Quality check.** A conservative min-entropy estimate (NIST SP 800-90B *most common value*) is computed on the differences between consecutive samples (mic) or consecutive frames (webcam), so the static part of the signal does not count as noise. The generation is **aborted** unless:
   - the estimate is at least 1.0 bit/sample (mic) or 0.5 bit/sample (webcam), and
   - after trusting only 1/1000 of the estimate (to account for correlated samples), at least 1024 bits remain, 4x the 256 bits extracted.

   A muted mic, digital silence, a partially silent recording, a covered or frozen webcam are rejected instead of silently producing a predictable key.
3. **Conditioning and mixing.** The accepted raw samples are hashed with sha256 and mixed with 256 bits from the operating system CSPRNG:

   ```
   entropy = sha256("papergen-entropy-v2" || sha256(raw samples) || os.urandom(32))
   ```

   The result is at least as strong as the stronger of the two sources: a weak or tampered physical device cannot make the key worse than `os.urandom`, and a compromised OS RNG is still covered by the physical noise.
4. **Key validation.** For single wallets, the key is checked to be in the valid secp256k1 range.

At the end of every run the script prints the measured estimate, e.g. `Entropy check: mic noise 5.32 bits/sample (min-entropy estimate), mixed with OS CSPRNG`.

## Entropy analysis

The raw physical samples were analysed **before hashing**. After sha256 any statistical test passes, even with a muted microphone, so testing the final output alone proves nothing. The session analysed used the same amount of data as a real run: 30 s of mic audio and 64 webcam frames on a laptop (Intel SOF audio, integrated 640x480 webcam). The estimators follow NIST SP 800-90B (simplified implementation of *most common value*, *t-tuple* and *Markov*), plus lzma compression and autocorrelation.

### Physical sources

| Source | Conservative min-entropy | Total gathered | vs 256 bits needed |
|---|---|---|---|
| Microphone, per channel (low byte of the samples) | ~4.9 bits/sample | ~6.4 Mbit | ~25,000x |
| Webcam, temporal differences (low byte) | ~2.1 bits/value | ~15 Mbit on 8 of the 63 frame pairs | far beyond |

Other mic results: no clipping, least significant bit perfectly balanced (0.500), lzma cannot compress the low byte below ~6 bits/byte.

Observed structure, all covered by the 1/1000 credit factor:

- **The mic signal is not pure white noise.** Nearby samples are correlated (~0.5 at lags 3-5), due to ambient sound and resampling in the audio stack. Even with only 1/1000 of the estimate trusted, ~6,400 bits remain versus the 1,024 required.
- **The two mic channels are correlated (0.33).** They are not two independent sources, so counting both overestimates slightly.
- **The webcam has strong correlation between adjacent pixels (0.72)**, caused by in-sensor processing and compression. The -0.48 correlation between consecutive frame differences is expected, since two consecutive differences share one frame.

### Rejection of bad sources

Simulated failure cases fed to the quality check:

| Case | Estimate | Result |
|---|---|---|
| Muted mic (all zeros) | 0.00 bits | rejected |
| Constant DC offset | 0.00 bits | rejected |
| 5 s of noise followed by 25 s of silence | 0.26 bits | rejected |
| Black / covered webcam | 0.00 bits | rejected |
| Real-like noise | ~5.9 bits | accepted |

### Final output

- **OS CSPRNG mixing:** feeding the same identical physical samples 3,000 times produced 3,000 different outputs, so `os.urandom` is really mixed in.
- **Statistical sanity check** on 768,000 output bits: monobit z = 1.20, runs z = 0.24, byte chi-square 283.5 with 255 degrees of freedom. All within the expected range, but after sha256 these are only a consistency check, not a proof of quality.

### Resulting entropy

The final value has **full 256 bits of entropy**: the maximum for a bitcoin private key or a 24-word bip39 mnemonic. sha256 cannot output more than 256 bits, and its input carries far more (~6,400 conservatively credited bits from the mic plus 256 bits from `os.urandom`). To drop below 256 bits both sources would have to fail at the same time.

The effective security of a bitcoin key is ~128 bits, because of the best known attacks on secp256k1. This is a limit of bitcoin cryptography, not of the key generation.

### Limits of the analysis

- The estimators are a simplified implementation. A formal validation requires the official NIST SP 800-90B tool (`ea_non_iid`) run on the raw samples.
- Results depend on hardware and environment: two sessions on the same laptop gave a mic standard deviation of 18 and 63. For this reason the quality check runs on every generation and blocks poor sessions.

## Requirements

System requirements (gnupg is needed only for `-w`)

```
 sudo apt-get update
 sudo apt-get install libportaudio2 python3-pip python3-venv gnupg
```

Install python dependencies in a virtual environment

```
 python3 -m venv env
 source env/bin/activate
 pip3 install -r requirements.txt
```

If you upgrade an existing environment, remove the conflicting gnupg package first: `pip3 uninstall gnupg` (python-gnupg is used).

## Syntax

To be run on an offline clean computer only. For production use, a live distro like Tails with the Internet connection down is mandatory. You can run the appimage file for this purpose.

```
usage: papergen.py [-h] [-t {single,bip39}] [-n {mainnet,testnet}] [-d DENOMINATION] [-e {mic,photo}] [-w WRITE]

optional arguments:
  -h, --help            show this help message and exit
  -t {single,bip39}, --type {single,bip39}
                        Specify Wallet type. Choose 'single' standalone address or 'bip39' HD(mnemonic), default single
  -n {mainnet,testnet}, --network {mainnet,testnet}
                        Specify network. Choose mainnet or testnet, default mainnet
  -d DENOMINATION, --denomination DENOMINATION
                        Specify a name for your Wallet.
  -e {mic,photo}, --entropy {mic,photo}
                        Specify Entropy source. Choose mic or photo, default mic
  -w WRITE, --write WRITE
                        Specify the recipient public key to use for creating an gpg encrypted file with the Wallet

```

For best results with the mic, have a source of noise in front of it; with the webcam, point it at something moving. If the source is not good enough the script stops with an error instead of generating a weak wallet.

## Usage examples

The keys below are published examples: never use them.

Generating a single address standalone paperwallet on the testnet. The entropy is gathered from the webcam.

```
$ ./papergen.py -t single -n testnet -d example_wallet -e photo
Getting data from webcam.. please wait
** WALLET JBOK/single **

{
    "name": "example_wallet",
    "network": "bitcoin testnet",
    "private": "db37912c80d40757b200b32c7a32c3f036fa236eec651ec3ea5234a9468f5753",
    "public": "03C67FB24356D411FFD07BD7F4D710FAF738BB843E452359DBA511D20FFCBECC64",
    "hash160": "aed37d9a0d4272c6348c210889b6d160beed53b7",
    "WIF": "cUvq9bKs9kxHkFDVUULrv2KfTCsMREBcoEN5nJqbnnDmAU8Dikgt",
    "p2pkh": "mwTME4PWZZLjWeYV6HUYtq62X2e1irQV4a",
    "p2wpkh-p2sh": "2N5x3Pr9WX7arSZKHZoxRTXSFywp84RiVAA",
    "p2wpkh": "tb1q4mfhmxsdgfevvdyvyyygndk3vzlw65ahukzf8t"
}
QRCODES: Created
Entropy check: photo noise 3.86 bits/sample (min-entropy estimate), mixed with OS CSPRNG
```

Generating a HD bip39 mnemonic 24-word sequence. The entropy is gathered from the mic noise.

```
$ ./papergen.py -t bip39
Getting data from mic.. please wait
** WALLET HD Bip39 24 words mnemonic **

Generated Entropy 256bits
7f7e9754dbba4129bb91b6b590f9a8e038b5891243d092eac60a23d2a22c65f2

Single line output
legal visa steel resist piano network unusual cycle remain march health scatter mercy setup empower key napkin file little element clay bike oak dutch

Json output
{
    "1": "legal",
    "2": "visa",
    "3": "steel",
    ...
    "22": "bike",
    "23": "oak",
    "24": "dutch"
}
Entropy check: mic noise 5.32 bits/sample (min-entropy estimate), mixed with OS CSPRNG
```

If the source is not working, for example with a muted mic:

```
Error: mic noise too poor (0.00 bits/sample estimated, 1.00 required): device muted, covered, frozen or not working, aborted
```

## Refs

Please refer to https://www.massmux.com and https://massmux.org for more infos.

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND **NONINFINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
