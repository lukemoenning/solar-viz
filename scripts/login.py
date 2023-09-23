import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

def login():
  login_page = st.empty()
  
  with login_page.container():
    st.title("Solar Viz Login")
    username = st.text_input("Username", value="iowa\\")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
      if authenticate(username, password):
        st.success("Login Successful!")
        login_page.empty()
        return True
        
      else:
        st.error("Authentication failed. Please check your credentials.")
        return False
    
  
# Try to authenticate with the PI Web API
def authenticate(username, password):
  try: 
    url = 'https://itsnt2259.iowa.uiowa.edu/piwebapi/elements/F1EmAVYciAZHVU6DzQbJjxTxWwCeQh1CdT7hGiW-T9RdLVfgSVRTTlQyMjU5XFJZQU4gU0FOREJPWFxTT0xBUiBQUk9EVUNUSU9O/elements'
    req = requests.get(url, auth=HTTPBasicAuth(username, password))
    if req.status_code == 401:
      return False
    return True
  except Exception as error:
    print('Error in authentication: ' + error)
    
  return False