import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="SMU Greenfield Project",
    page_icon="🌿",
    layout="wide"
)

# -----------------------------
# GREEN THEME STYLE
# -----------------------------
st.markdown("""
<style>

.stApp {
    background-color: #eef7f1;
}

h1, h2, h3 {
    color: #1b5e20;
}

[data-testid="metric-container"] {
    background-color: #dcedc8;
    border-radius: 10px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER WITH LOGOS
# -----------------------------
col1, col2, col3 = st.columns([1,3,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=180)

with col2:
    st.markdown("<h1 style='text-align:center;'>SMU Scope 2 Emissions Dashboard</h1>", unsafe_allow_html=True)

with col3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.markdown("---")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("Scope 2 Emissions.xlsx")

# Clean data
df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"])

# -----------------------------
# KPIs
# -----------------------------
total_consumption = df["Consumption (kWh)"].sum()
avg_consumption = df["Consumption (kWh)"].mean()
meters = df["Reference of electric meter"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Electricity Consumption (kWh)", f"{total_consumption:,.0f}")
col2.metric("Average Consumption (kWh)", f"{avg_consumption:,.0f}")
col3.metric("Number of Meters", meters)

st.markdown("---")

# -----------------------------
# CONSUMPTION BY METER
# -----------------------------
st.subheader("Electricity Consumption by Meter")

meter_data = df.groupby("Reference of electric meter")["Consumption (kWh)"].sum()

st.bar_chart(meter_data)

# -----------------------------
# CONSUMPTION BY PERIOD
# -----------------------------
st.subheader("Electricity Consumption by Period")

period_data = df.groupby("Period")["Consumption (kWh)"].sum()

st.line_chart(period_data)

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("Dataset")

st.dataframe(df)

# -----------------------------
# EMISSION CALCULATION
# -----------------------------
st.subheader("Estimated Scope 2 Emissions")

emission_factor = st.slider(
    "Grid Emission Factor (kg CO2e / kWh)",
    0.1,
    1.0,
    0.55
)

emissions = total_consumption * emission_factor / 1000

st.metric("Estimated Emissions (tCO2e)", f"{emissions:,.2f}")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown(
"""
**South Mediterranean University – Carbon Accounting Dashboard 🌿**

Scope 2 emissions are calculated using electricity consumption and the grid emission factor.
"""
)
