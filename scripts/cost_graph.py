import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from scripts.getting_DT_from_user import get_json_for_dates, get_stream_id

def calculate_monthly_costs(start_date, end_date, solar_option, username, password):   
    # Define rates for different time intervals and months
    rates = {
        "June-September 6AM-6PM": 0.12,
        "June-September 6PM-6AM": 0.05,
        "October-May 6AM-6PM": 0.05,
        "October-May 6PM-6AM": 0.04,
        "Default": 0.10
    }

    # Mapping of month numbers to abbreviations
    month_abbreviations = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    # Get the JSON data based on the provided parameters
    stream_id = get_stream_id(solar_option)
    response = get_json_for_dates(start_date, end_date, stream_id, username, password)
    data = response.get('Items', [])

    # Initialize a dictionary to store the costs for each month
    monthly_costs_cambus = {month: 0 for month in range(1, 13)}
    monthly_costs_ev = {month: 0 for month in range(1, 13)}

    if solar_option == "Cambus":
        for item in data:
            timestamp = pd.to_datetime(item['Value']['Timestamp'])
            month = timestamp.month
            hour = timestamp.hour

            if 6 <= hour < 18:
                if 6 <= month <= 9:
                    monthly_costs_cambus[month] += item['Value']['Value'] * rates["June-September 6AM-6PM"]
                else:
                    monthly_costs_cambus[month] += item['Value']['Value'] * rates["October-May 6AM-6PM"]
            else:
                if 6 <= month <= 9:
                    monthly_costs_cambus[month] += item['Value']['Value'] * rates["June-September 6PM-6AM"]
                else:
                    monthly_costs_cambus[month] += item['Value']['Value'] * rates["October-May 6PM-6AM"]
    
    elif solar_option == "Electric Vehicle Charging Station":
        for item in data:
            timestamp = pd.to_datetime(item['Value']['Timestamp'])
            month = timestamp.month
            hour = timestamp.hour

            if 6 <= hour < 18:
                if 6 <= month <= 9:
                    monthly_costs_ev[month] += item['Value']['Value'] * rates["June-September 6AM-6PM"]
                else:
                    monthly_costs_ev[month] += item['Value']['Value'] * rates["October-May 6AM-6PM"]
            else:
                if 6 <= month <= 9:
                    monthly_costs_ev[month] += item['Value']['Value'] * rates["June-September 6PM-6AM"]
                else:
                    monthly_costs_ev[month] += item['Value']['Value'] * rates["October-May 6PM-6AM"]
    
    else:
        for item in data:
            timestamp = pd.to_datetime(item['Value']['Timestamp'])
            month = timestamp.month
            hour = timestamp.hour

            if 6 <= hour < 18:
                if 6 <= month <= 9:
                    monthly_costs_cambus[month] += item['Value']['Value'] * rates["June-September 6AM-6PM"]
                    monthly_costs_ev[month] += item['Value']['Value'] * rates["June-September 6AM-6PM"]
                else:
                    monthly_costs_cambus[month] += item['Value']['Value'] * rates["October-May 6AM-6PM"]
                    monthly_costs_ev[month] += item['Value']['Value'] * rates["October-May 6AM-6PM"]
            else:
                if 6 <= month <= 9:
                    monthly_costs_cambus[month] += item['Value']['Value'] * rates["June-September 6PM-6AM"]
                    monthly_costs_ev[month] += item['Value']['Value'] * rates["June-September 6PM-6AM"]
                else:
                    monthly_costs_cambus[month] += item['Value']['Value'] * rates["October-May 6PM-6AM"]
                    monthly_costs_ev[month] += item['Value']['Value'] * rates["October-May 6PM-6AM"]

    # Create a DataFrame for plotting
    monthly_costs_data_cambus = pd.DataFrame({
        "Month": [month_abbreviations[month] for month in monthly_costs_cambus.keys()],
        "Cost": list(monthly_costs_cambus.values()),
        "SolarOption": "Cambus"
    })

    monthly_costs_data_ev = pd.DataFrame({
        "Month": [month_abbreviations[month] for month in monthly_costs_ev.keys()],
        "Cost": list(monthly_costs_ev.values()),
        "SolarOption": "EV Charging Station"
    })

    # Concatenate the two DataFrames
    monthly_costs_data = pd.concat([monthly_costs_data_cambus, monthly_costs_data_ev])

    # Plot the costs using Altair
    chart = alt.Chart(monthly_costs_data).mark_bar().encode(
        x=alt.X('Month:O', axis=alt.Axis(title='Month')),
        y=alt.Y('Cost:Q', axis=alt.Axis(title='Cost ($/kWh)')),
        color='SolarOption:N',
    ).properties(
        width=700,
        height=300,
        title='Monthly Energy Costs'
    )

    st.write(chart)
    ##Start payback analysis
    instillation_cost_EV = 890479.6
    instillation_cost_cambus = 509531
    #Calculate yearly costs for each array
    yearly_costs_cambus = sum(monthly_costs_cambus.values())
    yearly_costs_ev = sum(monthly_costs_ev.values())
    #How much does each array save in 20 years
    save_cambus = 20 * yearly_costs_cambus
    save_ev = 20 * yearly_costs_ev
    #st.write(yearly_costs_cambus)
    #st.write(save_cambus)
    #st.write(monthly_costs_cambus)
    #Profits made from each array
    profit_cambus = save_cambus - instillation_cost_cambus
    profit_ev = save_ev - instillation_cost_EV
    # Create DataFrames for installation costs and savings
    installation_cost_data = pd.DataFrame({
        "Array": ["Cambus", "EV"],
        "Installation Cost": [instillation_cost_cambus, instillation_cost_EV]
    })

    savings_data = pd.DataFrame({
      "Array": ["Cambus", "EV"],
      "Savings in 20 Years": [save_cambus, save_ev]
    })

    # Create separate bar charts for installation costs and savings
    chart_installation_cost = alt.Chart(installation_cost_data).mark_bar().encode(
        x='Array:N',
        y='Installation Cost:Q',
        color='Array:N',
        tooltip=['Array', 'Installation Cost']
    ).properties(
      width=300,
     title='Installation Cost'
    )

    chart_savings = alt.Chart(savings_data).mark_bar().encode(
      x='Array:N',
      y='Savings in 20 Years:Q',
      color='Array:N',
      tooltip=['Array', 'Savings in 20 Years']
    ).properties(
      width=300,
      title='Savings in 20 Years'
    )

    # Display the installation cost and savings charts
    #st.write(yearly_costs_ev)
    st.write(chart_installation_cost, chart_savings)






    return chart, monthly_costs_data

