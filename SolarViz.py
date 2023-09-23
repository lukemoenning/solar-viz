from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from scripts.login import login
from scripts.intial_url_to_other import get_json_from_string
from scripts.getting_DT_from_user import getting_DT_from_user

import os
from dotenv import load_dotenv

def main(user, pw):
  st.title("Welcome to Solar Viz!")

  result = getting_DT_from_user(user, pw)
  st.write(result)



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