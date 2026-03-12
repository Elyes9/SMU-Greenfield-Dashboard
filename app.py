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

EMISSION_FACTOR = 0.42

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("Scope 2 Emissions (1).csv")

    df.columns = df.columns.str.strip()

    # Convert numeric columns
    df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")
    df["Number of meters"] = pd.to_numeric(df["Number of meters"], errors="coerce")

    # Fill missing values
    df["Consumption (kWh)"] = df["Consumption (kWh)"].fillna(0)
    df["Number of meters"] = df["Number of meters"].replace(0,1)

    # Month order
    months_order = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    df["Period"] = pd.Categorical(df["Period"], categories=months_order, ordered=True)

    df = df.sort_values("Period")

    # Calculate emissions
    df["CO2 Emissions (kg)"] = df["Consumption (kWh)"] * EMISSION_FACTOR

    # Consumption per meter
    df["Consumption per meter"] = df["Consumption (kWh)"] / df["Number of meters"]

    return df


df = load_data()

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------

total_consumption = df["Consumption (kWh)"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_meter_consumption = df["Consumption per meter"].mean()

c1, c2, c3 = st.columns(3)

c1.metric("Total Electricity Consumption (kWh)", f"{total_consumption:,.0f}")
c2.metric("Total CO₂ Emissions (kg)", f"{total_emissions:,.0f}")
c3.metric("Average Consumption per Meter (kWh)", f"{avg_meter_consumption:,.1f}")

st.markdown("---")

# ---------------------------------------------------
# MONTHLY CONSUMPTION
# ---------------------------------------------------

st.subheader("Monthly Electricity Consumption")

st.line_chart(
    df.set_index("Period")[["Consumption (kWh)"]]
)

# ---------------------------------------------------
# MONTHLY EMISSIONS
# ---------------------------------------------------

st.subheader("Monthly CO₂ Emissions")

st.bar_chart(
    df.set_index("Period")[["CO2 Emissions (kg)"]]
)

# ---------------------------------------------------
# NUMBER OF METERS
# ---------------------------------------------------

st.subheader("Number of Electricity Meters")

st.line_chart(
    df.set_index("Period")[["Number of meters"]]
)

# ---------------------------------------------------
# CONSUMPTION PER METER
# ---------------------------------------------------

st.subheader("Consumption per Meter")

st.bar_chart(
    df.set_index("Period")[["Consumption per meter"]]
)

# ---------------------------------------------------
# EMISSION SHARE
# ---------------------------------------------------

st.subheader("Monthly Share of Total Emissions")

df["Emission Share (%)"] = (df["CO2 Emissions (kg)"] / total_emissions) * 100

st.bar_chart(
    df.set_index("Period")[["Emission Share (%)"]]
)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

st.subheader("Dataset")

st.dataframe(df)
