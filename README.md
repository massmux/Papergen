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

