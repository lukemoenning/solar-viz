import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from scripts.getting_DT_from_user import get_json_for_dates, get_stream_id
from scripts.colors import getColors
    

def calculate_monthly_costs(start_date, end_date, username, password):   
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

    def buildCostDict(solar_option):
        res = {month: 0 for month in range(1, 13)}
        stream_id = get_stream_id(solar_option)
        data = get_json_for_dates(start_date, end_date, stream_id, username, password)
        
        items = data['Items'] if data else []
        
        for item in items:
            timestamp = pd.to_datetime(item['Value']['Timestamp'])
            month = timestamp.month
            hour = timestamp.hour

            if 6 <= hour < 18:
                if 6 <= month <= 9:
                    res[month] += item['Value']['Value'] * rates["June-September 6AM-6PM"]
                else:
                    res[month] += item['Value']['Value'] * rates["October-May 6AM-6PM"]
            else:
                if 6 <= month <= 9:
                    res[month] += item['Value']['Value'] * rates["June-September 6PM-6AM"]
                else:
                    res[month] += item['Value']['Value'] * rates["October-May 6PM-6AM"]
                    
        return res
    
    monthly_costs_cambus = buildCostDict("Cambus")
    monthly_costs_ev = buildCostDict("EV Charging Station")

    monthly_costs_data_cambus = pd.DataFrame({
        "Month": [month_abbreviations[month] for month in monthly_costs_cambus.keys()],
        "Cost": list(monthly_costs_cambus.values()),
        "SolarOption": "Cambus"
    })

    monthly_costs_data_ev = pd.DataFrame({
        "Month": [month_abbreviations[month] for month in monthly_costs_ev.keys()],
        "Cost": list(monthly_costs_ev.values()),
        "SolarOption": "EV"
    })
    
    custom_color_scale = getColors()

    cambus_cost_chart = alt.Chart(monthly_costs_data_cambus).mark_bar().encode(
        x=alt.X('Month:O', axis=alt.Axis(title='Month')),
        y=alt.Y('Cost:Q', axis=alt.Axis(title='Cost ($/kWh)')),
        color=alt.Color('SolarOption:N', scale=custom_color_scale),
    ).properties(
        width=700,
        height=300,
        title='Monthly Cambus Energy Costs'
    )
    
    ev_cost_chart = alt.Chart(monthly_costs_data_ev).mark_bar().encode(
        x=alt.X('Month:O', axis=alt.Axis(title='Month')),
        y=alt.Y('Cost:Q', axis=alt.Axis(title='Cost ($/kWh)')),
        color=alt.Color('SolarOption:N', scale=custom_color_scale),
    ).properties(
        width=700,
        height=300,
        title='Monthly EV Energy Costs'
    )
    
    
    instillation_cost_EV = 890479.6
    instillation_cost_cambus = 509531
    yearly_costs_cambus = sum(monthly_costs_cambus.values())
    yearly_costs_ev = sum(monthly_costs_ev.values())
    save_cambus = 20 * yearly_costs_cambus
    save_ev = 20 * yearly_costs_ev
    
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
        color=alt.Color('Array:N', scale=custom_color_scale),
        tooltip=['Array', 'Installation Cost']
    ).properties(
      width=300,
     title='Installation Cost'
    )

    chart_savings = alt.Chart(savings_data).mark_bar().encode(
      x='Array:N',
      y='Savings in 20 Years:Q',
      color=alt.Color('Array:N', scale=custom_color_scale),
      tooltip=['Array', 'Savings in 20 Years']
    ).properties(
      width=300,
      title='Savings in 20 Years'
    )
    
    st.write(cambus_cost_chart)
    st.write(ev_cost_chart) 
    
    cost_columns = st.columns(2)
    with cost_columns[0]:
        st.write(chart_installation_cost)

    with cost_columns[1]:
        st.write(chart_savings)
