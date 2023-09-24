import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import altair as alt
import csv
from scripts.getting_DT_from_user import getting_DT_from_user, get_json_for_dates, get_stream_id

def generate_solar_irradiance(solar_option, start_date, end_date):
    start_year, start_month, start_day = start_date.split('-')
    end_year, end_month, end_day = end_date.split('-')
    st.write(start_year, start_month, start_day)
    irradiances = []
    if solar_option == "Cambus":
        in_range = False
        with open('9degree_averages/9_degree_fixed_tilt.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if in_range:
                    if int(row[0]) <= int(end_year):
                        if int(row[1]) <= int(end_month):
                            if int(row[2]) <= int(end_day):
                                irradiances.append(row[3])
                        in_range = False
                elif int(row[0])==int(start_year):
                    if int(row[1])==int(start_month):
                        if int(row[2])==int(start_day):
                            in_range = True
                            irradiances.append(row[3])

    elif solar_option == "Electric Vehicle Charging Station":
        in_range = False
        with open('30degree_averages/30_degree_fixed_tilt.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if in_range:
                    if int(row[0]) <= int(end_year):
                        if int(row[1]) <= int(end_month):
                            if int(row[2]) <= int(end_day):
                                irradiances.append(row[3])
                        in_range = False
                elif int(row[0])==int(start_year):
                    if int(row[1])==int(start_month):
                        if int(row[2])==int(start_day):
                            in_range = True
                            irradiances.append(row[3])

    else:
        in_range = False
        with open('30degree_averages/30_degree_fixed_tilt.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if in_range:
                    if int(row[0]) <= int(end_year):
                        if int(row[1]) <= int(end_month):
                            if int(row[2]) <= int(end_day):
                                irradiances.append(row[3])
                        in_range = False
                elif int(row[0])==int(start_year):
                    if int(row[1])==int(start_month):
                        if int(row[2])==int(start_day):
                            in_range = True
                            irradiances.append(row[3])
    return irradiances


def calc_conversion_efficiency(solar_irradiance, solar_option, username, password, start_date, end_date):
    solar_area = {
        'Cambus': 180.0/10.7639, # area in m^2
        'EV Charging Station': 267.14/10.7639 # area in m^2
    }
    
    if solar_option == "Cambus":
        cambus_stream_id = get_stream_id("Cambus")
        response_cambus = get_json_for_dates(start_date, end_date, cambus_stream_id, username, password)
        data_cambus = [{"Timestamp": item['Value']['Timestamp'], "Value": item['Value']['Value'], "SolarOption": "Cambus"} for item in response_cambus['Items']]

        # Generate solar irradiance values based on data length
        num_values = len(data_cambus)
        # irradiance_step = (max(solar_irradiance) - min(solar_irradiance)) / num_values
        # solar_irradiance_values = generate_solar_irradiance(num_values, max(solar_irradiance), irradiance_step)

        df = pd.DataFrame(data_cambus)
        df['Conversion Efficiency'] = [value / (irradiance * solar_area['Cambus']) for value, irradiance in zip(df['Value'], solar_irradiance_values)]
    
    elif solar_option == "Electric Vehicle Charging Station":
        ev_stream_id = get_stream_id("Electric Vehicle Charging Station")
        response_ev = get_json_for_dates(start_date, end_date, ev_stream_id, username, password)
        data_ev = [{"Timestamp": item['Value']['Timestamp'], "Value": item['Value']['Value'], "SolarOption": "EV Charging Station"} for item in response_ev['Items']]
        
        # Generate solar irradiance values based on data length
        num_values = len(data_ev)
        irradiance_step = (max(solar_irradiance) - min(solar_irradiance)) / num_values
        solar_irradiance_values = generate_solar_irradiance(solar_option, start_date, end_date)

        df = pd.DataFrame(data_ev)
        df['Conversion Efficiency'] = [value / (irradiance * solar_area['EV Charging Station']) for value, irradiance in zip(df['Value'], solar_irradiance_values)]
    
    else:
        cambus_stream_id = get_stream_id("Cambus")
        response_cambus = get_json_for_dates(start_date, end_date, cambus_stream_id, username, password)
        ev_stream_id = get_stream_id("Electric Vehicle Charging Station")
        response_ev = get_json_for_dates(start_date, end_date, ev_stream_id, username, password)

        # Process data for Cambus
        data_cambus = [{"Timestamp": item['Value']['Timestamp'], "Value": item['Value']['Value'], "SolarOption": "Cambus"} for item in response_cambus['Items']] if 'Items' in response_cambus else []
        # Process data for EV Charging Station
        data_ev = [{"Timestamp": item['Value']['Timestamp'], "Value": item['Value']['Value'], "SolarOption": "EV Charging Station"} for item in response_ev['Items']] if 'Items' in response_ev else []

        df = pd.DataFrame(data_cambus + data_ev)  # Combine data from both options into a single DataFrame

        # Generate solar irradiance values based on data length
        num_values = len(df)
        irradiance_step = (max(solar_irradiance) - min(solar_irradiance)) / num_values
        solar_irradiance_values = generate_solar_irradiance(solar_option, start_date, end_date)

        # Calculate conversion efficiency for combined data
        df['Conversion Efficiency'] = [value / (irradiance * solar_area[df['SolarOption'].iloc[i]]) for i, (value, irradiance) in enumerate(zip(df['Value'], solar_irradiance_values))]
    return df

def main2(start_date, end_date, solar_option, username, password):
    # Define solar irradiance values
    initial_irradiance = 10.0  # Initial solar irradiance
    num_values = 10  # Adjust the number of values as needed
    solar_irradiance = generate_solar_irradiance(solar_option, start_date, end_date)

    # Calculate conversion efficiency
    df = calc_conversion_efficiency(solar_irradiance, solar_option, username, password, start_date, end_date)

    # # Set the domain for the x-axis to cover a larger range
    # x_domain = (
    #     pd.Timestamp(min(conversion_df['Timestamp'])) - pd.Timedelta(days=1),
    #     pd.Timestamp(max(conversion_df['Timestamp'])) + pd.Timedelta(days=1)
    # )
    # st.write(df)
    # st.write("Chart Configuration:")

    # Plot the conversion efficiency
    if not df.empty:
        conversion_chart = alt.Chart(df).mark_line().encode(
            x=alt.X('Timestamp:T', axis=alt.Axis(title='Energy (kWh)', format='%Y-%m-%d %H:%M:%S')),
            y=alt.Y('Conversion Efficiency:Q', axis=alt.Axis(title='Conversion Efficiency')),
            color='SolarOption:N',
            tooltip=['Timestamp:T', 'Conversion Efficiency:Q']
        ).properties(
            width=700,  # Set a fixed width
            height=300,  # Set a fixed height
            title=f'Conversion Efficiency for {solar_option}'
        ) + alt.Chart(df).mark_circle(size=100).encode(
            x='Timestamp:T',
            y='Conversion Efficiency:Q',
            tooltip=['Timestamp:T', 'Conversion Efficiency:Q']
        )

        st.altair_chart(conversion_chart)
