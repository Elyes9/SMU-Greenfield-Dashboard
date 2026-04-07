import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SMU Carbon Dashboard", layout="wide")

# ------------------------------------------------
# LOGOS
# ------------------------------------------------

col1, col2 = st.columns([1,6])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=120)

with col2:
    st.title("SMU Carbon Emissions Dashboard")
    st.markdown("### Scope 1 and Scope 2 Carbon Accounting – 2025")

st.image("carbon_jar_logo (1).jfif", width=120)

st.markdown("---")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

@st.cache_data
def load_scope2():
    df = pd.read_csv("Scope 2 Emissions (4).csv")
    df.columns = df.columns.str.strip()
    return df

@st.cache_data
def load_vehicle():
    df = pd.read_csv("Mobile_Combustion_Vehicle.csv")
    df.columns = df.columns.str.strip()
    return df

@st.cache_data
def load_bus():
    df = pd.read_csv("Mobile_Combustion_Buses.csv")
    df.columns = df.columns.str.strip()
    return df


scope2_df = load_scope2()
vehicle_df = load_vehicle()
bus_df = load_bus()

# ------------------------------------------------
# EMISSION FACTORS
# ------------------------------------------------

vehicle_ef = 2.31
bus_ef = 2.68
grid_ef = 0.42

# ------------------------------------------------
# SCOPE 1 SECTION
# ------------------------------------------------

st.header("Scope 1 – Direct Emissions")

# ------------------------------------------------
# VEHICLES
# ------------------------------------------------

st.subheader("Mobile Combustion – Vehicles")

fuel_col_v = vehicle_df.select_dtypes(include=np.number).columns[0]

vehicle_df[fuel_col_v] = pd.to_numeric(vehicle_df[fuel_col_v], errors="coerce")

vehicle_df["CO2"] = vehicle_df[fuel_col_v] * vehicle_ef

total_vehicle = vehicle_df["CO2"].sum()

st.metric("Vehicle Emissions", f"{total_vehicle:,.0f} kgCO2e")

st.write("Emission Factor Range (Gasoline): **2.2 – 2.4 kg CO₂/L**")

st.markdown("#### Vehicle Fuel Consumption")

st.bar_chart(vehicle_df[fuel_col_v])

st.markdown("#### Vehicle CO₂ Emissions")

st.line_chart(vehicle_df["CO2"])

# ------------------------------------------------
# BUSES
# ------------------------------------------------

st.subheader("Mobile Combustion – Buses")

fuel_col_b = bus_df.select_dtypes(include=np.number).columns[0]

bus_df[fuel_col_b] = pd.to_numeric(bus_df[fuel_col_b], errors="coerce")

bus_df["CO2"] = bus_df[fuel_col_b] * bus_ef

total_bus = bus_df["CO2"].sum()

st.metric("Bus Emissions", f"{total_bus:,.0f} kgCO2e")

st.write("Emission Factor Range (Diesel): **2.6 – 2.8 kg CO₂/L**")

st.markdown("#### Bus Fuel Consumption")

st.bar_chart(bus_df[fuel_col_b])

st.markdown("#### Bus CO₂ Emissions")

st.line_chart(bus_df["CO2"])

# ------------------------------------------------
# SCOPE 2 SECTION
# ------------------------------------------------

st.header("Scope 2 – Electricity Emissions")

num_cols = scope2_df.select_dtypes(include=np.number).columns
consumption_col = num_cols[0]

scope2_df[consumption_col] = pd.to_numeric(scope2_df[consumption_col], errors="coerce")

scope2_df["CO2"] = scope2_df[consumption_col] * grid_ef

total_scope2 = scope2_df["CO2"].sum()

st.metric("Total Electricity Emissions", f"{total_scope2:,.0f} kgCO2e")

# ------------------------------------------------
# DETECT COLUMNS
# ------------------------------------------------

month_col = None
building_col = None

for c in scope2_df.columns:
    if "month" in c.lower():
        month_col = c
    if "building" in c.lower():
        building_col = c

# ------------------------------------------------
# MONTH ORDER
# ------------------------------------------------

months = [
"January","February","March","April","May","June",
"July","August","September","October","November","December"
]

if month_col is not None:

    scope2_df[month_col] = pd.Categorical(
        scope2_df[month_col],
        categories=months,
        ordered=True
    )

# ------------------------------------------------
# MONTHLY ELECTRICITY TREND
# ------------------------------------------------

if month_col is not None:

    st.subheader("Monthly Electricity Consumption")

    monthly_consumption = (
        scope2_df
        .groupby(month_col)[consumption_col]
        .sum()
        .sort_index()
    )

    st.line_chart(monthly_consumption)

# ------------------------------------------------
# MONTHLY CO2 TREND
# ------------------------------------------------

if month_col is not None:

    st.subheader("Monthly CO₂ Emissions")

    monthly_emissions = (
        scope2_df
        .groupby(month_col)["CO2"]
        .sum()
        .sort_index()
    )

    st.bar_chart(monthly_emissions)

# ------------------------------------------------
# BUILDING ELECTRICITY COMPARISON
# ------------------------------------------------

if building_col is not None:

    st.subheader("Electricity Consumption by Building")

    building_consumption = (
        scope2_df
        .groupby(building_col)[consumption_col]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(building_consumption)

# ------------------------------------------------
# BUILDING EMISSIONS
# ------------------------------------------------

if building_col is not None:

    st.subheader("CO₂ Emissions by Building")

    building_emissions = (
        scope2_df
        .groupby(building_col)["CO2"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(building_emissions)

# ------------------------------------------------
# TOP ELECTRICITY CONSUMERS
# ------------------------------------------------

st.subheader("Top Electricity Consumers")

top_consumers = scope2_df.sort_values(consumption_col, ascending=False).head(10)

st.dataframe(top_consumers)

# ------------------------------------------------
# SCATTER RELATIONSHIP
# ------------------------------------------------

st.subheader("Electricity Consumption vs CO₂")

scatter_df = scope2_df[[consumption_col, "CO2"]]

st.scatter_chart(scatter_df)

# ------------------------------------------------
# TOTAL CARBON FOOTPRINT
# ------------------------------------------------

st.header("Total Campus Carbon Footprint")

total_scope1 = total_vehicle + total_bus
total_emissions = total_scope1 + total_scope2

st.metric("Total Scope 1", f"{total_scope1:,.0f} kgCO2e")
st.metric("Total Scope 2", f"{total_scope2:,.0f} kgCO2e")
st.metric("Total Emissions", f"{total_emissions:,.0f} kgCO2e")

st.markdown("---")

st.success("SMU Sustainability Dashboard – Carbon Accounting Analysis")
