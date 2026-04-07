import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="SMU Carbon Emissions Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# LOGOS
# ---------------------------------------------------

col1, col2 = st.columns([1,5])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=120)

with col2:
    st.title("SMU Carbon Accounting Dashboard")
    st.write("Monitoring Scope 1 and Scope 2 Emissions – Year 2025")

st.image("carbon_jar_logo (1).jfif", width=90)

st.divider()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_scope1_vehicle():
    df = pd.read_csv("Mobile_Combustion_Vehicle.csv")
    return df

@st.cache_data
def load_scope1_bus():
    df = pd.read_csv("Mobile_Combustion_Buses.csv")
    return df

@st.cache_data
def load_scope2():
    df = pd.read_csv("Scope 2 Emissions (3).csv")
    return df


vehicle_df = load_scope1_vehicle()
bus_df = load_scope1_bus()
scope2_df = load_scope2()

# ---------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------

for df in [vehicle_df, bus_df, scope2_df]:
    df.columns = df.columns.str.strip()

# ---------------------------------------------------
# SCOPE 1 SECTION
# ---------------------------------------------------

st.header("Scope 1 Emissions – Mobile Combustion")

# ---------------------------------------------------
# VEHICLES
# ---------------------------------------------------

st.subheader("Mobile Combustion – Cars")

vehicle_numeric = vehicle_df.select_dtypes(include=np.number)

if not vehicle_numeric.empty:

    total_vehicle_emissions = vehicle_numeric.sum().sum()

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Vehicle Emissions",
        f"{total_vehicle_emissions:,.0f} kgCO2e"
    )

    # Plot
    vehicle_plot = vehicle_numeric.sum()

    st.bar_chart(vehicle_plot)

else:
    st.warning("No numeric emissions data detected in vehicle dataset")

st.dataframe(vehicle_df)

st.divider()

# ---------------------------------------------------
# BUSES
# ---------------------------------------------------

st.subheader("Mobile Combustion – Buses")

bus_numeric = bus_df.select_dtypes(include=np.number)

if not bus_numeric.empty:

    total_bus_emissions = bus_numeric.sum().sum()

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Bus Emissions",
        f"{total_bus_emissions:,.0f} kgCO2e"
    )

    bus_plot = bus_numeric.sum()

    st.bar_chart(bus_plot)

else:
    st.warning("No numeric emissions data detected in bus dataset")

st.dataframe(bus_df)

st.divider()

# ---------------------------------------------------
# SCOPE 2 SECTION
# ---------------------------------------------------

st.header("Scope 2 Emissions – Electricity Consumption")

scope2_numeric = scope2_df.select_dtypes(include=np.number)

if not scope2_numeric.empty:

    total_electricity = scope2_numeric.sum().sum()

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Electricity Emissions",
        f"{total_electricity:,.0f} kgCO2e"
    )

    # Electricity consumption plot
    electricity_plot = scope2_numeric.sum()

    st.bar_chart(electricity_plot)

else:
    st.warning("No numeric electricity data detected")

st.dataframe(scope2_df)

# ---------------------------------------------------
# COMBINED SUMMARY
# ---------------------------------------------------

st.header("Overall Emissions Summary")

vehicle_total = vehicle_numeric.sum().sum() if not vehicle_numeric.empty else 0
bus_total = bus_numeric.sum().sum() if not bus_numeric.empty else 0
scope2_total = scope2_numeric.sum().sum() if not scope2_numeric.empty else 0

summary = pd.DataFrame({
    "Category": ["Vehicles", "Buses", "Electricity"],
    "Emissions (kgCO2e)": [vehicle_total, bus_total, scope2_total]
})

st.bar_chart(summary.set_index("Category"))

st.dataframe(summary)

st.success("Dashboard successfully loaded.")
