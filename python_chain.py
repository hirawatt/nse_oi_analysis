import requests
import json
import pandas as pd
from pandas.io.json import build_table_schema

from glom import glom, T, Merge, Iter, Coalesce

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import graphviz as graphviz

# streamlit
st.set_page_config(page_title='Option Chain Analysis', page_icon=':shark:', layout='wide', initial_sidebar_state='expanded')
st.title('Option Chain Analysis')

# Variables
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


def fetch_oi(url):
    data = session.get(url, headers=headers, timeout=25)
    #st.write(data.headers)

    if data.status_code == 200:
        data = data.json()
        with open("oidata.json", "w") as files:
            files.write(json.dumps(data, sort_keys=True))
        st.success('Data Updated')
    else:
        data = pd.read_json('oidata.json')
        st.warning('Using Old Data')

    return data

def main():
    # NO DATA WIDGETS
    ticker = ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'HDFCBANK', 'RELIANCE', 'NMDC']
    script = st.sidebar.selectbox('Index to Trade?', ticker)

    # VARIABLES
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=' + script
    excel_file = 'option_chain_analysis.xlsx'

    # DATA
    data = fetch_oi(url)
    filtered = glom(data, 'filtered.data')
    cepeData = glom(data, 'records.data')
    ## Non-Nested Data
    strikePrices = glom(data, 'records.strikePrices')
    expiryDates = glom(data, 'records.expiryDates')
    spotPrice = glom(data, 'records.underlyingValue')
    lastUpdated = glom(data, 'records.timestamp')
    ## Nested Data
    


    # Ticker Information
    a1, a2, a3, a4 = st.beta_columns(4)
    a1.warning(script)
    a2.success('Spot Price : ' + str(spotPrice))
    a3.write('Last Updated : ' + str(lastUpdated))
    a4.write()

    # WIDGETS
    expiry = st.sidebar.selectbox('Expiry to Trade?', expiryDates)
    strikePrice = st.sidebar.slider('Select a range of Strike Prices', min(strikePrices), max(strikePrices), (min(strikePrices), max(strikePrices)))
    max_risk = st.sidebar.number_input('Maximum Risk', min_value=2000, max_value=50000, step=500)
    chosen = st.sidebar.radio('Options',("Call Buyer", "Call Seller", "Put Buyer", "Put Seller"))
    options_analysis = st.sidebar.multiselect('What data analysis do you want?', ['PCR', 'OI Change', 'Red', 'Blue'], ['PCR', 'OI Change'])

    # Dislpay Data
    oidata = pd.DataFrame.from_dict(pd.json_normalize(filtered), orient='columns')
    st.write('Latest Expiry', oidata)
    all_oidata = pd.DataFrame.from_dict(pd.json_normalize(cepeData), orient='columns')
    st.write('All Expiries', all_oidata)


if __name__ == '__main__':
    main()

# WIDGETS
left_column, right_column = st.beta_columns(2)
if right_column.button('Refresh', help='Click to Refresh Data'):
    main()
with left_column:
    LC = st.checkbox('Long Call')
    LP = st.checkbox('Long Put')
    SC = st.checkbox('Short Call')
    SP = st.checkbox('Short Put')

with st.beta_expander("See explanation"):
     st.write("""
              # Resources

     """)
