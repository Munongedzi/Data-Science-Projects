# economic_data_app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time
from fredapi import Fred
from kaggle_secrets import UserSecretsClient

# Set up Streamlit
st.set_page_config(page_title="Economic Data Analysis", page_icon=":chart_with_upwards_trend:")

# Function to retrieve Fred API key
@st.cache(allow_output_mutation=True)
def get_fred_api_key():
    secrets = UserSecretsClient()
    return secrets.get_secret('fred-api')

# Function to create the Fred object
@st.cache(allow_output_mutation=True)
def create_fred_object():
    fred_key = get_fred_api_key()
    return Fred(api_key=fred_key)

# Function to plot S&P 500
def plot_sp500():
    st.subheader('S&P 500')
    sp500 = fred.get_series(series_id='SP500')
    st.line_chart(sp500)

# Function to plot Unemployment Rate by State
def plot_unemployment_rate_by_state():
    st.subheader('Unemployment Rate by State')
    st.plotly_chart(px.line(uemp_states))

# Function to plot Unemployment Rate by State for a specific date
def plot_unemployment_rate_by_state_date():
    st.subheader('Unemployment Rate by State - May 2020')
    selected_date = '2020-05-01'
    selected_data = uemp_states.loc[uemp_states.index == selected_date].T.sort_values(selected_date)
    st.bar_chart(selected_data[selected_date], width=700, height=1200)

# Function to plot Unemployment vs Participation for each state
def plot_unemployment_vs_participation():
    st.subheader('Unemployment vs Participation for Each State')
    fig, axs = plt.subplots(10, 5, figsize=(30, 30), sharex=True)
    axs = axs.flatten()

    i = 0
    for state in uemp_states.columns:
        if state in ["District Of Columbia", "Puerto Rico"]:
            continue
        ax2 = axs[i].twinx()
        uemp_states.query('index >= 2020 and index < 2022')[state].plot(ax=axs[i], label='Unemployment')
        part_states.query('index >= 2020 and index < 2022')[state].plot(ax=ax2, label='Participation', color='orange')
        ax2.grid(False)
        axs[i].set_title(state)
        i += 1

    st.pyplot(fig)

# Function to plot Unemployment and Participation for a specific state
def plot_unemployment_and_participation_for_state():
    st.subheader('Unemployment and Participation for a Specific State')
    selected_state = 'California'
    fig, ax = plt.subplots(figsize=(10, 5), sharex=True)
    ax2 = ax.twinx()
    uemp_states2 = uemp_states.asfreq('MS')
    uemp_states2.query('index >= 2020 and index < 2022')[selected_state].plot(ax=ax, label='Unemployment')
    part_states.dropna().query('index >= 2020 and index < 2022')[selected_state].plot(ax=ax2, label='Participation',
                                                                                       color='orange')
    ax2.grid(False)
    ax.set_title(selected_state)
    fig.legend(labels=['Unemployment', 'Participation'])
    st.pyplot(fig)

# Main Streamlit app
if __name__ == "__main__":
    st.title("Economic Data Analysis with Fred & Pandas")

    # Create the Fred object
    fred = create_fred_object()

    # 3. Pull Raw Data & Plot S&P 500
    plot_sp500()

    # 4. Pull and Join Multiple Data Series - Unemployment Rate by State
    unemp_df = fred.search('unemployment rate state', filter=('frequency', 'Monthly'))
    unemp_df = unemp_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')
    # ... (rest of the existing code)

    # 5. Display Unemployment Rate by State
    plot_unemployment_rate_by_state()

    # 6. Display Unemployment Rate by State for a specific date
    plot_unemployment_rate_by_state_date()

    # 7. Display Unemployment vs Participation for each state
    plot_unemployment_vs_participation()

    # 8. Display Unemployment and Participation for a specific state
    plot_unemployment_and_participation_for_state()
