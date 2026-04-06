import streamlit as st
import pandas as pd
import numpy as np

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="SMU Carbon Dashboard",
    layout="wide"
)

# ----------------------------------
# HEADER WITH LOGOS
# ----------------------------------

col1, col2, col3 = st.columns([1,2,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=150)

with col2:
    st.title("SMU Carbon Accounting Dashboard")
    st.markdown("Monitoring **Scope 1 and Scope 2 Emissions – 2025**")

with col3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.markdown("---")

# ----------------------------------
# LOAD DATA
# ----------------------------------

@st.cache_data
def load_data():

    scope1 = pd.read_csv("Carbon_Accounting_Medtech.csv")
    scope2 = pd.read_csv("Scope 2 Emissions (3).csv")

    scope1.columns = scope1.columns.str.strip()
    scope2.columns = scope2.columns.str.strip()

    return scope1, scope2

scope1_df, scope2_df = load_data()

# ----------------------------------
# MONTH ORDER (IMPORTANT)
# ----------------------------------

month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.header("Dashboard Filters")

year = st.sidebar.selectbox(
    "Reporting Year",
    ["2025"]
)

# ----------------------------------
# SCOPE 1 SECTION
# ----------------------------------

st.header("🔥 Scope 1 Emissions")

st.write(
"Scope 1 emissions correspond to **direct greenhouse gas emissions** "
"from sources owned or controlled by the institution."
)

st.subheader("Scope 1 Data")
st.dataframe(scope1_df)

# KPI
if "Emission (kg CO2e)" in scope1_df.columns:

    total_scope1 = np.sum(scope1_df["Emission (kg CO2e)"])

    st.metric(
        "Total Scope 1 Emissions",
        f"{total_scope1:,.0f} kg CO2e"
    )

# -------------------------------
# PLOT 1 : Emissions by Source
# -------------------------------

if "Emission (kg CO2e)" in scope1_df.columns:

    st.subheader("Emissions by Source")

    source_column = scope1_df.columns[0]

    source_chart = scope1_df.groupby(source_column)["Emission (kg CO2e)"].sum()

    st.bar_chart(source_chart)

# -------------------------------
# PLOT 2 : Monthly Emissions
# -------------------------------

if "Month" in scope1_df.columns:

    st.subheader("Monthly Emissions Trend")

    scope1_df["Month"] = pd.Categorical(
        scope1_df["Month"],
        categories=month_order,
        ordered=True
    )

    monthly = scope1_df.groupby("Month")["Emission (kg CO2e)"].sum()

    st.line_chart(monthly)

# -------------------------------
# PLOT 3 : Consumption vs Emissions
# -------------------------------

if "Consumption (kWh)" in scope1_df.columns and "Emission (kg CO2e)" in scope1_df.columns:

    st.subheader("Consumption vs Emissions")

    chart_data = scope1_df[["Consumption (kWh)", "Emission (kg CO2e)"]]

    st.bar_chart(chart_data)

st.markdown("---")

# ----------------------------------
# SCOPE 2 SECTION
# ----------------------------------

st.header("⚡ Scope 2 Emissions")

st.write(
"Scope 2 emissions correspond to **indirect emissions from purchased electricity** "
"consumed by buildings and facilities."
)

st.subheader("Scope 2 Data")
st.dataframe(scope2_df)

# KPI
if "Emission (kg CO2e)" in scope2_df.columns:

    total_scope2 = np.sum(scope2_df["Emission (kg CO2e)"])

    st.metric(
        "Total Scope 2 Emissions",
        f"{total_scope2:,.0f} kg CO2e"
    )

# -------------------------------
# PLOT 1 : Emissions by Building
# -------------------------------

if "Building" in scope2_df.columns:

    st.subheader("Emissions by Building")

    building_chart = scope2_df.groupby("Building")["Emission (kg CO2e)"].sum()

    st.bar_chart(building_chart)

# -------------------------------
# PLOT 2 : Monthly Electricity Emissions
# -------------------------------

if "Month" in scope2_df.columns:

    st.subheader("Monthly Electricity Emissions")

    scope2_df["Month"] = pd.Categorical(
        scope2_df["Month"],
        categories=month_order,
        ordered=True
    )

    monthly2 = scope2_df.groupby("Month")["Emission (kg CO2e)"].sum()

    st.line_chart(monthly2)

# -------------------------------
# PLOT 3 : Electricity Consumption
# -------------------------------

if "Consumption (kWh)" in scope2_df.columns:

    st.subheader("Electricity Consumption")

    consumption_chart = scope2_df.groupby("Month")["Consumption (kWh)"].sum()

    st.bar_chart(consumption_chart)

st.markdown("---")

# ----------------------------------
# GLOBAL EMISSIONS COMPARISON
# ----------------------------------

st.header("📊 Scope 1 vs Scope 2 Comparison")

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
"Dashboard developed for the **SMU Carbon Accounting Project – 2025**"
)
