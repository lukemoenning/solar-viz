import streamlit as st
import pandas as pd
import numpy as np
import asyncio
from scripts.steam_analysis import steamAnalysis
from scripts.subarray_chart import subarrayChart
from scripts.cost_graph import calculate_monthly_costs

def analysis(analysis_page, user, pw):
  st.title("In-Depth Analysis")
  
  baseURL = "https://itsnt2259.iowa.uiowa.edu/piwebapi/elements/"

  # Subarray Analysis
  st.header('Sub-Array Anomaly Analysis')
  st.write("Here, we look at the sub-arrays for the cambus/busbarn arrays and the electric vehicle charging arrays to understand how these subarrays are preforming in terms of power output. In both the arrays, there is one subarray that can be seen to underperform.")
  st.write("In the graphs below, the subarrays are the x-axis. The subarrays are laid out in the same order as given in the API, i.e. the leftmost point is the first subarray and the rightmost point the last sub array. The y-axis is power output.")
  
  for _ in range(2):
    st.write(" ")
  
  anomalyURL = baseURL + "F1EmAVYciAZHVU6DzQbJjxTxWwimrOBShT7hGiW-T9RdLVfgSVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEJVUyBCQVJO/elements"
  asyncio.run(subarrayChart(anomalyURL, user, pw))
  
  evURL = baseURL + "F1EmAVYciAZHVU6DzQbJjxTxWwYTCY6CdT7hGiW-T9RdLVfgSVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9OXEVMRUNUUklDIFZFSElDTEUgQ0hBUkdJTkc/elements"
  asyncio.run(subarrayChart(evURL, user, pw))
  
  for _ in range(3):
    st.write(" ")
  
  # Steam Analysis
  st.header('Solar Powered Campus Analysis')
  st.write("Most of the energy on campus is produced on the main powerplant along the Iowa River. The plant provides power mostly through steam, and the amount of steam power produced was given in the API. Using this data, we analyze how many square feet of each solar panel array are needed to replace the steam plant. The first graph displays the power output of the steam plant in MMBTU’s. Using standard conversions, we convert this unit to regular power units, and analyze how much square feet of solar arrays would be needed to replace the steam plant, and how much this would cost to install.")
  
  for _ in range(2):
    st.write(" ")
  
  steamAnalysis(user, pw)
  
  
  for _ in range(3):
    st.write(" ")
  
  # Payback Analysis
  st.header('Payback Analysis')
  st.write("Solar Panels have high installation costs but save money over time by not having to pay electric bills. Engie’s solar panels mean they don’t need to purchase any electricity from the MidAmerican Energy Company. Given that solar panels last for around 20 years, is the costs saved enough to offset the instillation costs?")
  st.write("The first graph shows the costs saved by a solar panel in a typical year, based on the rates MidAmerican Energy Company charges. The second graph visualizes the installation costs of both the Electric Vehicle and Cambus solar panels, and the third graph displays the amount of money saved in electric bills by each solar panel.")
  
  for _ in range(2):
    st.write(" ")
  
  start_date = (pd.Timestamp.today() - pd.Timedelta(days=365)).date()
  end_date = pd.Timestamp.today().date()
  calculate_monthly_costs(start_date, end_date, user, pw)
  
  
  # RETURN HOME BUTTON
  for _ in range(5):
    st.write(" ")
  home_columns = st.columns(2)
  with home_columns[0]:
    if st.button("Return Home"):
      analysis_page.empty()
      return