import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import altair as alt
from scripts.getting_DT_from_user import getting_DT_from_user, get_json_for_dates, get_stream_id

def generate_solar_irradiance(num_values, initial_irradiance, irradiance_step):
    irradiances =  [initial_irradiance - i * irradiance_step for i in range(num_values)][::-1]
    # st.write(irradiances)
    return irradiances

def calc_conversion_efficiency(solar_irradiance, solar_option, username, password, start_date, end_date):
    solar_area = {
        'Cambus': 180.0,
        'EV Charging Station': 237.14
    }

    if solar_option == "Cambus":
        cambus_stream_id = get_stream_id("Cambus")
        response_cambus = get_json_for_dates(start_date, end_date, cambus_stream_id, username, password)
        data_cambus = [{"Timestamp": item['Value']['Timestamp'], "Value": item['Value']['Value'], "SolarOption": "Cambus"} for item in response_cambus['Items']]

        # Generate solar irradiance values based on data length
        num_values = len(data_cambus)
        irradiance_step = (max(solar_irradiance) - min(solar_irradiance)) / num_values
        solar_irradiance_values = generate_solar_irradiance(num_values, max(solar_irradiance), irradiance_step)

        df = pd.DataFrame(data_cambus)
        df['Conversion Efficiency'] = [value / (irradiance * solar_area['Cambus']) for value, irradiance in zip(df['Value'], solar_irradiance_values)]
    
    elif solar_option == "EV Charging Station":
        # Complete this part
        return 0
    
    return df

def main2(start_date, end_date, solar_option, username, password):
    # Define solar irradiance values
    initial_irradiance = 10.0  # Initial solar irradiance
    num_values = 10  # Adjust the number of values as needed
    solar_irradiance = generate_solar_irradiance(num_values, initial_irradiance, 0.5)

    # Calculate conversion efficiency
    conversion_df = calc_conversion_efficiency(solar_irradiance, solar_option, username, password, start_date, end_date)

    # Plot the conversion efficiency
    if not conversion_df.empty:
        chart = alt.Chart(conversion_df).mark_line().encode(
            x=alt.X('Timestamp:T', title='Timestamp'),
            y=alt.Y('Conversion Efficiency', title='Conversion Efficiency'),
            tooltip=['Timestamp:T', 'Conversion Efficiency']
        ).properties(
            width=700,
            height=300,
            title=f'Conversion Efficiency for {solar_option}'
        )

        st.altair_chart(chart)  # Display Altair chart