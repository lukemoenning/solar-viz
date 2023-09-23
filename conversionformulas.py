from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from scripts.login import login
from datetime import datetime


def main():
  st.title("Welcome to Solar Viz!")
  
##conversion for days

##link with json object that has convesrion effeciency at each time
url1 = 'https://itsnt2259.iowa.uiowa.edu/piwebapi/streams/F1AbEAVYciAZHVU6DzQbJjxTxWwimrOBShT7hGiW-T9RdLVfg_m58A6BxNVULugR7j2EabASVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEJVUyBCQVJOfEZMT1cgVEFH/summary?starttime=2011-06-01%2000:00:00&endtime=*&summaryType=Maximum&summaryDuration=1d'
pw1 = 'meghanaboobs1234'
user1 = 'mkasturirangan'

response = requests.get(url1, auth=HTTPBasicAuth(user1, pw1))

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    original_data = response.json()

#initialize new data
new_data = []

#Initialize variables for tracking day and value
current_day = 0
current_value = None

# Iterate through the original data
for item in original_data["Items"]:
    timestamp_str = item["Value"]["Timestamp"]
    timestamp = datetime.fromisoformat(timestamp_str)

    # Calculate the day difference from the first timestamp
    day_difference = (timestamp - datetime.fromisoformat(original_data["Items"][0]["Value"]["Timestamp"])).days

    # If a new day is reached, update the day and current value
    if day_difference > current_day:
        current_day = day_difference
        current_value = item["Value"]["Value"]

    # Append the data to the new list
    new_data.append({
        "Day": current_day,
        "Value": current_value,
        "UnitsAbbreviation": item["Value"]["UnitsAbbreviation"]
    })

#conversion 


if __name__ == "__main__":
  if login():
    main()