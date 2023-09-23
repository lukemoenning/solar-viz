import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import altair as alt

'''
these functions are being used to 
'''
def get_json_for_dates(start_date, end_date, username, password):
    base_url = 'https://itsnt2259.iowa.uiowa.edu/piwebapi/streams/'
    stream_id = 'F1AbEAVYciAZHVU6DzQbJjxTxWwimrOBShT7hGiW-T9RdLVfgFiqSlzYXN1c8B8kKhkXr4ASVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEJVUyBCQVJOfERBSUxZIFRPVEFM'

    start_datetime = f'{start_date}T05:00:00'
    end_datetime = f'{end_date}T05:00:00'

    url = f'{base_url}{stream_id}/summary?starttime={start_datetime}&endtime={end_datetime}&summaryType=Total&summaryDuration=1d'

    # Retrieve JSON response for the URL
    response = requests.get(url, auth=HTTPBasicAuth(username, password)).json()

    return response

def getting_DT_sum(response):
    if 'Items' in response:
        values = [item['Value']['Value'] for item in response['Items']]
        total_energy = sum(values)
        return total_energy
    else:
        return None

def getting_DT_from_user(username, password, start_date, end_date):
    DT_page = st.empty()
    
    with DT_page.container():

        # Fetch JSON response for the specified dates
        response = get_json_for_dates(start_date, end_date, username, password)

        # Calculate the sum of values
        total_energy = getting_DT_sum(response)

        # Extract data for plotting
        if 'Items' in response:
            data = [{"Timestamp": item['Value']['Timestamp'], "Value": item['Value']['Value']} for item in response['Items']]
            df = pd.DataFrame(data)

            # Center the chart
            # st.write("Daily Energy Production:")
            # st.write(df)  # Display DataFrame

            # Plot the graph with points
            chart = alt.Chart(df).mark_line().encode(
                x=alt.X('Timestamp:T', scale=alt.Scale(domain=(pd.Timestamp(df['Timestamp'].min()) - pd.Timedelta(days=1), pd.Timestamp(df['Timestamp'].max()) + pd.Timedelta(days=1)))),
                y=alt.Y('Value:Q', axis=alt.Axis(title='Energy (kWh)'))
            ).properties(
                width=700, 
                height=300,
                title='Daily Energy Production'
            ) + alt.Chart(df).mark_circle(size=100).encode(
                x='Timestamp:T',
                y='Value:Q',
                tooltip=['Timestamp:T', 'Value:Q']
            )

            st.altair_chart(chart)  # Display Altair chart

        # Return the DataFrame and total energy
        return chart, total_energy
