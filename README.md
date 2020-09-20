# Papergen
Bitcoin paperwallet generator by mic entropy

 generate a bitcoin paper wallet by gathering entropy from computer microphone. The script calculates the main addresses and shows results. It's important to run on an offline computer, better if with onthefly distro like tails. Network must be down so that no internet connection is active. The script does not need to be online for any purpose.

 Since true entropy from microphone is used, please be assured that your computer audio works, your microphone is active and works taking noise from the environment. Should microphone is off or not working, the entropy source would compromised and your resulting wallet would be not secure.

 It supports mainnet and testnet. It provides the following bitcoin address formats: p2pkh ; p2wpkh-p2sh ; p2wpkh


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
usage: papergen.py [-h] -n {mainnet,testnet}

optional arguments:
  -h, --help            show this help message and exit
  -n {mainnet,testnet}, --network {mainnet,testnet}
                        Specify network. Choose mainnet or testnet, default mainnet


```

## Refs

 Please refer to https://www.massmux.com for more infos.

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

