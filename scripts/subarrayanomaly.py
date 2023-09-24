from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from scripts.login import login
from datetime import datetime

import os
from dotenv import load_dotenv







def main(user, pw):
  st.title("Welcome to Solar Viz!")

  #work on busburn
  #URL to just busbarn

  url = "https://itsnt2259.iowa.uiowa.edu/piwebapi/elements/F1EmAVYciAZHVU6DzQbJjxTxWwimrOBShT7hGiW-T9RdLVfgSVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEJVUyBCQVJO/elements"

  pw = os.getenv('PW')
  user = os.getenv('USER')

  # Make the GET request with authentication
  response = requests.get(url, auth=HTTPBasicAuth(user, pw))
  # Check if the request was successful (status code 200)
  if response.status_code == 200:
    # Parse the JSON response
    #st.write("wrote")
    # st.write(response.json())
    data = response.json()
    #st.write(data)
    
    items = data["Items"]
    value_links = []

    for item in items:
    # Iterate through each "value" in the current item
      value_links.append(item["Links"]["Value"])
    #st.write(value_links)

    json_data_list = []
    



    for value_link in value_links:
      response = requests.get(value_link, auth=HTTPBasicAuth(user, pw))
      if response.status_code == 200:
        json_data = response.json()  # Retrieve JSON content from the response
        json_data_list.append(json_data)
        #st.write("Working for link:", value_link)

    extracted_data = []



    # Now you can work with the json_data_list, which contains JSON data from all the links
    for json_data in json_data_list:
        # Do something with each JSON data object
               for item in json_data["Items"]:
                value_info = item.get("Value", {})  # Get the "Value" object if it exists
                units_abbreviation = value_info.get("UnitsAbbreviation", "")

                # Check if the "UnitsAbbreviation" is equal to "kW"
                if units_abbreviation == "kWh":
                    extracted_value = value_info.get("Value", None)
                    if extracted_value is not None:
                        extracted_data.append({
                            "Link": value_link,
                            "Name": item.get("Name", ""),
                            "Value": extracted_value
                        })


    #for item_data in extracted_data:
        #st.write("Link:", item_data["Link"])
        #st.write("Name:", item_data["Name"])
        #st.write("Value:", item_data["Value"])
    # Create a new list containing items with "kW" in UnitsAbbreviation
    # Create a new list containing items with "kW" or "kW" anywhere in UnitsAbbreviation
    # Create a new list containing items with "KWH Tag" in the "Name" field
    kWh_items = [item for item in extracted_data if "Name" in item and item["Name"] == "KWH Tag"]

    st.write("Sub-Array Anomaly Analysis for the busbarn solar arrays")
    st.write("This is a graph of all the busbarn subarrays, with the first sub array being the left-most 0 index, and each subsequent sub array follows.")


    #st.write(kWh_items)

  # Create a DataFrame from the extracted data
  df = pd.DataFrame(extracted_data)

  # Filter for items with "KWH Tag" in the "Name" column
  kWh_items = df[df['Name'] == 'KWH Tag']

  # Create a new column 'x' to manually space the data points
  kWh_items['x'] = range(len(kWh_items))

  # Create a line chart using Altair
  chart = alt.Chart(kWh_items).mark_line().encode(
      x=alt.X('x:O', title='Item'),  # 'x' represents the custom x-axis
      y=alt.Y('Value:Q', title='Value (kWh)')
  ).properties(
      width=800,  # Adjust the width of the chart as needed
      title='KWH Tag Values Over Time'  # Add a title to the chart
  ).configure_axisX(labelAngle=45)  # Rotate x-axis labels for better readability

# Display the chart using Streamlit
  st.altair_chart(chart, use_container_width=True)  

    
    




    







    

        







if __name__ == "__main__":
  load_dotenv()
  user = os.getenv('USER')
  pw = os.getenv('PW')
  main(user, pw)
    #if login():

   
