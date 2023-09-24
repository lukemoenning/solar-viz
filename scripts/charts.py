import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import altair as alt
from scripts.getting_DT_from_user import getting_DT_from_user
from scripts.conversion_efficiency import calc_conversion_efficiency, main2


def displayChart(username, password):
  chart_container = st.empty()

  with chart_container.container():
    st.title("Data Comparison")
    
    columns = st.columns(2)
    date_options = ["Select a Start Date", "Select an End Date"]
    solar_options = ["Cambus", "Electric Vehicle Charging Station", "Cambus and EV Charging Station"]
    granuality_options = ["Hourly", "Daily", "Monthly"]
    
    with columns[0]:
      default_start_date = datetime.today() - pd.Timedelta(days=7)
      start_date = st.date_input(date_options[0], value=default_start_date)
      granularity = st.radio("Select a Granularity Option", granuality_options)
      
    with columns[1]:
      default_end_date = datetime.today()
      end_date = st.date_input(date_options[1], value=default_end_date)
      solar_option = st.radio("Select a Solar Option", solar_options)
    
    for _ in range(3):
      st.write(" ")

    try:
      # Retrieve data
      chart_data, total_energy = getting_DT_from_user(username, password, start_date, end_date, solar_option)
      st.write("Total Energy:", total_energy)
    except:
      st.write("Oops! Something went wrong loading the data. Please try again.")


    try:
      main2(start_date, end_date, solar_option, username, password)
    except:
      st.write("Oops! Something went wrong loading the data. Please try again.")

    # try:
    #   main(start_date, end_date, solar_option, username, password)
    #   # conversion_chart =
    #   # st.write("Conversion Efficiency:", conversion_chart)
    # except:
    #   conversion_chart = chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    #   st.line_chart(conversion_chart)
    #   st.write("Conversion Efficiency:", conversion_chart)

  return start_date, end_date
      
    