# papergen
Bitcoin paperwallet generator by mic entropy

 generate a bitcoin paper wallet by gathering entropy from computer microphone. The script calculates the main addresses and shows results. It's important to run on an offline computer, better if with onthefly distro like tails. Network must be down so that no internet connection is active. The script does not need to be online for any purpose.

 It supports mainnet and testnet. It provides the following bitcoin address formats: p2pkh ; p2wpkh-p2sh ; p2wpkh


## Requirements

```
 pip3 install -r requirements.txt

```
 using qrcode[pil]


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

