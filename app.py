import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="SMU Scope 2 Carbon Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# GREEN STYLE
# ---------------------------------------------------
st.markdown("""
<style>
.main {
background-color:#f4fbf4;
}

h1, h2, h3 {
color:#0a6e3d;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
col1, col2, col3 = st.columns([1,4,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=120)

with col2:
    st.title("SMU Scope 2 Carbon Emissions Dashboard")
    st.write("Greenfield Carbon Accounting Project")

with col3:
    st.image("carbon_jar_logo (1).jfif", width=100)

st.divider()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("Scope 2 Emissions (1).csv")

    # Convert everything to string first
    df["Consumption (kWh)"] = df["Consumption (kWh)"].astype(str)

    # Remove spaces and commas
    df["Consumption (kWh)"] = df["Consumption (kWh)"].str.replace(",", "")
    df["Consumption (kWh)"] = df["Consumption (kWh)"].str.replace(" ", "")

    # Replace invalid values
    df["Consumption (kWh)"] = df["Consumption (kWh)"].replace(["?", "nan", ""], np.nan)

    # Convert safely to numeric
    df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")

    # Remove rows with missing consumption
    df = df.dropna(subset=["Consumption (kWh)"])

    return df


df = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("Settings")

emission_factor = st.sidebar.slider(
    "Emission Factor (kg CO₂ / kWh)",
    0.1,
    1.0,
    0.55
)

# ---------------------------------------------------
# CALCULATE EMISSIONS
# ---------------------------------------------------
df["CO2 Emissions (kg)"] = df["Consumption (kWh)"] * emission_factor

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------
total_energy = df["Consumption (kWh)"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_energy = df["Consumption (kWh)"].mean()

c1, c2, c3 = st.columns(3)

c1.metric("Total Electricity (kWh)", f"{total_energy:,.0f}")
c2.metric("Total CO₂ Emissions (kg)", f"{total_emissions:,.0f}")
c3.metric("Average Consumption (kWh)", f"{avg_energy:,.0f}")

st.divider()

# ---------------------------------------------------
# ELECTRICITY CHART
# ---------------------------------------------------
st.subheader("Electricity Consumption by Period")

energy_chart = df.set_index("Period")["Consumption (kWh)"]

st.bar_chart(energy_chart)

# ---------------------------------------------------
# CO2 EMISSIONS CHART
# ---------------------------------------------------
st.subheader("CO₂ Emissions by Period")

emission_chart = df.set_index("Period")["CO2 Emissions (kg)"]

st.line_chart(emission_chart)

# ---------------------------------------------------
# METERS CHART
# ---------------------------------------------------
st.subheader("Number of Electricity Meters")

meter_chart = df.set_index("Period")["Number of meters"]

st.bar_chart(meter_chart)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------
st.subheader("Dataset")

st.dataframe(df)
