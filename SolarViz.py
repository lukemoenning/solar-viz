from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from scripts.login import login

def main():
  st.title("Welcome to Solar Viz!")
  
  
  url = 'https://itsnt2259.iowa.uiowa.edu/piwebapi/elements/F1EmAVYciAZHVU6DzQbJjxTxWwCeQh1CdT7hGiW-T9RdLVfgSVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9O/elements'
  pw = ''
  user = ''
  req = requests.get(url, auth=HTTPBasicAuth(user, pw))

  st.write(req.text)


if __name__ == "__main__":
  if login():
    main()