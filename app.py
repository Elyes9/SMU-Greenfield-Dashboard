import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="SMU Greenfield Project",
    page_icon="🌿",
    layout="wide"
)

# ---------------------------------------------------
# SMU GREEN STYLE
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
background-color:#eef7f1;
}

h1{
color:#1b5e20;
}

h2{
color:#2e7d32;
}

[data-testid="metric-container"]{
background-color:#dcedc8;
border-radius:12px;
padding:15px;
border:1px solid #a5d6a7;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("Scope 2 Emissions.csv")
    return df

df = load_data()

df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")

# ---------------------------------------------------
# HEADER WITH LOGOS
# ---------------------------------------------------

c1,c2,c3 = st.columns([1,3,1])

with c1:
    st.image("LOGO_SMU_2023_FINAL.png", width=170)

with c2:
    st.markdown("<h1 style='text-align:center;'>SMU Carbon Accounting Dashboard</h1>", unsafe_allow_html=True)

with c3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.markdown("---")

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.title("Filters")

meter_filter = st.sidebar.multiselect(
    "Select Electric Meter",
    df["Reference of electric meter"].unique(),
    default=df["Reference of electric meter"].unique()
)

period_filter = st.sidebar.multiselect(
    "Select Period",
    df["Period"].unique(),
    default=df["Period"].unique()
)

df_filtered = df[
    (df["Reference of electric meter"].isin(meter_filter)) &
    (df["Period"].isin(period_filter))
]

# ---------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------

total_consumption = df_filtered["Consumption (kWh)"].sum()

avg_consumption = df_filtered["Consumption (kWh)"].mean()

meters = df_filtered["Reference of electric meter"].nunique()

emission_factor = 0.55

total_emissions = total_consumption * emission_factor / 1000

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

k1,k2,k3,k4 = st.columns(4)

k1.metric(
    "Total Electricity (kWh)",
    f"{total_consumption:,.0f}"
)

k2.metric(
    "Average Consumption",
    f"{avg_consumption:,.0f}"
)

k3.metric(
    "Active Meters",
    meters
)

k4.metric(
    "Estimated CO₂ (tCO₂e)",
    f"{total_emissions:,.2f}"
)

st.markdown("---")

# ---------------------------------------------------
# CONSUMPTION BY METER
# ---------------------------------------------------

st.subheader("Electricity Consumption by Meter")

meter_data = df_filtered.groupby(
    "Reference of electric meter"
)["Consumption (kWh)"].sum()

st.bar_chart(meter_data)

# ---------------------------------------------------
# CO2 EMISSIONS BY METER
# ---------------------------------------------------

st.subheader("CO₂ Emissions by Meter")

emissions_meter = meter_data * emission_factor / 1000

st.bar_chart(emissions_meter)

# ---------------------------------------------------
# TOP ENERGY CONSUMING METERS
# ---------------------------------------------------

st.subheader("Top Electricity Consuming Meters")

top_meters = meter_data.sort_values(ascending=False).head(5)

st.bar_chart(top_meters)

# ---------------------------------------------------
# ENERGY TREND
# ---------------------------------------------------

st.subheader("Electricity Consumption Trend")

period_data = df_filtered.groupby("Period")["Consumption (kWh)"].sum()

st.line_chart(period_data)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

st.subheader("Dataset")

st.dataframe(df_filtered)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown(
"""
🌿 **South Mediterranean University – Carbon Accounting Dashboard**

This dashboard visualizes electricity consumption and estimates **Scope 2 CO₂ emissions**
based on electricity purchased from the national grid.
"""
)
