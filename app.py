import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="SMU Carbon Dashboard",
    layout="wide"
)

# -----------------------------
# HEADER WITH LOGOS
# -----------------------------
col1, col2, col3 = st.columns([1,3,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=150)

with col2:
    st.title("SMU Carbon Accounting Dashboard")
    st.markdown("Monitoring **Scope 1 and Scope 2 Emissions – 2025**")

with col3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.markdown("---")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():

    scope1 = pd.read_csv("Carbon_Accounting_Medtech.csv")
    scope2 = pd.read_csv("Scope 2 Emissions (3).csv")

    scope1.columns = scope1.columns.str.strip()
    scope2.columns = scope2.columns.str.strip()

    return scope1, scope2

scope1_df, scope2_df = load_data()

# -----------------------------
# MONTH ORDER
# -----------------------------
month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

if "Building" in scope2_df.columns:

    building_filter = st.sidebar.multiselect(
        "Select Building",
        scope2_df["Building"].unique(),
        default=scope2_df["Building"].unique()
    )

    scope2_df = scope2_df[scope2_df["Building"].isin(building_filter)]

# -----------------------------
# SCOPE 1 SECTION
# -----------------------------
st.header("🔥 Scope 1 Emissions")

st.write("Direct emissions from sources owned or controlled by SMU.")

st.dataframe(scope1_df)

# KPIs
if "Emission (kg CO2e)" in scope1_df.columns:

    total_scope1 = np.sum(scope1_df["Emission (kg CO2e)"])

    st.metric("Total Scope 1 Emissions", f"{total_scope1:,.0f} kg CO2e")

# -----------------------------
# PLOT 1 : Emissions by Source
# -----------------------------
if "Emission (kg CO2e)" in scope1_df.columns:

    st.subheader("Emissions by Source")

    source_col = scope1_df.columns[0]

    emissions_by_source = scope1_df.groupby(source_col)["Emission (kg CO2e)"].sum()

    st.bar_chart(emissions_by_source)

# -----------------------------
# PLOT 2 : Monthly Emissions
# -----------------------------
if "Month" in scope1_df.columns:

    st.subheader("Monthly Emissions")

    scope1_df["Month"] = pd.Categorical(
        scope1_df["Month"],
        categories=month_order,
        ordered=True
    )

    monthly_scope1 = scope1_df.groupby("Month")["Emission (kg CO2e)"].sum()

    st.line_chart(monthly_scope1)

# -----------------------------
# PLOT 3 : Consumption vs Emissions
# -----------------------------
if "Consumption (kWh)" in scope1_df.columns:

    st.subheader("Consumption vs Emissions")

    chart_data = scope1_df[["Consumption (kWh)", "Emission (kg CO2e)"]]

    st.bar_chart(chart_data)

# -----------------------------
# PLOT 4 : Emissions Distribution
# -----------------------------
if "Emission (kg CO2e)" in scope1_df.columns:

    st.subheader("Emission Distribution")

    distribution = scope1_df["Emission (kg CO2e)"]

    st.bar_chart(distribution)

st.markdown("---")

# -----------------------------
# SCOPE 2 SECTION
# -----------------------------
st.header("⚡ Scope 2 Emissions")

st.write("Indirect emissions from purchased electricity.")

st.dataframe(scope2_df)

# KPIs
if "Emission (kg CO2e)" in scope2_df.columns:

    total_scope2 = np.sum(scope2_df["Emission (kg CO2e)"])

    st.metric("Total Scope 2 Emissions", f"{total_scope2:,.0f} kg CO2e")

# -----------------------------
# PLOT 1 : Emissions by Building
# -----------------------------
if "Building" in scope2_df.columns:

    st.subheader("Emissions by Building")

    building_emissions = scope2_df.groupby("Building")["Emission (kg CO2e)"].sum()

    st.bar_chart(building_emissions)

# -----------------------------
# PLOT 2 : Electricity Consumption by Building
# -----------------------------
if "Consumption (kWh)" in scope2_df.columns:

    st.subheader("Electricity Consumption by Building")

    consumption_building = scope2_df.groupby("Building")["Consumption (kWh)"].sum()

    st.bar_chart(consumption_building)

# -----------------------------
# PLOT 3 : Monthly Electricity Consumption
# -----------------------------
if "Month" in scope2_df.columns:

    st.subheader("Monthly Electricity Consumption")

    scope2_df["Month"] = pd.Categorical(
        scope2_df["Month"],
        categories=month_order,
        ordered=True
    )

    monthly_consumption = scope2_df.groupby("Month")["Consumption (kWh)"].sum()

    st.line_chart(monthly_consumption)

# -----------------------------
# PLOT 4 : Monthly Scope 2 Emissions
# -----------------------------
if "Month" in scope2_df.columns:

    st.subheader("Monthly Scope 2 Emissions")

    monthly_emissions = scope2_df.groupby("Month")["Emission (kg CO2e)"].sum()

    st.line_chart(monthly_emissions)

# -----------------------------
# PLOT 5 : Consumption per Meter
# -----------------------------
if "Number of meters" in scope2_df.columns:

    st.subheader("Consumption per Meter")

    scope2_df["Consumption per meter"] = (
        scope2_df["Consumption (kWh)"] /
        scope2_df["Number of meters"]
    )

    meter_chart = scope2_df.groupby("Building")["Consumption per meter"].mean()

    st.bar_chart(meter_chart)

st.markdown("---")

# -----------------------------
# GLOBAL COMPARISON
# -----------------------------
st.header("📊 Scope Comparison")

scope1_total = 0
scope2_total = 0

if "Emission (kg CO2e)" in scope1_df.columns:
    scope1_total = np.sum(scope1_df["Emission (kg CO2e)"])

if "Emission (kg CO2e)" in scope2_df.columns:
    scope2_total = np.sum(scope2_df["Emission (kg CO2e)"])

comparison_df = pd.DataFrame({
    "Scope": ["Scope 1","Scope 2"],
    "Emissions": [scope1_total, scope2_total]
})

st.bar_chart(comparison_df.set_index("Scope"))

st.markdown("---")

st.markdown(
"SMU Sustainability Monitoring Dashboard – Carbon Accounting Project 2025"
)
