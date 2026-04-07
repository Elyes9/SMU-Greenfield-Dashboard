import streamlit as st
import pandas as pd
import numpy as np

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="SMU Carbon Dashboard",
    layout="wide"
)

# ------------------------------------------------
# HEADER + LOGOS
# ------------------------------------------------

c1, c2, c3 = st.columns([1,3,1])

with c1:
    st.image("LOGO_SMU_2023_FINAL.png", width=120)

with c3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.title("SMU Campus Carbon Accounting Dashboard")
st.write("Scope 1 and Scope 2 Emissions Analysis – 2025")

st.markdown("---")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

@st.cache_data
def load_data():

    vehicles = pd.read_csv("Mobile_Combustion_Vehicle.csv")
    buses = pd.read_csv("Mobile_Combustion_Buses.csv")
    electricity = pd.read_csv("Scope 2 Emissions (4).csv")

    vehicles.columns = vehicles.columns.str.strip()
    buses.columns = buses.columns.str.strip()
    electricity.columns = electricity.columns.str.strip()

    return vehicles, buses, electricity


vehicles_df, buses_df, scope2_df = load_data()

# ------------------------------------------------
# EMISSION FACTORS
# ------------------------------------------------

CAR_EF_MIN = 2.20
CAR_EF_MAX = 2.40

BUS_EF_MIN = 2.60
BUS_EF_MAX = 2.80

GRID_EF = 0.42

# ------------------------------------------------
# SCOPE 1
# ------------------------------------------------

st.header("Scope 1 – Direct Emissions")

# =================================================
# VEHICLES
# =================================================

st.subheader("Mobile Combustion – Cars")

fuel_col = vehicles_df.select_dtypes(include=np.number).columns[0]

vehicles_df[fuel_col] = pd.to_numeric(vehicles_df[fuel_col], errors="coerce")

vehicles_df["CO2_min"] = vehicles_df[fuel_col] * CAR_EF_MIN
vehicles_df["CO2_max"] = vehicles_df[fuel_col] * CAR_EF_MAX
vehicles_df["CO2"] = (vehicles_df["CO2_min"] + vehicles_df["CO2_max"]) / 2

vehicle_total = vehicles_df["CO2"].sum()

st.metric("Vehicle Emissions", f"{vehicle_total:,.0f} kgCO2e")

st.write("Vehicle CO₂ emissions calculated using emission factor range:")
st.write(f"{CAR_EF_MIN} – {CAR_EF_MAX} kg CO₂ / L")

# PLOT VEHICLES

vehicle_plot = vehicles_df[["CO2"]]

st.line_chart(vehicle_plot)

# =================================================
# BUSES
# =================================================

st.subheader("Mobile Combustion – Buses")

fuel_col_bus = buses_df.select_dtypes(include=np.number).columns[0]

buses_df[fuel_col_bus] = pd.to_numeric(buses_df[fuel_col_bus], errors="coerce")

buses_df["CO2_min"] = buses_df[fuel_col_bus] * BUS_EF_MIN
buses_df["CO2_max"] = buses_df[fuel_col_bus] * BUS_EF_MAX
buses_df["CO2"] = (buses_df["CO2_min"] + buses_df["CO2_max"]) / 2

bus_total = buses_df["CO2"].sum()

st.metric("Bus Emissions", f"{bus_total:,.0f} kgCO2e")

st.write("Bus CO₂ emissions calculated using emission factor range:")
st.write(f"{BUS_EF_MIN} – {BUS_EF_MAX} kg CO₂ / L")

# BUS PLOT

bus_plot = buses_df[["CO2"]]

st.line_chart(bus_plot)

st.markdown("---")



# ------------------------------------------------
# SCOPE 2 – ELECTRICITY
# ------------------------------------------------

st.header("Scope 2 – Electricity Emissions")

GRID_EF = 0.42   # kg CO2 per kWh

scope2_df.columns = scope2_df.columns.str.strip()

# Detect columns automatically
num_cols = scope2_df.select_dtypes(include=np.number).columns
consumption_col = num_cols[0]

month_col = [c for c in scope2_df.columns if "month" in c.lower()][0]
building_col = [c for c in scope2_df.columns if "building" in c.lower()][0]

scope2_df[consumption_col] = pd.to_numeric(scope2_df[consumption_col], errors="coerce")

# Calculate emissions
scope2_df["CO2"] = scope2_df[consumption_col] * GRID_EF

total_scope2 = scope2_df["CO2"].sum()

# KPI
st.metric("Total Electricity Emissions", f"{total_scope2:,.0f} kgCO2e")

st.markdown("---")

# ------------------------------------------------
# MONTH ORDER
# ------------------------------------------------

months = [
"January","February","March","April","May","June",
"July","August","September","October","November","December"
]

scope2_df[month_col] = pd.Categorical(
    scope2_df[month_col],
    categories=months,
    ordered=True
)

# ------------------------------------------------
# MONTHLY CONSUMPTION TREND
# ------------------------------------------------

st.subheader("Monthly Electricity Consumption (2025)")

monthly_consumption = (
    scope2_df
    .groupby(month_col)[consumption_col]
    .sum()
    .sort_index()
)

st.line_chart(monthly_consumption)

# ------------------------------------------------
# MONTHLY CO2 EMISSIONS
# ------------------------------------------------

st.subheader("Monthly CO₂ Emissions from Electricity")

monthly_emissions = (
    scope2_df
    .groupby(month_col)["CO2"]
    .sum()
    .sort_index()
)

st.bar_chart(monthly_emissions)

# ------------------------------------------------
# BUILDING ELECTRICITY CONSUMPTION
# ------------------------------------------------

st.subheader("Electricity Consumption by Building")

building_consumption = (
    scope2_df
    .groupby(building_col)[consumption_col]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(building_consumption)

# ------------------------------------------------
# BUILDING CO2 EMISSIONS
# ------------------------------------------------

st.subheader("CO₂ Emissions by Building")

building_emissions = (
    scope2_df
    .groupby(building_col)["CO2"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(building_emissions)

# ------------------------------------------------
# TOP ELECTRICITY METERS
# ------------------------------------------------

st.subheader("Top Electricity Consumers")

top_consumers = scope2_df.sort_values(consumption_col, ascending=False).head(10)

st.dataframe(top_consumers)

# ------------------------------------------------
# CONSUMPTION VS EMISSIONS RELATIONSHIP
# ------------------------------------------------

st.subheader("Electricity Consumption vs CO₂ Emissions")

scatter_df = scope2_df[[consumption_col, "CO2"]]

st.scatter_chart(scatter_df)
)

st.bar_chart(comparison)
