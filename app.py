import streamlit as st
import pandas as pd
import numpy as np
import os

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Scope 2 Carbon Dashboard",
    layout="wide"
)

# -------------------------------------------------
# HEADER WITH SAFE LOGO
# -------------------------------------------------
col_logo, col_title = st.columns([1,6])

with col_logo:
    if os.path.exists("LOGO_SMU_2023_FINAL.png"):
        st.image("carbon_jar_logo (1).jfif", width=110)

with col_title:
    st.title("🌍 Scope 2 Carbon Emissions Dashboard")
    st.caption("Electricity consumption and Scope 2 emissions analysis")

st.divider()

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
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

    df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")

    # Convert months
    df["Period"] = pd.to_datetime(df["Period"], format="%b-%y")

    # Sort months correctly
    df = df.sort_values("Period")

    return df

df = load_data()

# -------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------
st.sidebar.header("⚙️ Dashboard Controls")

emission_factor = st.sidebar.slider(
    "Emission Factor (kg CO₂ / kWh)",
    min_value=0.1,
    max_value=1.0,
    value=0.45,
    step=0.05
)

# -------------------------------------------------
# CALCULATE EMISSIONS
# -------------------------------------------------
df["CO2 Emissions (kg)"] = df["Consumption (kWh)"] * emission_factor

# -------------------------------------------------
# KPI METRICS
# -------------------------------------------------
total_consumption = df["Consumption (kWh)"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_consumption = df["Consumption (kWh)"].mean()

k1, k2, k3 = st.columns(3)

k1.metric("⚡ Total Electricity (kWh)", f"{total_consumption:,.0f}")
k2.metric("🌍 Total CO₂ Emissions (kg)", f"{total_emissions:,.0f}")
k3.metric("📊 Average Monthly Consumption", f"{avg_consumption:,.0f}")

st.divider()

# -------------------------------------------------
# TREND CHARTS
# -------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("⚡ Electricity Consumption Trend")

    electricity = df.set_index("Period")["Consumption (kWh)"]
    st.line_chart(electricity)

with c2:
    st.subheader("🌍 CO₂ Emissions Trend")

    emissions = df.set_index("Period")["CO2 Emissions (kg)"]
    st.line_chart(emissions)

st.divider()

# -------------------------------------------------
# HISTOGRAMS
# -------------------------------------------------
st.subheader("📊 Distribution Analysis")

col1, col2 = st.columns(2)

# Electricity histogram
with col1:

    st.markdown("**Electricity Consumption Distribution**")

    data = df["Consumption (kWh)"].dropna()

    hist, bins = np.histogram(data, bins=6)

    hist_df = pd.DataFrame({
        "Range": bins[:-1],
        "Frequency": hist
    }).set_index("Range")

    st.bar_chart(hist_df)

# Emissions histogram
with col2:

    st.markdown("**CO₂ Emissions Distribution**")

    data2 = df["CO2 Emissions (kg)"].dropna()

    hist2, bins2 = np.histogram(data2, bins=6)

    hist_df2 = pd.DataFrame({
        "Range": bins2[:-1],
        "Frequency": hist2
    }).set_index("Range")

    st.bar_chart(hist_df2)

st.divider()

# -------------------------------------------------
# SCATTER RELATIONSHIP
# -------------------------------------------------
st.subheader("🔎 Electricity vs CO₂ Emissions")

scatter_data = df[["Consumption (kWh)", "CO2 Emissions (kg)"]].dropna()

st.scatter_chart(scatter_data)

st.divider()

# -------------------------------------------------
# DATA TABLE
# -------------------------------------------------
st.subheader("📄 Cleaned Dataset")

st.dataframe(df, use_container_width=True)
