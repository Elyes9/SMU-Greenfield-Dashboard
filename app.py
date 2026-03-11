import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="SMU Carbon Dashboard",
    layout="wide"
)

# -------------------------
# GREEN THEME STYLE
# -------------------------
st.markdown("""
<style>
.main {
    background-color:#f5fff5;
}
.kpi-card {
    background-color:#e8f5e9;
    padding:20px;
    border-radius:12px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# LOGOS
# -------------------------
col1, col2 = st.columns([1,6])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=120)

with col2:
    st.title("SMU Scope 2 Carbon Emissions Dashboard")
    st.write("Greenfield Carbon Accounting Project")

st.image("carbon_jar_logo (1).jfif", width=120)

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Scope 2 Emissions.csv")
    return df

df = load_data()

# -------------------------
# SIDEBAR FILTER
# -------------------------
st.sidebar.header("Filters")

buildings = st.sidebar.multiselect(
    "Select Building",
    df["Building"].unique(),
    default=df["Building"].unique()
)

df = df[df["Building"].isin(buildings)]

# -------------------------
# EMISSION FACTOR INPUT
# -------------------------
emission_factor = st.sidebar.number_input(
    "Emission Factor (kg CO2 / kWh)",
    value=0.55
)

# -------------------------
# EMISSION CALCULATION
# -------------------------
df["CO2 Emissions (kg)"] = df["Electricity_kWh"] * emission_factor

# -------------------------
# KPI CARDS
# -------------------------
total_energy = df["Electricity_kWh"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_energy = df["Electricity_kWh"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
    <h3>Total Electricity</h3>
    <h2>{total_energy:,.0f} kWh</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
    <h3>Total CO2 Emissions</h3>
    <h2>{total_emissions:,.0f} kg</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
    <h3>Average Electricity</h3>
    <h2>{avg_energy:,.0f} kWh</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -------------------------
# ENERGY BY BUILDING
# -------------------------
st.subheader("Electricity Consumption by Building")

energy_building = df.groupby("Building")["Electricity_kWh"].sum()

st.bar_chart(energy_building)

# -------------------------
# CO2 EMISSIONS BY BUILDING
# -------------------------
st.subheader("CO2 Emissions by Building")

emissions_building = df.groupby("Building")["CO2 Emissions (kg)"].sum()

st.bar_chart(emissions_building)

# -------------------------
# TOP ELECTRICITY METERS
# -------------------------
st.subheader("Top Electricity Meters")

top_meters = df.sort_values(
    "Electricity_kWh",
    ascending=False
).head(10)

st.dataframe(top_meters)

# -------------------------
# MONTHLY ELECTRICITY
# -------------------------
if "Month" in df.columns:

    st.subheader("Monthly Electricity Consumption")

    monthly = df.groupby("Month")["Electricity_kWh"].sum()

    st.line_chart(monthly)

# -------------------------
# DATA TABLE
# -------------------------
st.subheader("Dataset")

st.dataframe(df)
