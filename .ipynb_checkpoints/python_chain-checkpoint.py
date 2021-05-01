import requests
import json

url = "https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"

def fetch_oi():
    r = requests.get(url).json()
    print(r)
    with open("oidata.json", "w") as files:
        files.write(json.dumps(r, indent=4, sort_keys=True))
def main():
    fetch_oi()

if __name__ == '__main__':
    main()
