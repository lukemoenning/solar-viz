from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from scripts.login import login

def main(user, pw):
  st.title("Welcome to Solar Viz!")
  
  url = 'https://itsnt2259.iowa.uiowa.edu/piwebapi/elements/F1EmAVYciAZHVU6DzQbJjxTxWwCeQh1CdT7hGiW-T9RdLVfgSVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9O/elements'
  req = requests.get(url, auth=HTTPBasicAuth(user, pw))

  st.write(req.text)


if __name__ == "__main__":
  # login_result = login()
  # if login_result is not None:
  #     user, pw = login_result
  #     main(user, pw)
  
  
  # DO NOT COMMIT WITH CREDENTIALS
  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  # JUST FOR DEVELOPMENT PURPOSES
  user = ''
  pw = ''
  main(user, pw)