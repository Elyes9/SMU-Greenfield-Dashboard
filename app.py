import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="SMU Scope 2 Carbon Dashboard", layout="wide")

# ---------------------------------------------------
# STYLE
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

    # Clean electricity consumption
    df["Consumption (kWh)"] = (
        df["Consumption (kWh)"]
        .astype(str)
        .str.replace(",", "")
        .str.replace(" ", "")
        .replace(["?", ""], np.nan)
    )

    df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")

    # Clean number of meters
    df["Number of meters"] = (
        df["Number of meters"]
        .astype(str)
        .str.replace(",", "")
        .str.replace(" ", "")
        .replace(["?", ""], np.nan)
    )

    df["Number of meters"] = pd.to_numeric(df["Number of meters"], errors="coerce")

    # Drop invalid rows
    df = df.dropna()

    return df


df = load_data()

# ---------------------------------------------------
# ORDER MONTHS CORRECTLY
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
# CALCULATIONS
# ---------------------------------------------------
df["CO2 Emissions (kg)"] = df["Consumption (kWh)"] * emission_factor

df["Consumption per meter"] = df["Consumption (kWh)"] / df["Number of meters"]

total_energy = df["Consumption (kWh)"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------
c1, c2, c3 = st.columns(3)

c1.metric("Total Electricity (kWh)", f"{total_energy:,.0f}")
c2.metric("Total CO₂ Emissions (kg)", f"{total_emissions:,.0f}")
c3.metric("Average Consumption per Meter", f"{df['Consumption per meter'].mean():,.2f}")

st.divider()

# ---------------------------------------------------
# ELECTRICITY TREND
# ---------------------------------------------------
st.subheader("Monthly Electricity Consumption")

electricity_chart = df.set_index("Period")[["Consumption (kWh)"]]
st.bar_chart(electricity_chart)

# ---------------------------------------------------
# CO2 EMISSIONS TREND
# ---------------------------------------------------
st.subheader("Monthly CO₂ Emissions")

co2_chart = df.set_index("Period")[["CO2 Emissions (kg)"]]
st.line_chart(co2_chart)

# ---------------------------------------------------
# NUMBER OF METERS
# ---------------------------------------------------
st.subheader("Electricity Meters Over Time")

meter_chart = df.set_index("Period")[["Number of meters"]]
st.line_chart(meter_chart)

# ---------------------------------------------------
# CONSUMPTION PER METER
# ---------------------------------------------------
st.subheader("Average Consumption per Meter")

efficiency_chart = df.set_index("Period")[["Consumption per meter"]]
st.bar_chart(efficiency_chart)

# ---------------------------------------------------
# EMISSION SHARE
# ---------------------------------------------------
st.subheader("Monthly Contribution to Total Emissions")

df["Emission Share (%)"] = (df["CO2 Emissions (kg)"] / total_emissions) * 100

share_chart = df.set_index("Period")[["Emission Share (%)"]]
st.bar_chart(share_chart)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------
st.subheader("Dataset")

st.dataframe(df)
