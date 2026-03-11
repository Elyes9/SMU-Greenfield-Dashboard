import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="SMU Carbon Dashboard", layout="wide")

# -------------------------
# GREEN STYLE
# -------------------------
st.markdown("""
<style>
.main {
background-color:#f5fff5;
}
.kpi {
background:#e8f5e9;
padding:20px;
border-radius:10px;
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
    st.title("SMU Scope 2 Carbon Dashboard")
    st.write("Greenfield Carbon Accounting Project")

st.image("carbon_jar_logo (1).jfif", width=100)

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Scope 2 emissions.csv")
    return df

df = load_data()

# -------------------------
# AUTOMATIC COLUMN DETECTION
# -------------------------
name_column = df.columns[0]
energy_column = df.columns[1]

# -------------------------
# SIDEBAR FILTER
# -------------------------
st.sidebar.header("Filters")

selection = st.sidebar.multiselect(
    "Select Meter / Building",
    df[name_column].unique(),
    default=df[name_column].unique()
)

df = df[df[name_column].isin(selection)]

# -------------------------
# EMISSION FACTOR
# -------------------------
emission_factor = st.sidebar.number_input(
    "Emission Factor (kg CO2 / kWh)",
    value=0.55
)

# -------------------------
# CALCULATE EMISSIONS
# -------------------------
df["CO2 Emissions (kg)"] = df[energy_column] * emission_factor

# -------------------------
# KPI CARDS
# -------------------------
total_energy = df[energy_column].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_energy = df[energy_column].mean()

c1, c2, c3 = st.columns(3)

c1.metric("Total Electricity (kWh)", f"{total_energy:,.0f}")
c2.metric("Total CO2 Emissions (kg)", f"{total_emissions:,.0f}")
c3.metric("Average Consumption", f"{avg_energy:,.0f}")

st.divider()

# -------------------------
# ELECTRICITY CHART
# -------------------------
st.subheader("Electricity Consumption")

energy_chart = df.groupby(name_column)[energy_column].sum()

st.bar_chart(energy_chart)

# -------------------------
# EMISSIONS CHART
# -------------------------
st.subheader("CO2 Emissions")

emission_chart = df.groupby(name_column)["CO2 Emissions (kg)"].sum()

st.bar_chart(emission_chart)

# -------------------------
# TOP METERS
# -------------------------
st.subheader("Top Electricity Consumers")

top = df.sort_values(energy_column, ascending=False).head(10)

st.dataframe(top)

# -------------------------
# DATA TABLE
# -------------------------
st.subheader("Dataset")

st.dataframe(df)
