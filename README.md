# Papergen
Bitcoin paperwallet generator by mic entropy

 generate a bitcoin paper wallet by gathering entropy from computer microphone. The script calculates the main addresses and shows results. It's important to run on an offline computer, better if with onthefly distro like tails. Network must be down so that no internet connection is active. The script does not need to be online for any purpose.

 Since true entropy from microphone is used, please be assured that your computer audio works, your microphone is active and works taking noise from the environment. Should microphone is off or not working, the entropy source would compromised and your resulting wallet would be not secure.

 It supports mainnet and testnet. It provides the following bitcoin address formats: p2pkh ; p2wpkh-p2sh ; p2wpkh

 Added feature: now you can specify -d bip39 in order to get a true random generated HD wallet by 24 words sequence. In this case the network choice has no influece. A 24words bip39 HD mnemonic output is returned.

 Added feature: now you can specify -e photo or -e mic in order to choose between webcam generated entropy or microphone generate entropy

## Standard install

```
 sudo apt-get install libportaudio2
 pip3 install -r requirements.txt

```
 then clone the repository and run the script

 using qrcode[pil]

## Install on tails

 for running on tails we minimized the requirements of software download with the lib/ directory included. This directory includes all the needed lib for the script to run. it should be placed at the following path

```
 ~/.local/lib/python3.8/site-packages/

```
 check the version of your python interpreter and correct in case the path above with correct version. In such a way there no dipendence to download and the script will be immediately ready to use on the tails distro.


## syntax

 to be run on an offline clean computer only. Better using a live distro like tails.

```
usage: papergen.py [-h] [-t {jbok,bip39}] [-n {mainnet,testnet}] [-d DENOMINATION] [-e {mic,photo}]

optional arguments:
  -h, --help            show this help message and exit
  -t {jbok,bip39}, --type {jbok,bip39}
                        Specify wallet type. Choose jbok (single standalone address) or bip39 HD(mnemonic), default JBOK
  -n {mainnet,testnet}, --network {mainnet,testnet}
                        Specify network. Choose mainnet or testnet for jbok type, default mainnet
  -d DENOMINATION, --denomination DENOMINATION
                        Specify a name for your wallet.
  -e {mic,photo}, --entropy {mic,photo}
                        Specify entropy source. Choose mic or photo, default mic


```

## Examples

 Generating a standard single address standalone paperwallet on the testnet. The entropy is gathered from the mic noise.

```
$ ./papergen.py -t jbok -n testnet -d example_wallet

** WALLET JBOK **

name        : example_wallet
network     : bitcoin testnet
private     : b7323b3ed16bcff0f2b709bfdc36d89e5a07e40312e47884ed2d7f9b8d655589
public      : 03CDEAE3E2229E7DE4D9D9A35230CD043179FA9B57D1F5E803D39CAA7014934961
hash160     : c27f8966f6b3dea80de797676baf8f188702fe31
WIF         : cTiozx2fiTPfxXn6Bh3Ht1UwFpTWeBVJr3XkqowqmRVK3TmcFmTz
p2pkh       : myFNAgBHtumF2GMisq1zepAq3jPYCkpwQo
p2wpkh-ps2h : 2N7vu7XyGUuRAkeRHN1LZB14fh57kwq4LRr
p2wpkh      : tb1qcflcjehkk002sr08jankhtu0rzrs9l33x8xrv6

QRCODES: Created     
```
 Generating a HD bip39 mnemonic 24words sequence. The entropy is gathered from the mic noise.

```
$ ./papergen.py -t bip39

** WALLET HD Bip39 24 words mnemonic **

[] Single line output
detail rail fruit utility nasty awful dismiss valve bridge tenant subject drop sudden chunk project baby honey melody misery fire name sail pill abstract

[] Numbered list output
           1: detail      
           2: rail        
           3: fruit       
           4: utility     
           5: nasty       
           6: awful       
           7: dismiss     
           8: valve       
           9: bridge      
          10: tenant      
          11: subject     
          12: drop        
          13: sudden      
          14: chunk       
          15: project     
          16: baby        
          17: honey       
          18: melody      
          19: misery      
          20: fire        
          21: name        
          22: sail        
          23: pill        
          24: abstract
```

## Refs

 Please refer to https://www.massmux.com for more infos.

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

