import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Scope 2 Emissions Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# HEADER WITH LOGO
# ---------------------------------------------------
col_logo, col_title = st.columns([1,6])

with col_logo:
    st.image("logo.png", width=120)

with col_title:
    st.title("Scope 2 Carbon Emissions Dashboard")
    st.caption("Electricity consumption and carbon emissions analysis")

st.divider()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("Scope 2 Emissions (2).csv")

    df["Consumption (kWh)"] = (
        df["Consumption (kWh)"]
        .astype(str)
        .str.replace(" ", "")
        .str.replace(",", "")
        .replace("?", np.nan)
    )

    df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")

    df["Period"] = pd.to_datetime(df["Period"], format="%b-%y")

    df = df.sort_values("Period")

    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("⚙️ Dashboard Controls")

emission_factor = st.sidebar.slider(
    "Emission Factor (kg CO₂ / kWh)",
    0.1,
    1.0,
    0.45,
    0.05
)

# ---------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------
df["CO2 Emissions (kg)"] = df["Consumption (kWh)"] * emission_factor

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------
total_consumption = df["Consumption (kWh)"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_emissions = df["CO2 Emissions (kg)"].mean()

k1, k2, k3 = st.columns(3)

k1.metric("⚡ Total Electricity (kWh)", f"{total_consumption:,.0f}")
k2.metric("🌍 Total CO₂ Emissions (kg)", f"{total_emissions:,.0f}")
k3.metric("📊 Average Monthly CO₂", f"{avg_emissions:,.0f}")

st.divider()

# ---------------------------------------------------
# TIME SERIES PLOTS
# ---------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚡ Electricity Consumption Trend")

    electricity = df.set_index("Period")["Consumption (kWh)"]
    st.line_chart(electricity)

with col2:
    st.subheader("🌍 CO₂ Emissions Trend")

    emissions = df.set_index("Period")["CO2 Emissions (kg)"]
    st.line_chart(emissions)

# ---------------------------------------------------
# HISTOGRAMS
# ---------------------------------------------------
st.subheader("Distribution Analysis")

col3, col4 = st.columns(2)

# Electricity Histogram
with col3:

    st.markdown("**Electricity Consumption Distribution**")

    data = df["Consumption (kWh)"].dropna()

    hist, bins = np.histogram(data, bins=6)

    hist_df = pd.DataFrame({
        "Range": bins[:-1],
        "Frequency": hist
    }).set_index("Range")

    st.bar_chart(hist_df)

# Emissions Histogram
with col4:

    st.markdown("**CO₂ Emissions Distribution**")

    data2 = df["CO2 Emissions (kg)"].dropna()

    hist2, bins2 = np.histogram(data2, bins=6)

    hist_df2 = pd.DataFrame({
        "Range": bins2[:-1],
        "Frequency": hist2
    }).set_index("Range")

    st.bar_chart(hist_df2)

# ---------------------------------------------------
# SCATTER RELATIONSHIP
# ---------------------------------------------------
st.subheader("Consumption vs CO₂ Emissions")

scatter_data = df[["Consumption (kWh)", "CO2 Emissions (kg)"]].dropna()

st.scatter_chart(scatter_data)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------
st.subheader("Clean Dataset")

st.dataframe(df, use_container_width=True)
