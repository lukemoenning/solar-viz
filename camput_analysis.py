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


  
  


url1 = 'https://itsnt2259.iowa.uiowa.edu/piwebapi/points?path=%5C%5Cpiserver.facilities.uiowa.edu%5CPP_Total_Campus_Steam_Delivered_MMBTU/HR'


pw = os.getenv('PW')
user = os.getenv('USER')
# Make the GET request with authentication
response = requests.get(url1, auth=HTTPBasicAuth(user, pw))

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

#st.write("JSON Response:", data)



# Extract RecordedData URL from the JSON response
recorded_data_url = data['Links']['RecordedData']

# Now, recorded_data_url contains the URL for RecordedData
#st.write("RecordedData URL:", recorded_data_url)



# Conversion factor from MMBTU per hour to kWh
conversion_factor = 293.071  # Conversion factor for natural gas (adjust as needed)

timestamps = []
mmBTU_per_hour_values = []
kWh_values = []
kW_values = []
Electrical_Array_Sq_Feet_values = []
Cambus_Array_Sq_Feet_values = []

# Make the GET request with authentication
response = requests.get(recorded_data_url, auth=HTTPBasicAuth(user, pw))

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Extract and parse through the list of timestamped values
    items = data.get("Items", [])
    
    # Initialize variables for calculating kW
    prev_timestamp = None
    prev_value = None
    
    for item in items:
        timestamp_str = item.get("Timestamp")
        mmBTU_per_hour = item.get("Value")
        
        # Convert the timestamp to a datetime object
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
        
        # Calculate the time duration in hours (for kW)
        if prev_timestamp is not None:
            time_duration_hours = (timestamp - prev_timestamp).total_seconds() / 3600
        else:
            # Set time_duration_hours to 0 for the first data point
            time_duration_hours = 0
        
        # Calculate kWh and kW
        kWh = mmBTU_per_hour * conversion_factor
        kW = kWh / time_duration_hours if time_duration_hours > 0 else 0
        Electrical_Array_Sq_Feet = (kW/49.5)/180
        Cambus_Array_Sq_Feet = (kW/38)/267.13
        
        # Display the timestamp, original value, kWh, and kW
        #st.write("Timestamp:", timestamp_str)
        #st.write("MMBTU per hour:", mmBTU_per_hour)
        #st.write("kWh:", kWh)
        #st.write("kW:", kW)
        #st.write("Electrical_Array_Sq_Feet:", Electrical_Array_Sq_Feet)
        #st.write("Cambus_Array_Sq_Feet:", Cambus_Array_Sq_Feet)

        timestamps.append(timestamp)  # Append timestamps here
        mmBTU_per_hour_values.append(mmBTU_per_hour)
        kWh_values.append(kWh)
        kW_values.append(kW)
        Electrical_Array_Sq_Feet_values.append(Electrical_Array_Sq_Feet)
        Cambus_Array_Sq_Feet_values.append(Cambus_Array_Sq_Feet)




        
        # Update previous timestamp and value for the next iteration
        prev_timestamp = timestamp
        prev_value = mmBTU_per_hour
 
      # Create a DataFrame from the collected data
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'MMBTU per hour': mmBTU_per_hour_values,
        'kWh': kWh_values,
        'kW': kW_values,
        'Electrical_Array_Sq_Feet': Electrical_Array_Sq_Feet_values,
        'Cambus_Array_Sq_Feet': Cambus_Array_Sq_Feet_values
    })



        # Create a line chart using Altair
    chart0 = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',  # Treat Timestamp as a time field
        y='MMBTU per hour:Q',  # kWh values on the y-axis (you can change this to other fields)
        color='MMBTU per hour:Q'  # Color the lines by kWh values (optional)
    ).properties(
        width=800  # Set the chart width
    )

    # Create a line chart using Altair
    chart = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',  # Treat Timestamp as a time field
        y='kWh:Q',  # kWh values on the y-axis (you can change this to other fields)
        color='kWh:Q'  # Color the lines by kWh values (optional)
    ).properties(
        width=800  # Set the chart width
    )

        # Create a line chart using Altair
    chart1 = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',  # Treat Timestamp as a time field
        y='kW:Q',  # kWh values on the y-axis (you can change this to other fields)
        color='kW:Q'  # Color the lines by kWh values (optional)
    ).properties(
        width=800  # Set the chart width
    )

            # Create a line chart using Altair
    chart2 = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',  # Treat Timestamp as a time field
        y='Electrical_Array_Sq_Feet:Q',  # kWh values on the y-axis (you can change this to other fields)
        color='Electrical_Array_Sq_Feet:Q'  # Color the lines by kWh values (optional)
    ).properties(
        width=800  # Set the chart width
    )

                # Create a line chart using Altair
    chart3 = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',  # Treat Timestamp as a time field
        y='Cambus_Array_Sq_Feet:Q',  # kWh values on the y-axis (you can change this to other fields)
        color='Cambus_Array_Sq_Feet:Q'  # Color the lines by kWh values (optional)
    ).properties(
        width=800  # Set the chart width
    )

    #cost of installing the equivilant amount of solar panels
    sum_list = sum(Electrical_Array_Sq_Feet_values)
    average_electrical = sum_list/len(Electrical_Array_Sq_Feet_values)
    sum_list1 = sum(Cambus_Array_Sq_Feet_values)
    average_cambus = sum_list1/len(Cambus_Array_Sq_Feet_values)

    cost1 = (average_electrical/180)*890479.6
    cost2 = (average_cambus/267.13)*509531



  

    # Display the chart in Streamlit
    st.altair_chart(chart0)
    st.altair_chart(chart)
    st.altair_chart(chart1)
    st.altair_chart(chart2)
    st.altair_chart(chart3)
    st.write("Predicted cost to replace steam plant with Electrical Vehicle Changing Array, without accounting for degradation")
    st.write(cost1)

    

    st.write("Predicted cost to replace steam plant with Cambus Array without accounting for degradation")
    st.write(cost2)
else:
    st.write("Error:", response.status_code)


if __name__ == "__main__":
  load_dotenv()
  user = os.getenv('USER')
  pw = os.getenv('PW')
  main(user, pw)
  #if login():

    
