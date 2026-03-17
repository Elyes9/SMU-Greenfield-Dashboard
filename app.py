import streamlit as st
import pandas as pd
import numpy as np
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="SMU Scope 2 Emissions Dashboard",
    layout="wide"
)

# --------------------------------------------------
# HEADER WITH LOGOS
# --------------------------------------------------
col_logo1, col_title, col_logo2 = st.columns([1,4,1])

with col_logo1:
    if os.path.exists("LOGO_SMU_2023_FINAL.png"):
        st.image("LOGO_SMU_2023_FINAL.png", width=120)

with col_title:
    st.title("Scope 2 Carbon Emissions Dashboard")
    st.caption("Electricity consumption and emissions analysis")

with col_logo2:
    if os.path.exists("carbon_jar_logo (1).jfif"):
        st.image("carbon_jar_logo (1).jfif", width=120)

st.markdown("---")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("Scope 2 Emissions (2).csv")

    # Clean electricity values
    df["Consumption (kWh)"] = (
        df["Consumption (kWh)"]
        .astype(str)
        .str.replace(" ", "")
        .str.replace(",", "")
        .replace("?", np.nan)
    )

    df["Consumption (kWh)"] = pd.to_numeric(
        df["Consumption (kWh)"],
        errors="coerce"
    )

    # Convert Period to datetime
    df["Period"] = pd.to_datetime(df["Period"], format="%b-%y")

    # Sort months
    df = df.sort_values("Period")

    return df


df = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.header("Dashboard Controls")

emission_factor = st.sidebar.slider(
    "Emission Factor (kg CO₂ / kWh)",
    0.1,
    1.0,
    0.45,
    0.05
)

# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------
df["CO2 Emissions (kg)"] = df["Consumption (kWh)"] * emission_factor

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------
st.subheader("Key Indicators")

total_consumption = df["Consumption (kWh)"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_consumption = df["Consumption (kWh)"].mean()

k1, k2, k3 = st.columns(3)

k1.metric(
    "Total Electricity Consumption",
    f"{total_consumption:,.0f} kWh"
)

k2.metric(
    "Total CO₂ Emissions",
    f"{total_emissions:,.0f} kg"
)

k3.metric(
    "Average Monthly Consumption",
    f"{avg_consumption:,.0f} kWh"
)

st.markdown("---")

# --------------------------------------------------
# TREND CHARTS
# --------------------------------------------------
st.subheader("Monthly Trends")

c1, c2 = st.columns(2)

with c1:

    st.markdown("**Electricity Consumption (kWh)**")

    electricity = df.set_index("Period")["Consumption (kWh)"]

    st.line_chart(electricity)

with c2:

    st.markdown("**CO₂ Emissions (kg)**")

    emissions = df.set_index("Period")["CO2 Emissions (kg)"]

    st.line_chart(emissions)

st.markdown("---")

# --------------------------------------------------
# ELECTRICITY HISTOGRAM
# --------------------------------------------------
st.subheader("Electricity Consumption Distribution")

values = df["Consumption (kWh)"].dropna()

hist, bins = np.histogram(values, bins=7)

labels = [
    f"{int(bins[i])}-{int(bins[i+1])}"
    for i in range(len(hist))
]

hist_df = pd.DataFrame({
    "Range": labels,
    "Frequency": hist
}).set_index("Range")

st.bar_chart(hist_df)

st.markdown("---")


# --------------------------------------------------
# SCATTER RELATIONSHIP
# --------------------------------------------------
st.subheader("Electricity Consumption vs CO₂ Emissions")

scatter_data = df[[
    "Consumption (kWh)",
    "CO2 Emissions (kg)"
]].dropna()

st.scatter_chart(scatter_data)

st.markdown("---")

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------
st.subheader("Clean Dataset")

st.dataframe(df, use_container_width=True)
