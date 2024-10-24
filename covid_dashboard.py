import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page title
st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide")

# Title
st.title("COVID-19 Dashboard")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('WHO-COVID-19-Dataset-Final.csv')
    df['Date_reported'] = pd.to_datetime(df['Date_reported'])
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df['Date_reported'].min())
end_date = st.sidebar.date_input("End Date", df['Date_reported'].max())

# Filter data based on date range
filtered_df = df[(df['Date_reported'].dt.date >= start_date) & (df['Date_reported'].dt.date <= end_date)]

# Check if the filtered DataFrame is empty
if not filtered_df.empty:
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases", f"{filtered_df['Cumulative_cases'].max():,}")
    col2.metric("Total Deaths", f"{filtered_df['Cumulative_deaths'].max():,}")
    col3.metric("New Cases (Last Day)", f"{filtered_df['New_cases'].iloc[-1]:,}")
    col4.metric("New Deaths (Last Day)", f"{filtered_df['New_deaths'].iloc[-1]:,}")

    # Cumulative Cases and Deaths Chart
    st.subheader("Cumulative Cases and Deaths Over Time")
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=filtered_df['Date_reported'], y=filtered_df['Cumulative_cases'], name="Cumulative Cases"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=filtered_df['Date_reported'], y=filtered_df['Cumulative_deaths'], name="Cumulative Deaths"),
        secondary_y=True,
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Cases",
        yaxis2_title="Cumulative Deaths"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Daily New Cases and Deaths Chart
    st.subheader("Daily New Cases and Deaths")
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    fig2.add_trace(
        go.Bar(x=filtered_df['Date_reported'], y=filtered_df['New_cases'], name="New Cases"),
        secondary_y=False,
    )

    fig2.add_trace(
        go.Bar(x=filtered_df['Date_reported'], y=filtered_df['New_deaths'], name="New Deaths"),
        secondary_y=True,
    )

    fig2.update_layout(
        xaxis_title="Date",
        yaxis_title="New Cases",
        yaxis2_title="New Deaths",
        barmode='group'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Data Table
    st.subheader("Raw Data")
    st.dataframe(filtered_df)
else:
    st.warning("No data available for the selected date range.")