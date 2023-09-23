import json
import requests
from requests.auth import HTTPBasicAuth

'''
taking the initial url, then getting the attributes link for each solar from the json

might not be needed anymore
'''
def get_json_from_string(url, user, pw):
    response = requests.get(url, auth=HTTPBasicAuth(user, pw)).json()

    list_of_attributes = []
    for i in response['Items']:
        # st.write(i)
        list_of_attributes.append((i['Links']['Attributes']))

    cambus_array = list_of_attributes[0]
    electric_vechile_charging = list_of_attributes[1]

    return cambus_array, electric_vechile_charging