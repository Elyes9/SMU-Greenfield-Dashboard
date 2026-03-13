import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Scope 2 Emissions Dashboard", layout="wide")

st.title("🌍 Scope 2 Carbon Emissions Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Scope 2 Emissions (1).csv")

    # Clean consumption column
    df["Consumption (kWh)"] = (
        df["Consumption (kWh)"]
        .astype(str)
        .str.replace(" ", "")
        .replace("?", np.nan)
    )

    df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")

    # Convert Period to datetime for correct sorting
    df["Period"] = pd.to_datetime(df["Period"], format="%b-%y")

    # Sort months correctly
    df = df.sort_values("Period")

    return df

df = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Dashboard Controls")

emission_factor = st.sidebar.slider(
    "Emission Factor (kg CO₂ per kWh)",
    min_value=0.1,
    max_value=1.0,
    value=0.45,
    step=0.05
)

# -----------------------------
# CALCULATE EMISSIONS
# -----------------------------
df["CO2 Emissions (kg)"] = df["Consumption (kWh)"] * emission_factor

# -----------------------------
# KPI METRICS
# -----------------------------
total_consumption = df["Consumption (kWh)"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_emissions = df["CO2 Emissions (kg)"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("⚡ Total Electricity (kWh)", f"{total_consumption:,.0f}")
col2.metric("🌍 Total CO₂ Emissions (kg)", f"{total_emissions:,.0f}")
col3.metric("📊 Average Monthly CO₂ (kg)", f"{avg_emissions:,.0f}")

st.divider()

# -----------------------------
# PREPARE DATA FOR CHARTS
# -----------------------------
df_chart = df.set_index("Period")

# -----------------------------
# ELECTRICITY CONSUMPTION
# -----------------------------
st.subheader("⚡ Monthly Electricity Consumption")

st.line_chart(df_chart["Consumption (kWh)"])

# -----------------------------
# CO2 EMISSIONS
# -----------------------------
st.subheader("🌍 Monthly CO₂ Emissions")

st.bar_chart(df_chart["CO2 Emissions (kg)"])

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📄 Cleaned Data")

st.dataframe(df, use_container_width=True)
