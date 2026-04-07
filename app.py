import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="SMU Carbon Accounting Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# LOGOS
# ---------------------------------------------------

col1, col2, col3 = st.columns([1,3,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=140)

with col3:
    st.image("carbon_jar_logo (1).jfif", width=140)

st.title("SMU Campus Carbon Accounting Dashboard")
st.markdown("### Scope 1 and Scope 2 Greenhouse Gas Emissions Analysis")

st.markdown("---")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

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

# ---------------------------------------------------
# EMISSION FACTORS
# ---------------------------------------------------

CAR_EF_MIN = 2.20
CAR_EF_MAX = 2.40

BUS_EF_MIN = 2.60
BUS_EF_MAX = 2.80

GRID_EF = 0.42  # kgCO2/kWh

# ---------------------------------------------------
# SCOPE 1 SECTION
# ---------------------------------------------------

st.header("Scope 1 – Direct Emissions")

st.markdown("""
Scope 1 emissions correspond to **direct greenhouse gas emissions from sources owned or controlled by the university**.
This section focuses on **mobile combustion sources**, including **campus vehicles and buses**.
""")

# ===================================================
# VEHICLES
# ===================================================

st.subheader("Mobile Combustion – Campus Vehicles")

st.markdown(f"""
**Emission factor range used for vehicles:**

{CAR_EF_MIN} – {CAR_EF_MAX} kgCO₂ / litre of fuel
""")

fuel_col = [c for c in vehicles_df.columns if "fuel" in c.lower() or "consumption" in c.lower()]

if fuel_col:
    fuel_column = fuel_col[0]
else:
    fuel_column = vehicles_df.columns[-1]

vehicles_df[fuel_column] = pd.to_numeric(vehicles_df[fuel_column], errors="coerce")

vehicles_df["CO2_min"] = vehicles_df[fuel_column] * CAR_EF_MIN
vehicles_df["CO2_max"] = vehicles_df[fuel_column] * CAR_EF_MAX
vehicles_df["CO2_mean"] = (vehicles_df["CO2_min"] + vehicles_df["CO2_max"]) / 2

total_vehicle_emissions = vehicles_df["CO2_mean"].sum()

st.metric("Total Vehicle Emissions", f"{total_vehicle_emissions:,.0f} kgCO2e")

st.markdown("#### Vehicle Emissions")

vehicle_plot = vehicles_df.set_index(vehicles_df.columns[0])["CO2_mean"]

st.line_chart(vehicle_plot)

st.markdown("---")

# ===================================================
# BUSES
# ===================================================

st.subheader("Mobile Combustion – Campus Buses")

st.markdown(f"""
**Emission factor range used for buses:**

{BUS_EF_MIN} – {BUS_EF_MAX} kgCO₂ / litre of fuel
""")

fuel_col_bus = [c for c in buses_df.columns if "fuel" in c.lower() or "consumption" in c.lower()]

if fuel_col_bus:
    bus_fuel_column = fuel_col_bus[0]
else:
    bus_fuel_column = buses_df.columns[-1]

buses_df[bus_fuel_column] = pd.to_numeric(buses_df[bus_fuel_column], errors="coerce")

buses_df["CO2_min"] = buses_df[bus_fuel_column] * BUS_EF_MIN
buses_df["CO2_max"] = buses_df[bus_fuel_column] * BUS_EF_MAX
buses_df["CO2_mean"] = (buses_df["CO2_min"] + buses_df["CO2_max"]) / 2

total_bus_emissions = buses_df["CO2_mean"].sum()

st.metric("Total Bus Emissions", f"{total_bus_emissions:,.0f} kgCO2e")

st.markdown("#### Bus Emissions")

bus_plot = buses_df.set_index(buses_df.columns[0])["CO2_mean"]

st.line_chart(bus_plot)

st.markdown("---")

# ---------------------------------------------------
# SCOPE 2 SECTION
# ---------------------------------------------------

st.header("Scope 2 – Electricity Consumption")

st.markdown("""
Scope 2 emissions correspond to **indirect emissions from purchased electricity** consumed on campus.
""")

consumption_col = [c for c in scope2_df.columns if "kwh" in c.lower()]

if consumption_col:
    consumption_column = consumption_col[0]
else:
    consumption_column = scope2_df.columns[-1]

scope2_df[consumption_column] = pd.to_numeric(scope2_df[consumption_column], errors="coerce")

scope2_df["CO2"] = scope2_df[consumption_column] * GRID_EF

total_scope2 = scope2_df["CO2"].sum()

st.metric("Total Electricity Emissions", f"{total_scope2:,.0f} kgCO2e")

st.markdown("### Monthly Electricity Consumption")

month_col = [c for c in scope2_df.columns if "month" in c.lower()]

if month_col:
    month_column = month_col[0]
else:
    month_column = scope2_df.columns[0]

months_order = [
"January","February","March","April","May","June",
"July","August","September","October","November","December"
]

scope2_df[month_column] = pd.Categorical(
    scope2_df[month_column],
    categories=months_order,
    ordered=True
)

monthly_consumption = scope2_df.groupby(month_column)[consumption_column].sum().sort_index()

st.line_chart(monthly_consumption)

st.markdown("### Monthly CO2 Emissions")

monthly_emissions = scope2_df.groupby(month_column)["CO2"].sum().sort_index()

st.line_chart(monthly_emissions)

st.markdown("---")

# ---------------------------------------------------
# BUILDING COMPARISON
# ---------------------------------------------------

building_cols = [c for c in scope2_df.columns if "building" in c.lower()]

if building_cols:

    building_column = building_cols[0]

    st.subheader("Building Electricity Consumption")

    building_consumption = scope2_df.groupby(building_column)[consumption_column].sum()

    st.bar_chart(building_consumption)

# ---------------------------------------------------
# TOTAL FOOTPRINT
# ---------------------------------------------------

st.header("Total Campus Carbon Footprint")

total_emissions = total_vehicle_emissions + total_bus_emissions + total_scope2

colA, colB, colC = st.columns(3)

colA.metric("Vehicles", f"{total_vehicle_emissions:,.0f} kgCO2e")
colB.metric("Buses", f"{total_bus_emissions:,.0f} kgCO2e")
colC.metric("Electricity", f"{total_scope2:,.0f} kgCO2e")

st.success(f"Total Campus Emissions: {total_emissions:,.0f} kgCO2e")
