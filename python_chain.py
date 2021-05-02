import requests
import json
import pandas as pd

url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'

headers = { 
    'User-Agent' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
    'Upgrade-Insecure-Requests': "1",
    'Accept': "applicationjson, text/javascript, */*; q=0.01",
    'Accept-Language': "en-GB,en;q=0.5",
    'Accept-Encoding': "gzip, deflate, br",'DNT': "1"
}

cookies = {
    'bm_sv' : '3A8FFBF5409C04DC6D84B39EDFACC362~xQD33G0CZc7uMVaYCLmu6ywyOe8JBy7M3MV5oXanx62m3nKvijYB4NLbD2wxDgkZ8Q5j+JtNILBmVW5FO7j2MLPjj+j0p4Qsudo/EiYKrfUXebMbJDcwOi/j2Nx/VWCuRCj23qBZdXNU7X1rc3mEZU+otX36QVVDDCYhOJR6Ses=',
    'nseappid':	"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTYxOTkzNDMwMSwiZXhwIjoxNjE5OTM3OTAxfQ.rllVot8rOsivraGNC6e5-CA8ECdUzeXA_MHjS9qOKuM",
    'nsit': "DrveQOGzi0Z8hthvx2IDCcf6"
}


session = requests.session()

for cookie in cookies:
    if 'bm_sv' in cookie or 'nseappid' in cookie or 'nsit' in cookie:
        session.cookies.set(cookie, cookies[cookie])

data = session.get(url, headers=headers, timeout=25)
print(data.headers)
data = data.json()
with open("oidata.json", "w") as files:
    files.write(json.dumps(data, sort_keys=True))
#print(data.request_headers)

#df = pd.DataFrame().from_dict(data['records']['data'])
#print(df.tail())
#print(data.content)
#print("*", 50)

def fetch_oi(expiry_dt):
    ce_values = [data['CE'] for data in data['records']['data'] if "CE" in data and data['expiryDate'] == expiry_dt]
    pe_values = [data['PE'] for data in data['records']['data'] if "PE" in data and data['expiryDate'] == expiry_dt]

    ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])
    pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])
    
    print(ce_dt[['strikePrice','lastPrice']])
    print(pe_dt[['strikePrice','lastPrice']])


def main():
    
    expiry_dt = '06-May-2021'
    fetch_oi(expiry_dt)

if __name__ == '__main__':
    main()
