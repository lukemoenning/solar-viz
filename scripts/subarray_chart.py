import altair as alt
import pandas as pd
import streamlit as st
import requests
import asyncio
import aiohttp
from aiohttp import BasicAuth
from requests.auth import HTTPBasicAuth

async def fetch_data(session, value_link, user, pw):
  async with session.get(value_link, auth=BasicAuth(user, pw)) as response:
    if response.status != 200:
      print("There was an error retrieving the data.")
      return
      
    json_data = await response.json()
    return value_link, json_data

async def subarrayChart(url, user, pw):
  response = requests.get(url, auth=HTTPBasicAuth(user, pw))
  
  if response.status_code != 200:
    st.write("Oops! Something went wrong. Please try again.")
    return
  
  data = response.json()
  items = data["Items"]
  value_links = []

  for item in items:
  # Iterate through each "value" in the current item
    value_links.append(item["Links"]["Value"])

  json_data_list = []
  
  async with aiohttp.ClientSession() as session:
    tasks = []
    for value_link in value_links:
        task = fetch_data(session, value_link, user, pw)
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    
    # Sort responses based on the original order of value_links
    sorted_responses = sorted(responses, key=lambda x: value_links.index(x[0]))

    # Extract the JSON data from the sorted responses
    json_data_list = [response[1] for response in sorted_responses]

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

  kWh_items = [item for item in extracted_data if "Name" in item and item["Name"] == "KWH Tag"]

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
  ).configure_axisX(labelAngle=0)

# Display the chart using Streamlit
  st.altair_chart(chart, use_container_width=True)  
  