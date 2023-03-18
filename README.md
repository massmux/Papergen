# Papergen

Bitcoin paperwallet generator by mic Entropy or by webcam input

 generate a bitcoin paper Wallet by gathering Entropy from computer microphone. It's important to run on an offline system, for example using a distro like tails without persistence and without any Internet connection. The script does not need to be online for any purpose.

 Since true Entropy from microphone is used, please be assured that your computer audio works, your microphone is active and works taking noise from the environment. Should microphone is off or not working, the Entropy source would be compromised, and your resulting Wallet would be not secure. For optimal result you should have a source of noise in front of microphone.

 If Entropy from webcam is used, please be assured that your computer webcam works. Your webcam infact will take a certain amount of photos in order to get randomness. Should webcam is of or not working, the Entropy source would be compromised, and you resulting Wallet would be not secure. For optimal result you should have the webcam pointed towards something moving fastly in front of it.

 It supports mainnet and testnet. It provides the following bitcoin address formats: p2pkh ; p2wpkh-p2sh ; p2wpkh

- Added feature: now you can specify -d bip39 in order to get a true random generated HD Wallet by 24 words sequence. In this case the network choice has no influece. A 24words bip39 HD mnemonic output is returned with the generated entropy.
- Added feature: now you can specify -e photo or -e mic in order to choose between webcam generated Entropy or microphone generate Entropy
- Added feature: now you can specify the -w flag in order to choose a recipient key (gpg) to write an encrypted Wallet file locally. This means that the Wallet is created, shown on the monitor and written as an encrypted ascii file using the public key specified by the flag. The filename is the same as the Wallet denomination
- Added feature: removed the mnemonic library, because now mnemonic calculation is made without any external lib.

## Note on openssl

Hashlib uses OpenSSL for ripemd160 and apparently OpenSSL disabled some older crypto algos around version 3.0 in November 2021. All the functions are still there but require manual enabling. See issue 16994 of OpenSSL github project for details.

To quickly enable it, find the directory that holds your OpenSSL config file or a symlink to it, by running the below command:

```
openssl version -d
```

You can now go to the directory and edit the config file:

```
sudo vi openssl.cnf
```

Make sure that the config file contains following lines:

```
openssl_conf = openssl_init

[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
```

Uncomment what is needed to


## Requirements

System requirements

```
 sudo apt-get update
 sudo apt-get install libportaudio2 python3-pip
 sudo apt-get install python3-pyaudio
```

Install python dependencies

```
 pip3 install -r requirements.txt
```

 using qrcode[pil]

## openssl.cnf

check the directory

```
openssl version -d
```

You can now go to the directory and edit the config file (it may be necessary to use sudo):

vim openssl.cnf

Make sure that the config file contains following lines:
```
openssl_conf = openssl_init

[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
```

save and exit


## Syntax

 to be run on an offline clean computer only. For production use, a live distro like tails with internet connection down is mandatory. You can run the appimage file for this purpose.

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
  -e {mic,photo}, --Entropy {mic,photo}
                        Specify Entropy source. Choose mic or photo, default mic
  -w WRITE, --write WRITE
                        Specify the recipient public key to use for creating an gpg encrypted file with the Wallet

```

## Usage examples

 Generating a standard single address standalone paperwallet on the testnet. The Entropy is gathered from the mic noise.

```
$ ./papergen.py -t single -n testnet -d example_wallet -e photo

** WALLET JBOK/single **

{
    "name": "default",
    "network": "bitcoin mainnet",
    "private": "ee8601afe7d494313a347761ce5e98b185667864b61339e686f1535ec828aafe",
    "public": "039CD8DA342B74FDBEB649A9CD590E51261845030C71F6C822C731624770CF1902",
    "hash160": "dc6053c0872b832998bc6530778fc8eb923105dc",
    "WIF": "L5DNNfPBZe8n9Atf47MEsxbMqv4c7p4BCKnuc4xQrPFjzYtoaV6G",
    "p2pkh": "1M6F48bDSoLhx3VEK8pfYe687TUmVrsANX",
    "p2wpkh-ps2h": "3Hi93DkVZcDRiG8BzsQNHmNRKrE8kHwyyH",
    "p2wpkh": "bc1qm3s98sy89wpjnx9uv5c80r7gawfrzpwuswknzk"
}
QRCODES: Created    

```
 Generating a HD bip39 mnemonic 24words sequence. The Entropy is gathered from the mic noise.

```
$ ./papergen.py -t bip39 
Getting data from mic.. please wait
** WALLET HD Bip39 24 words mnemonic **

Generated Entropy 256bits
be1a9c39c2fdd4dce957508ecd660bb992be28cfa094318ae83e7573b461afcb

Single line output
finish train leader until evil mesh check brand correct bounce happy outdoor soft sting picnic unable photo sword candy that unfair inject change fiction

Json output
{
    "1": "finish",
    "2": "train",
    "3": "leader",
    "4": "until",
    "5": "evil",
    "6": "mesh",
    "7": "check",
    "8": "brand",
    "9": "correct",
    "10": "bounce",
    "11": "happy",
    "12": "outdoor",
    "13": "soft",
    "14": "sting",
    "15": "picnic",
    "16": "unable",
    "17": "photo",
    "18": "sword",
    "19": "candy",
    "20": "that",
    "21": "unfair",
    "22": "inject",
    "23": "change",
    "24": "fiction"
}

```

## Refs

 Please refer to https://www.massmux.com for more infos.

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND **NONINFINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

