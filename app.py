import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(page_title="SMU Scope 2 Dashboard", layout="wide")

# ---------------------------------------------------
# HEADER WITH LOGOS
# ---------------------------------------------------

col1, col2, col3 = st.columns([1,3,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=120)

with col2:
    st.title("SMU Greenfield Project")
   

with col3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.markdown("---")

# ---------------------------------------------------
# EMISSION FACTOR
# ---------------------------------------------------

EMISSION_FACTOR = 0.42   # kg CO2 per kWh

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("Scope 2 Emissions (1).csv")

    df.columns = df.columns.str.strip()

    # Convert numbers safely
    df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")
    df["Number of meters"] = pd.to_numeric(df["Number of meters"], errors="coerce")

    # Replace missing
    df["Consumption (kWh)"] = df["Consumption (kWh)"].fillna(0)
    df["Number of meters"] = df["Number of meters"].replace(0,1)

    # Months order
    months_order = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    df["Period"] = pd.Categorical(df["Period"], categories=months_order, ordered=True)

    # Emissions
    df["CO2 Emissions (kg)"] = df["Consumption (kWh)"] * EMISSION_FACTOR

    # Consumption per meter
    df["Consumption per meter"] = df["Consumption (kWh)"] / df["Number of meters"]

    return df


df = load_data()

# ---------------------------------------------------
# SIDEBAR FILTER
# ---------------------------------------------------

st.sidebar.header("Filters")

building_filter = st.sidebar.multiselect(
    "Select Building",
    df["Building"].unique(),
    default=df["Building"].unique()
)

df = df[df["Building"].isin(building_filter)]

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------

total_consumption = df["Consumption (kWh)"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_consumption = df["Consumption per meter"].mean()

c1, c2, c3 = st.columns(3)

c1.metric("Total Electricity Consumption (kWh)", f"{total_consumption:,.0f}")
c2.metric("Total CO₂ Emissions (kg)", f"{total_emissions:,.0f}")
c3.metric("Average Consumption per Meter (kWh)", f"{avg_consumption:,.1f}")

st.markdown("---")

# ---------------------------------------------------
# MONTHLY CONSUMPTION
# ---------------------------------------------------

st.subheader("Monthly Electricity Consumption")

monthly = df.groupby("Period")["Consumption (kWh)"].sum().reset_index()

st.line_chart(monthly.set_index("Period"))

# ---------------------------------------------------
# MONTHLY EMISSIONS
# ---------------------------------------------------

st.subheader("Monthly CO₂ Emissions")

monthly_emissions = df.groupby("Period")["CO2 Emissions (kg)"].sum().reset_index()

st.bar_chart(monthly_emissions.set_index("Period"))

# ---------------------------------------------------
# BUILDING CONSUMPTION
# ---------------------------------------------------

st.subheader("Electricity Consumption by Building")

building_consumption = df.groupby("Building")["Consumption (kWh)"].sum()

st.bar_chart(building_consumption)

# ---------------------------------------------------
# TOP ELECTRICITY METERS
# ---------------------------------------------------

st.subheader("Top Electricity Meters by Consumption")

top_meters = df.sort_values("Consumption (kWh)", ascending=False).head(10)

st.dataframe(
    top_meters[[
        "Building",
        "Meter",
        "Consumption (kWh)",
        "CO2 Emissions (kg)"
    ]]
)

# ---------------------------------------------------
# CONSUMPTION PER METER
# ---------------------------------------------------

st.subheader("Consumption per Meter")

meter_consumption = df.groupby("Meter")["Consumption per meter"].mean()

st.bar_chart(meter_consumption)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

st.subheader("Dataset")

st.dataframe(df)
