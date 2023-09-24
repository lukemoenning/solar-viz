import streamlit as st
import pandas as pd
import numpy as np
import asyncio
from scripts.subarray_chart import subarrayChart

def analysis(analysis_page, user, pw):
  st.title("Analysis")
  
  baseURL = "https://itsnt2259.iowa.uiowa.edu/piwebapi/elements/"
  
  # CAMBUS
  st.write("Sub-Array Anomaly Analysis for the busbarn solar arrays")
  st.write("This is a graph of all the busbarn subarrays, with the first sub array being the left-most 0 index, and each subsequent sub array follows.")
  anomalyURL = baseURL + "F1EmAVYciAZHVU6DzQbJjxTxWwimrOBShT7hGiW-T9RdLVfgSVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEJVUyBCQVJO/elements"
  asyncio.run(subarrayChart(anomalyURL, user, pw))
  
  # EV CHARGING
  st.write("Sub-Array Anomaly Analysis for the electric vehicle charging solar arrays")
  st.write("This is a graph of all the electric vehicle charging subarrays, with the first sub array being the left-most 0 index, and each subsequent sub array follows.")
  evURL = baseURL + "F1EmAVYciAZHVU6DzQbJjxTxWwYTCY6CdT7hGiW-T9RdLVfgSVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEVMRUNUUklDIFZFSElDTEUgQ0hBUkdJTkc/elements"
  asyncio.run(subarrayChart(evURL, user, pw))
  
  
  # RETURN HOME BUTTON
  for _ in range(5):
    st.write(" ")
  home_columns = st.columns(2)
  with home_columns[0]:
    if st.button("Return Home"):
      analysis_page.empty()
      return