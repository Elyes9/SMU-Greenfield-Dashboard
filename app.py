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
# EMISSION FACTOR
# ---------------------------------------------------

EMISSION_FACTOR = 0.42

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("Scope 2 Emissions (1).csv")

    df.columns = df.columns.str.strip()

    # Convert numeric columns
    df["Consumption (kWh)"] = pd.to_numeric(df["Consumption (kWh)"], errors="coerce")
    df["Number of meters"] = pd.to_numeric(df["Number of meters"], errors="coerce")

    # Fill missing values
    df["Consumption (kWh)"] = df["Consumption (kWh)"].fillna(0)
    df["Number of meters"] = df["Number of meters"].replace(0,1)

    # Month order
    months_order = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    df["Period"] = pd.Categorical(df["Period"], categories=months_order, ordered=True)

    df = df.sort_values("Period")

    # Calculate emissions
    df["CO2 Emissions (kg)"] = df["Consumption (kWh)"] * EMISSION_FACTOR

    # Consumption per meter
    df["Consumption per meter"] = df["Consumption (kWh)"] / df["Number of meters"]

    return df


df = load_data()

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------

total_consumption = df["Consumption (kWh)"].sum()
total_emissions = df["CO2 Emissions (kg)"].sum()
avg_meter_consumption = df["Consumption per meter"].mean()

c1, c2, c3 = st.columns(3)

c1.metric("Total Electricity Consumption (kWh)", f"{total_consumption:,.0f}")
c2.metric("Total CO₂ Emissions (kg)", f"{total_emissions:,.0f}")
c3.metric("Average Consumption per Meter (kWh)", f"{avg_meter_consumption:,.1f}")

st.markdown("---")

# ---------------------------------------------------
# MONTHLY CONSUMPTION
# ---------------------------------------------------

st.subheader("Monthly Electricity Consumption")

st.line_chart(
    df.set_index("Period")[["Consumption (kWh)"]]
)

# ---------------------------------------------------
# MONTHLY EMISSIONS
# ---------------------------------------------------

st.subheader("Monthly CO₂ Emissions")

st.bar_chart(
    df.set_index("Period")[["CO2 Emissions (kg)"]]
)

# ---------------------------------------------------
# NUMBER OF METERS
# ---------------------------------------------------

st.subheader("Number of Electricity Meters")

st.line_chart(
    df.set_index("Period")[["Number of meters"]]
)

# ---------------------------------------------------
# CONSUMPTION PER METER
# ---------------------------------------------------

st.subheader("Consumption per Meter")

st.bar_chart(
    df.set_index("Period")[["Consumption per meter"]]
)

# ---------------------------------------------------
# EMISSION SHARE
# ---------------------------------------------------

st.subheader("Monthly Share of Total Emissions")

df["Emission Share (%)"] = (df["CO2 Emissions (kg)"] / total_emissions) * 100

st.bar_chart(
    df.set_index("Period")[["Emission Share (%)"]]
)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

st.subheader("Dataset")

st.dataframe(df)

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
