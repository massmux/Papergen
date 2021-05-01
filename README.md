# Papergen

Bitcoin paperwallet generator by mic entropy or by webcam input

 generate a bitcoin paper wallet by gathering entropy from computer microphone. The script calculates the main addresses and shows results. It's important to run on an offline computer, better if with onthefly distro like tails. Network must be down so that no internet connection is active. The script does not need to be online for any purpose.

 Since true entropy from microphone is used, please be assured that your computer audio works, your microphone is active and works taking noise from the environment. Should microphone is off or not working, the entropy source would compromised and your resulting wallet would be not secure. For optimal result you should have a source of noise in front of microphone.

 If entropy from webcam is used, please be assured that your computer webcam works. Your webcam infact will take a certain amount of photos in order to get randomness. Should webcam is of or not working, the entropy source would be compromised and you resulting wallet would be not secure. For optimal result you should have the webcam pointed towards something moving fastly in front of it.

 It supports mainnet and testnet. It provides the following bitcoin address formats: p2pkh ; p2wpkh-p2sh ; p2wpkh

 - Added feature: now you can specify -d bip39 in order to get a true random generated HD wallet by 24 words sequence. In this case the network choice has no influece. A 24words bip39 HD mnemonic output is returned.

 - Added feature: now you can specify -e photo or -e mic in order to choose between webcam generated entropy or microphone generate entropy

 - Added feature: now you can specify the -w flag in order to choose a recipient key (gpg) to write an encrypted wallet file locally. This means that the wallet is created, shown on the monitor and written as an encrypted ascii file using the public key specified by the flag. The filename is the same as the wallet denomination

## Requirements

System requirements

```
 sudo apt-get update
 sudo apt-get install libportaudio2 python3-pip
```

Install python dependencies

```
 pip3 install -r requirements.txt
```

 using qrcode[pil]


## Syntax

 to be run on an offline clean computer only. Better using a live distro without internet connection

```
usage: papergen.py [-h] [-t {single,bip39}] [-n {mainnet,testnet}] [-d DENOMINATION] [-e {mic,photo}] [-w WRITE]

optional arguments:
  -h, --help            show this help message and exit
  -t {single,bip39}, --type {single,bip39}
                        Specify wallet type. Choose 'single' standalone address or 'bip39' HD(mnemonic), default single
  -n {mainnet,testnet}, --network {mainnet,testnet}
                        Specify network. Choose mainnet or testnet, default mainnet
  -d DENOMINATION, --denomination DENOMINATION
                        Specify a name for your wallet.
  -e {mic,photo}, --entropy {mic,photo}
                        Specify entropy source. Choose mic or photo, default mic
  -w WRITE, --write WRITE
                        Specify the recipient public key to use for creating an gpg encrypted file with the wallet

```

## Usage examples

 Generating a standard single address standalone paperwallet on the testnet. The entropy is gathered from the mic noise.

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
 Generating a HD bip39 mnemonic 24words sequence. The entropy is gathered from the mic noise.

```
$ ./papergen.py -t bip39

** WALLET HD Bip39 24 words mnemonic **

Generated entropy 256bits
63e58dd572818f4a28c5459b10ebece49e66127e6f0ba36518a8c860cd0774d7

Single line output
nothing olive athlete attitude fold road damage practice infant aerobic wrap attract example digital master bright business crunch cloth weasel auto detect grit media

Json output
{
    "1": "nothing",
    "2": "olive",
    "3": "athlete",
    "4": "attitude",
    "5": "fold",
    "6": "road",
    "7": "damage",
    "8": "practice",
    "9": "infant",
    "10": "aerobic",
    "11": "wrap",
    "12": "attract",
    "13": "example",
    "14": "digital",
    "15": "master",
    "16": "bright",
    "17": "business",
    "18": "crunch",
    "19": "cloth",
    "20": "weasel",
    "21": "auto",
    "22": "detect",
    "23": "grit",
    "24": "media"
}


```

## Refs

 Please refer to https://www.massmux.com for more infos.

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

