import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

def get_json_for_dates(start_date, end_date, username, password):
    base_url = 'https://itsnt2259.iowa.uiowa.edu/piwebapi/streams/'
    stream_id = 'F1AbEAVYciAZHVU6DzQbJjxTxWwimrOBShT7hGiW-T9RdLVfgFiqSlzYXN1c8B8kKhkXr4ASVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEJVUyBCQVJOfERBSUxZIFRPVEFM'

    start_datetime = f'{start_date} 00:00:00'
    end_datetime = f'{end_date} 00:00:00'

    start_url = f'{base_url}{stream_id}/summary?starttime={start_datetime}&summaryType=Maximum&summaryDuration=1d'
    end_url = f'{base_url}{stream_id}/summary?endtime={end_datetime}&summaryType=Maximum&summaryDuration=1d'

    # Retrieve JSON responses for both URLs
    start_response = requests.get(start_url, auth=HTTPBasicAuth(username, password)).json()
    end_response = requests.get(end_url, auth=HTTPBasicAuth(username, password)).json()

    return start_response, end_response

def getting_DT_from_user(username, password):
    DT_page = st.empty()
  
    with DT_page.container():
        st.title("Solar Viz Select Date")
        
        # Get start and end dates from the user
        start_date = st.date_input("Select a start date")
        end_date = st.date_input("Select an end date")
        
        # Display the selected start and end dates
        st.write("Start Date:", start_date)
        st.write("End Date:", end_date)

        # Fetch JSON responses for the specified dates
        start_response, end_response = get_json_for_dates(start_date, end_date, username, password)

        # Display JSON responses
        st.write("JSON response for start date:")
        st.write(start_response)

        st.write("JSON response for end date:")
        st.write(end_response)

if __name__ == "__main__":
    getting_DT_from_user()
