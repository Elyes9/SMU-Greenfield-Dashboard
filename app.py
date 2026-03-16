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
# HEADER WITH SMU LOGO
# --------------------------------------------------
col_logo, col_title = st.columns([1,5])

with col_logo:
    if os.path.exists("LOGO_SMU_2023_FINAL.png"):
        st.image("LOGO_SMU_2023_FINAL.png", width=130)

with col_title:
    st.title("SMU Greenfield Project")
    st.caption("Electricity consumption and emissions analysis – SMU")

st.markdown("---")

# --------------------------------------------------
# LOAD AND CLEAN DATA
# --------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("Scope 2 Emissions (2).csv")

    # Clean electricity column
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

    # Convert period to datetime
    df["Period"] = pd.to_datetime(df["Period"], format="%b-%y")

    # Sort months
    df = df.sort_values("Period")

    return df


df = load_data()

# --------------------------------------------------
# SIDEBAR CONTROLS
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
# EMISSIONS CALCULATION
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
# TIME SERIES CHARTS
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
# HISTOGRAMS
# --------------------------------------------------
st.subheader("Distribution Analysis")

col1, col2 = st.columns(2)

# Electricity Histogram
with col1:

    st.markdown("**Electricity Consumption Distribution**")

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

# Emissions Histogram
with col2:

    st.markdown("**CO₂ Emissions Distribution**")

    values = df["CO2 Emissions (kg)"].dropna()

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
st.subheader("Relationship Between Consumption and Emissions")

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
