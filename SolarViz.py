from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from scripts.login import login
from scripts.intro import intro
from scripts.intial_url_to_other import get_json_from_string
from scripts.getting_DT_from_user import getting_DT_from_user
from scripts.charts import displayChart

import os
from dotenv import load_dotenv

def main(user, pw):
  st.title("Welcome to Solar Viz!")
    
  st.write(intro)
  
  start_date, end_date = displayChart(user,pw)

  # chart, total_energy = getting_DT_from_user(user, pw, start_date, end_date)
  # st.write("Total Energy:", total_energy)

  # st.write("Daily Energy Production:")
  # st.altair_chart(chart)



if __name__ == "__main__":
  # login_result = login()
  # if login_result is not None:
  #     user, pw = login_result
  #     main(user, pw)
  
  
  # JUST FOR DEVELOPMENT PURPOSES
  load_dotenv()
  user = os.getenv('USER')
  pw = os.getenv('PW')
  main(user, pw)