import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SMU Carbon Dashboard", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_scope2():
    df = pd.read_csv("Scope 2 Emissions (3).csv")
    df.columns = df.columns.str.strip()
    return df


@st.cache_data
def load_scope1():
    df = pd.read_csv("Carbon_Accounting_Medtech.csv")
    df.columns = df.columns.str.strip()
    return df


scope2_df = load_scope2()
scope1_df = load_scope1()

# -----------------------------
# LOGOS HEADER
# -----------------------------

col1, col2, col3 = st.columns([1,3,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=120)

with col2:
    st.title("SMU Carbon Accounting Dashboard")
    st.write("Monitoring Scope 1 and Scope 2 Emissions")

with col3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.divider()

# -----------------------------
# MONTH ORDER
# -----------------------------

month_order = [
"Jan","Feb","Mar","Apr","May","Jun",
"Jul","Aug","Sep","Oct","Nov","Dec"
]

# -----------------------------
# SCOPE 1 SECTION
# -----------------------------

st.header("Scope 1 Emissions")
st.write("Direct emissions produced by campus activities.")

st.dataframe(scope1_df)

# detect emission column
emission_col = None
for col in scope1_df.columns:
    if "emission" in col.lower() or "co2" in col.lower():
        emission_col = col
        break

if emission_col:

    scope1_df[emission_col] = pd.to_numeric(scope1_df[emission_col], errors="coerce")
    scope1_df[emission_col] = scope1_df[emission_col].fillna(0)

    total_scope1 = scope1_df[emission_col].sum()

    colA, colB = st.columns(2)

    with colA:
        st.metric("Total Scope 1 Emissions", f"{total_scope1:,.0f} kgCO2e")

    with colB:
        st.metric("Records", len(scope1_df))

    st.subheader("Scope 1 Emissions Distribution")

    st.bar_chart(scope1_df[emission_col])

else:
    st.warning("Emission column not detected in Scope 1 dataset.")

st.divider()

# -----------------------------
# SCOPE 2 SECTION
# -----------------------------

st.header("Scope 2 Emissions")
st.write("Indirect emissions from electricity consumption.")

st.dataframe(scope2_df)

# -----------------------------
# COLUMN DETECTION
# -----------------------------

month_col = None
cons_col = None
meter_col = None
building_col = None

for col in scope2_df.columns:

    if "month" in col.lower() or "period" in col.lower():
        month_col = col

    if "consumption" in col.lower() or "kwh" in col.lower():
        cons_col = col

    if "meter" in col.lower():
        meter_col = col

    if "building" in col.lower():
        building_col = col

# -----------------------------
# DATA CLEANING
# -----------------------------

if cons_col:
    scope2_df[cons_col] = pd.to_numeric(scope2_df[cons_col], errors="coerce")
    scope2_df[cons_col] = scope2_df[cons_col].fillna(0)

if meter_col:
    scope2_df[meter_col] = pd.to_numeric(scope2_df[meter_col], errors="coerce")
    scope2_df[meter_col] = scope2_df[meter_col].fillna(1)

# -----------------------------
# KPI SECTION
# -----------------------------

total_consumption = scope2_df[cons_col].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Electricity Consumption", f"{total_consumption:,.0f} kWh")

with col2:
    st.metric("Records", len(scope2_df))

# -----------------------------
# MONTHLY CONSUMPTION
# -----------------------------

if month_col:

    scope2_df[month_col] = scope2_df[month_col].astype(str)

    monthly = scope2_df.groupby(month_col)[cons_col].sum()

    monthly = monthly.reindex(month_order)

    st.subheader("Monthly Electricity Consumption")

    st.line_chart(monthly)

# -----------------------------
# BUILDING CONSUMPTION
# -----------------------------

if building_col:

    building_consumption = scope2_df.groupby(building_col)[cons_col].sum()

    st.subheader("Electricity Consumption by Building")

    st.bar_chart(building_consumption)

# -----------------------------
# TOP ELECTRICITY METERS
# -----------------------------

if meter_col and cons_col:

    scope2_df["Consumption_per_meter"] = scope2_df[cons_col] / scope2_df[meter_col]

    top_meters = scope2_df.sort_values(
        "Consumption_per_meter",
        ascending=False
    ).head(10)

    st.subheader("Top Electricity Meters (Consumption per Meter)")

    st.bar_chart(top_meters["Consumption_per_meter"])

# -----------------------------
# EMISSION ESTIMATION
# -----------------------------

emission_factor = 0.233

scope2_df["Estimated_CO2"] = scope2_df[cons_col] * emission_factor

total_emissions = scope2_df["Estimated_CO2"].sum()

st.subheader("Estimated Scope 2 CO₂ Emissions")

st.metric(
"Total Scope 2 Emissions",
f"{total_emissions:,.0f} kgCO2e"
)

st.bar_chart(scope2_df["Estimated_CO2"])

st.divider()

st.success("Dashboard loaded successfully.")
