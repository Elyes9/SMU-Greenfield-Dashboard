import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Scope 2 Dashboard", layout="wide")

st.title("🌍 Scope 2 Emissions Dashboard")

# -----------------------------
# LOAD AND CLEAN DATA
# -----------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("Scope 2 Emissions (1).csv")

    # Clean electricity values
    df["Consumption (kWh)"] = (
        df["Consumption (kWh)"]
        .astype(str)
        .str.replace(",", "")
        .str.replace(" ", "")
        .replace("?", np.nan)
    )

    df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")

    # Convert months to datetime
    df["Period"] = pd.to_datetime(df["Period"], format="%b-%y")

    # Sort months
    df = df.sort_values("Period")

    return df

df = load_data()

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
st.sidebar.header("⚙️ Controls")

emission_factor = st.sidebar.slider(
    "Emission Factor (kg CO₂ / kWh)",
    0.1,
    1.0,
    0.45,
    0.05
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
avg_consumption = df["Consumption (kWh)"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("⚡ Total Electricity (kWh)", f"{total_consumption:,.0f}")
col2.metric("🌍 Total CO₂ Emissions (kg)", f"{total_emissions:,.0f}")
col3.metric("📊 Average Monthly Consumption", f"{avg_consumption:,.0f}")

st.divider()

# -----------------------------
# MONTHLY ELECTRICITY TREND
# -----------------------------
st.subheader("⚡ Monthly Electricity Consumption")

chart_data = df.set_index("Period")["Consumption (kWh)"]
st.line_chart(chart_data)

# -----------------------------
# MONTHLY EMISSIONS
# -----------------------------
st.subheader("🌍 Monthly CO₂ Emissions")

emission_chart = df.set_index("Period")["CO2 Emissions (kg)"]
st.bar_chart(emission_chart)

# -----------------------------
# HISTOGRAM: ELECTRICITY
# -----------------------------
st.subheader("📊 Histogram of Electricity Consumption")

consumption = df["Consumption (kWh)"].dropna()

hist, bins = np.histogram(consumption, bins=6)

hist_df = pd.DataFrame({
    "Bin": bins[:-1],
    "Frequency": hist
}).set_index("Bin")

st.bar_chart(hist_df)

# -----------------------------
# HISTOGRAM: EMISSIONS
# -----------------------------
st.subheader("🌍 Histogram of CO₂ Emissions")

emissions = df["CO2 Emissions (kg)"].dropna()

hist2, bins2 = np.histogram(emissions, bins=6)

hist_df2 = pd.DataFrame({
    "Bin": bins2[:-1],
    "Frequency": hist2
}).set_index("Bin")

st.bar_chart(hist_df2)

# -----------------------------
# SCATTER PLOT
# -----------------------------
st.subheader("🔎 Consumption vs CO₂ Emissions")

scatter_data = df[["Consumption (kWh)", "CO2 Emissions (kg)"]].dropna()

st.scatter_chart(scatter_data)

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📄 Dataset")

st.dataframe(df, use_container_width=True)
