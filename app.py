import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="SMU Scope 2 Carbon Dashboard", layout="wide")

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
    st.write("SMU Greenfield Project")

with col3:
    st.image("carbon_jar_logo (1).jfif", width=100)

st.divider()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("Scope 2 Emissions (1).csv")

    df["Consumption (kWh)"] = df["Consumption (kWh)"].astype(str)
    df["Consumption (kWh)"] = df["Consumption (kWh)"].str.replace(",", "")
    df["Consumption (kWh)"] = df["Consumption (kWh)"].str.replace(" ", "")
    df["Consumption (kWh)"] = df["Consumption (kWh)"].replace(["?", "nan", ""], np.nan)

    df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")

    df = df.dropna(subset=["Consumption (kWh)"])

    return df

df = load_data()

# ---------------------------------------------------
# MONTH ORDER (IMPORTANT FIX)
# ---------------------------------------------------
month_order = [
"Jan","Feb","Mar","Apr","May","Jun",
"Jul","Aug","Sep","Oct","Nov","Dec"
]

df["Period"] = pd.Categorical(df["Period"], categories=month_order, ordered=True)
df = df.sort_values("Period")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("Settings")

emission_factor = st.sidebar.slider(
    "Emission Factor (kg CO₂ / kWh)",
    0.1, 1.0, 0.55
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
c3.metric("Average Monthly Consumption", f"{avg_energy:,.0f}")

st.divider()

# ---------------------------------------------------
# ELECTRICITY TREND
# ---------------------------------------------------
st.subheader("Monthly Electricity Consumption")

electricity_chart = df.set_index("Period")["Consumption (kWh)"]
st.line_chart(electricity_chart)

# ---------------------------------------------------
# CO2 TREND
# ---------------------------------------------------
st.subheader("Monthly CO₂ Emissions")

emission_chart = df.set_index("Period")["CO2 Emissions (kg)"]
st.line_chart(emission_chart)

# ---------------------------------------------------
# METERS TREND
# ---------------------------------------------------
st.subheader("Number of Electricity Meters")

meter_chart = df.set_index("Period")["Number of meters"]
st.bar_chart(meter_chart)

# ---------------------------------------------------
# CONSUMPTION PER METER
# ---------------------------------------------------
st.subheader("Average Consumption per Meter")

df["Consumption per meter"] = df["Consumption (kWh)"] / df["Number of meters"]

meter_efficiency = df.set_index("Period")["Consumption per meter"]
st.bar_chart(meter_efficiency)

# ---------------------------------------------------
# EMISSION CONTRIBUTION
# ---------------------------------------------------
st.subheader("Monthly Contribution to Total Emissions")

df["Emission Share (%)"] = (df["CO2 Emissions (kg)"] / total_emissions) * 100

share_chart = df.set_index("Period")["Emission Share (%)"]
st.bar_chart(share_chart)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------
st.subheader("Dataset")

st.dataframe(df)
