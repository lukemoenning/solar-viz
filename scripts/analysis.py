import streamlit as st
import pandas as pd
import numpy as np

def analysis(analysis_page, user, pw):
  st.title("Analysis")
  
  # RETURN HOME BUTTON
  if st.button("Return Home"):
    analysis_page.empty()
    return