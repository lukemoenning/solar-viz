import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def displayChart():
  chart_container = st.empty()
  
  with chart_container.container():
    st.title("Data Comparison")
    
    columns = st.columns(2)
    date_options = ["Select a Start Date", "Select an End Date"]
    solar_options = ["Cambus", "Electric Vehicle Charging Station"]
    granuality_options = ["Hourly", "Daily", "Monthly"]
    
    with columns[0]:
      st.date_input(date_options[0])
      st.radio("Select a Granularity Option", granuality_options)
      
    with columns[1]:
      st.date_input(date_options[1])
      st.radio("Select a Solar Option", solar_options)
    
      
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    st.line_chart(chart_data)
    
    st.write("For more in-depth analysis, please visit")
      
    