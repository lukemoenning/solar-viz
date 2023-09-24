from collections import namedtuple
import altair as alt
import pandas as pd
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from scripts.login import login
from datetime import datetime


def steamAnalysis(user, pw):
    url = 'https://itsnt2259.iowa.uiowa.edu/piwebapi/points?path=%5C%5Cpiserver.facilities.uiowa.edu%5CPP_Total_Campus_Steam_Delivered_MMBTU/HR'

    response = requests.get(url, auth=HTTPBasicAuth(user, pw))

    if response.status_code != 200:
        st.write("Oops! Something went wrong. Please try again.")
        return
    
    data = response.json()
    recorded_data_url = data['Links']['RecordedData']

    # Conversion factor from MMBTU per hour to kWh
    conversion_factor = 293.071  # Conversion factor for natural gas (adjust as needed)

    timestamps = []
    mmBTU_per_hour_values = []
    kWh_values = []
    kW_values = []
    ev_sqft_values = []
    cambus_sqft_values = []

    # Make the GET request with authentication
    response = requests.get(recorded_data_url, auth=HTTPBasicAuth(user, pw))

    if response.status_code != 200:
        st.write("Oops! Something went wrong. Please try again.")
        return
    
    data = response.json()
    items = data.get("Items", [])
    prev_timestamp = None
    
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
        curr_ev_sqft = (kW/49.5)/180
        curr_cambus_sqft = (kW/38)/267.13

        timestamps.append(timestamp)  
        mmBTU_per_hour_values.append(mmBTU_per_hour)
        kWh_values.append(kWh)
        kW_values.append(kW)
        ev_sqft_values.append(curr_ev_sqft)
        cambus_sqft_values.append(curr_cambus_sqft)

        prev_timestamp = timestamp

    # Create a DataFrame from the collected data
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'MMBTU per hour': mmBTU_per_hour_values,
        'kWh': kWh_values,
        'kW': kW_values,
        'EV Array Square Feet': ev_sqft_values,
        'Cambus Array Square Feet': cambus_sqft_values
    })

    ev_sqft_chart = alt.Chart(df).mark_line().encode(
        x='Timestamp:T',  
        y='EV Array Square Feet:Q',  
        color='EV Array Square Feet:Q'  
    ).properties(
        width=800 
    )

    cambus_sqft_chart = alt.Chart(df).mark_line().encode(
        x='Timestamp:T', 
        y='Cambus Array Square Feet:Q', 
        color='Cambus Array Square Feet:Q'  
    ).properties(
        width=800 
    )
    
    cambus_surface_area = 267.13
    cambus_installation_cost = 509531
    cambus_sum = sum(cambus_sqft_values)
    cambus_average = cambus_sum/len(cambus_sqft_values)
    cambus_cost = (cambus_average/cambus_surface_area)*cambus_installation_cost
    formatted_cambus_cost = f'${cambus_cost:,.2f}'
    st.altair_chart(cambus_sqft_chart)
    st.write("Predicted cost to replace steam plant with Cambus Array without accounting for degradation: ", formatted_cambus_cost)
    
    ev_sum = sum(ev_sqft_values)
    ev_average = ev_sum/len(ev_sqft_values)
    ev_surface_area = 180
    ev_installation_cost = 890479.6
    ev_cost = (ev_average/ev_surface_area)*ev_installation_cost
    formatted_ev_cost = f'${ev_cost:,.2f}'
    st.altair_chart(ev_sqft_chart)
    st.write("Predicted cost to replace steam plant with Electrical Vehicle Changing Array, without accounting for degradation: ", formatted_ev_cost)
