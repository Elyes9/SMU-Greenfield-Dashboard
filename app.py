import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="SMU Greenfield Project",
    layout="wide"
)

# --------------------------------------------------
# GREEN THEME
# --------------------------------------------------
st.markdown("""
<style>

.main {
background-color:#f4fff4;
}

h1,h2,h3{
color:#0f7d3e;
}

.kpi{
background-color:#e6f5ea;
padding:20px;
border-radius:12px;
text-align:center;
font-size:20px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER WITH LOGOS
# --------------------------------------------------
col1,col2,col3 = st.columns([1,3,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=140)

with col2:
    st.title("SMU Scope 2 Carbon Emissions Dashboard 🌱")

with col3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.markdown("---")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Scope 2 emissions.csv")
    return df

df = load_data()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("Dashboard Filters")

if "Building" in df.columns:
    building = st.sidebar.multiselect(
        "Select Building",
        df["Building"].unique(),
        default=df["Building"].unique()
    )

    df = df[df["Building"].isin(building)]

# --------------------------------------------------
# EMISSION FACTOR
# --------------------------------------------------
emission_factor = st.sidebar.slider(
    "Emission Factor (kg CO2 / kWh)",
    0.1,1.0,0.233
)

# --------------------------------------------------
# CALCULATE EMISSIONS
# --------------------------------------------------
if "Electricity Consumption (kWh)" in df.columns:
    df["CO2 Emissions (kg)"] = df["Electricity Consumption (kWh)"] * emission_factor

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
total_energy = df["Electricity Consumption (kWh)"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_energy = df["Electricity Consumption (kWh)"].mean()

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown(f'<div class="kpi">⚡ Total Electricity<br>{total_energy:,.0f} kWh</div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="kpi">🌍 Total CO₂ Emissions<br>{total_emissions:,.0f} kg</div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="kpi">📊 Average Consumption<br>{avg_energy:,.0f} kWh</div>', unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# ELECTRICITY CONSUMPTION CHART
# --------------------------------------------------
st.subheader("Electricity Consumption Over Time ⚡")

if "Date" in df.columns:
    energy_time = df.groupby("Date")["Electricity Consumption (kWh)"].sum()
    st.line_chart(energy_time)

# --------------------------------------------------
# CO2 EMISSIONS CHART
# --------------------------------------------------
st.subheader("CO₂ Emissions Over Time 🌍")

if "Date" in df.columns:
    emissions_time = df.groupby("Date")["CO2 Emissions (kg)"].sum()
    st.area_chart(emissions_time)

# --------------------------------------------------
# TOP ELECTRICITY METERS
# --------------------------------------------------
st.subheader("Top Electricity Meters 🔌")

if "Meter" in df.columns:
    meter_rank = df.groupby("Meter")["Electricity Consumption (kWh)"].sum()
    meter_rank = meter_rank.sort_values(ascending=False).head(10)

    st.bar_chart(meter_rank)

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------
st.subheader("Dataset Preview")
st.dataframe(df)
