import streamlit as st
import pandas as pd
import numpy as np

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="SMU Greenfield Project",
    page_icon="🌿",
    layout="wide"
)

# ----------------------------
# GREEN THEME
# ----------------------------
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
    border-radius: 12px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Scope 2 Emissions.csv")
    return df

df = load_data()

df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")

# ----------------------------
# HEADER WITH LOGOS
# ----------------------------
col1, col2, col3 = st.columns([1,3,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=170)

with col2:
    st.markdown(
        "<h1 style='text-align:center;'>SMU Scope 2 Carbon Dashboard</h1>",
        unsafe_allow_html=True
    )

with col3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.markdown("---")

# ----------------------------
# KPIs
# ----------------------------
total_consumption = df["Consumption (kWh)"].sum()
avg_consumption = df["Consumption (kWh)"].mean()
meters = df["Reference of electric meter"].nunique()

c1, c2, c3 = st.columns(3)

c1.metric("Total Electricity Consumption (kWh)", f"{total_consumption:,.0f}")
c2.metric("Average Consumption (kWh)", f"{avg_consumption:,.0f}")
c3.metric("Number of Electric Meters", meters)

st.markdown("---")

# ----------------------------
# BAR CHART
# ----------------------------
st.subheader("Electricity Consumption by Meter")

meter_data = df.groupby("Reference of electric meter")["Consumption (kWh)"].sum()

st.bar_chart(meter_data)

# ----------------------------
# LINE CHART
# ----------------------------
st.subheader("Electricity Consumption by Period")

period_data = df.groupby("Period")["Consumption (kWh)"].sum()

st.line_chart(period_data)

# ----------------------------
# EMISSION CALCULATOR
# ----------------------------
st.subheader("Scope 2 Emission Calculator")

emission_factor = st.slider(
    "Grid Emission Factor (kg CO₂e / kWh)",
    0.1,
    1.0,
    0.55
)

emissions = total_consumption * emission_factor / 1000

st.metric("Estimated Scope 2 Emissions (tCO₂e)", f"{emissions:,.2f}")

# ----------------------------
# DATA TABLE
# ----------------------------
st.subheader("Dataset")

st.dataframe(df)

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")

st.markdown(
"""
🌿 **South Mediterranean University – Carbon Accounting Dashboard**

This dashboard estimates Scope 2 emissions using electricity consumption data
and a configurable grid emission factor.
"""
)
