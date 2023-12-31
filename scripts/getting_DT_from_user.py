import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import altair as alt

def get_stream_id(solar_option):
    """
    Returns the stream ID for the specified solar option.
    """
    stream_ids = {
        "Cambus": "F1AbEAVYciAZHVU6DzQbJjxTxWwimrOBShT7hGiW-T9RdLVfgFiqSlzYXN1c8B8kKhkXr4ASVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEJVUyBCQVJOfERBSUxZIFRPVEFM",
        "Electric Vehicle Charging Station": "F1AbEAVYciAZHVU6DzQbJjxTxWwYTCY6CdT7hGiW-T9RdLVfg_XDEejkXN1c8B8kKhkXr4ASVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEVMRUNUUklDIFZFSElDTEUgQ0hBUkdJTkd8REFJTFkgVE9UQUw",
        "EV Charging Station": "F1AbEAVYciAZHVU6DzQbJjxTxWwYTCY6CdT7hGiW-T9RdLVfg_XDEejkXN1c8B8kKhkXr4ASVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEVMRUNUUklDIFZFSElDTEUgQ0hBUkdJTkd8REFJTFkgVE9UQUw",

    }
    return stream_ids.get(solar_option, None)

def get_json_for_dates(start_date, end_date, stream_id, username, password):
    """
    Retrieve JSON response for a given time range and stream ID.
    """
    base_url = 'https://itsnt2259.iowa.uiowa.edu/piwebapi/streams/'

    start_datetime = f'{start_date}T00:00:00'
    end_datetime = f'{end_date}T00:00:00'

    url = f'{base_url}{stream_id}/summary?starttime={start_datetime}&endtime={end_datetime}&summaryType=Total&summaryDuration=1d'

    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    
    if response.status_code != 200:
        st.write("Oops! Something went wrong. Please try again.")
        return
    
    return response.json()

def getting_DT_sum(response):
    """
    Calculate the total energy from the response.
    """
    if 'Items' in response:
        values = [item['Value']['Value'] for item in response['Items']]
        total_energy = sum(values)
        return total_energy
    else:
        return None

def getting_DT_from_user(username, password, start_date, end_date, solar_option):
    """
    Retrieve data and plot the daily energy production for the specified solar option.
    """
    if solar_option == "Cambus and EV Charging Station":
        cambus_stream_id = get_stream_id("Cambus")
        response_cambus = get_json_for_dates(start_date, end_date, cambus_stream_id, username, password)
        ev_stream_id = get_stream_id("Electric Vehicle Charging Station")
        response_ev = get_json_for_dates(start_date, end_date, ev_stream_id, username, password)

        # Process data for Cambus
        data_cambus = [{"Timestamp": item['Value']['Timestamp'], "Value": item['Value']['Value'], "SolarOption": "Cambus"} for item in response_cambus['Items']] if 'Items' in response_cambus else []
        # Process data for EV Charging Station
        data_ev = [{"Timestamp": item['Value']['Timestamp'], "Value": item['Value']['Value'], "SolarOption": "EV Charging Station"} for item in response_ev['Items']] if 'Items' in response_ev else []

        df = pd.DataFrame(data_cambus + data_ev)  # Combine data from both options into a single DataFrame

    else:
        if solar_option == "Electric Vehicle Charging Station":
            solar_option = "EV Charging Station"  # Rename solar_option if needed

        stream_id = get_stream_id(solar_option)
        response = get_json_for_dates(start_date, end_date, stream_id, username, password)

        if 'Items' in response:
            data = [{"Timestamp": item['Value']['Timestamp'], "Value": item['Value']['Value'], "SolarOption": solar_option} for item in response['Items']]
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame()


    with st.container():
        total_energy = df['Value'].sum()

        if not df.empty:
            # Plot the graph with points
            chart = alt.Chart(df).mark_line().encode(
                x=alt.X('Timestamp:T', axis=alt.Axis(title='Energy (kWh)', format='%Y-%m-%d %H:%M:%S')),
                y=alt.Y('Value:Q', axis=alt.Axis(title='Energy (kWh)')),
                color='SolarOption:N'
            ).properties(
                width=700,
                height=300,
                title= f'Daily Energy Production for {solar_option}'
            ) + alt.Chart(df).mark_circle(size=100).encode(
                x='Timestamp:T',
                y='Value:Q',
                tooltip=['Timestamp:T', 'Value:Q', 'SolarOption:N']
            )

            st.altair_chart(chart)  # Display Altair chart

    return df, total_energy
