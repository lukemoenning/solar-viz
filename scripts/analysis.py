import streamlit as st
import pandas as pd
import numpy as np

def analysis(analysis_page, user, pw):
  st.title("Analysis")
  
  # RETURN HOME BUTTON
  
  for _ in range(5):
    st.write(" ")
  home_columns = st.columns(2)
  with home_columns[0]:
    if st.button("Return Home"):
      analysis_page.empty()
      return