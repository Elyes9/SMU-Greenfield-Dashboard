import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="SMU Carbon Accounting Dashboard",
    layout="wide"
)

# --------------------------------------------------
# HEADER WITH LOGOS
# --------------------------------------------------

col1, col2, col3 = st.columns([1,4,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=120)

with col2:
    st.title("SMU Carbon Emissions Dashboard")
    st.write("Executive Carbon Monitoring Platform – 2025")

with col3:
    st.image("carbon_jar_logo (1).jfif", width=100)

st.divider()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    vehicle = pd.read_csv("Mobile_Combustion_Vehicle.csv")
    buses = pd.read_csv("Mobile_Combustion_Buses.csv")
    electricity = pd.read_csv("Scope 2 Emissions (3).csv")

    vehicle.columns = vehicle.columns.str.strip()
    buses.columns = buses.columns.str.strip()
    electricity.columns = electricity.columns.str.strip()

    return vehicle, buses, electricity


vehicle_df, bus_df, scope2_df = load_data()

# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def numeric_data(df):
    return df.select_dtypes(include=np.number)

# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------

st.header("Executive Carbon Summary")

vehicle_total = numeric_data(vehicle_df).sum().sum()
bus_total = numeric_data(bus_df).sum().sum()
electricity_total = numeric_data(scope2_df).sum().sum()

total_emissions = vehicle_total + bus_total + electricity_total

col1, col2, col3, col4 = st.columns(4)

col1.metric("Vehicle Emissions", f"{vehicle_total:,.0f} kgCO2e")
col2.metric("Bus Emissions", f"{bus_total:,.0f} kgCO2e")
col3.metric("Electricity Emissions", f"{electricity_total:,.0f} kgCO2e")
col4.metric("Total Campus Emissions", f"{total_emissions:,.0f} kgCO2e")

st.divider()

# --------------------------------------------------
# SCOPE 1 SECTION
# --------------------------------------------------

st.header("Scope 1 – Mobile Combustion")

# --------------------------------------------------
# VEHICLES
# --------------------------------------------------

st.subheader("Cars Fleet Emissions")

vehicle_numeric = numeric_data(vehicle_df)

if not vehicle_numeric.empty:

    st.write("Fuel Consumption / Emissions Analysis")

    vehicle_plot = vehicle_numeric.sum()

    st.bar_chart(vehicle_plot)

    st.dataframe(vehicle_df)

else:
    st.warning("No numeric vehicle data detected")

st.divider()

# --------------------------------------------------
# BUSES
# --------------------------------------------------

st.subheader("Campus Bus Fleet Emissions")

bus_numeric = numeric_data(bus_df)

if not bus_numeric.empty:

    bus_plot = bus_numeric.sum()

    st.bar_chart(bus_plot)

    st.dataframe(bus_df)

else:
    st.warning("No numeric bus data detected")

st.divider()

# --------------------------------------------------
# SCOPE 2 SECTION
# --------------------------------------------------

st.header("Scope 2 – Electricity Consumption")

scope2_numeric = numeric_data(scope2_df)

if not scope2_numeric.empty:

    st.subheader("Electricity Consumption by Building")

    building_plot = scope2_numeric.sum()

    st.bar_chart(building_plot)

    st.dataframe(scope2_df)

else:
    st.warning("No electricity data detected")

st.divider()

# --------------------------------------------------
# MONTHLY EMISSIONS TREND
# --------------------------------------------------

st.header("Monthly Emissions Trend (2025)")

months = [
"Jan","Feb","Mar","Apr","May","Jun",
"Jul","Aug","Sep","Oct","Nov","Dec"
]

monthly_data = {}

for m in months:
    for df in [vehicle_df, bus_df, scope2_df]:

        if m in df.columns:
            monthly_data[m] = monthly_data.get(m,0) + df[m].sum()

if monthly_data:

    monthly_df = pd.DataFrame({
        "Month": list(monthly_data.keys()),
        "Emissions": list(monthly_data.values())
    })

    monthly_df = monthly_df.set_index("Month")

    st.line_chart(monthly_df)

else:
    st.info("Monthly columns not detected in dataset")

st.divider()

# --------------------------------------------------
# EMISSIONS DISTRIBUTION
# --------------------------------------------------

st.header("Campus Emissions Distribution")

distribution = pd.DataFrame({

    "Source":[
        "Vehicles",
        "Buses",
        "Electricity"
    ],

    "Emissions":[
        vehicle_total,
        bus_total,
        electricity_total
    ]
})

st.bar_chart(distribution.set_index("Source"))

st.dataframe(distribution)

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption("SMU Sustainability Analytics Platform – Carbon Accounting Project")
