import streamlit as st
import pandas as pd
import numpy as np

# ----------------------------------
# PAGE CONFIGURATION
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
    st.markdown("Monitoring **Scope 1 and Scope 2 Emissions (2025)**")

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
# SIDEBAR
# ----------------------------------

st.sidebar.header("Dashboard Filters")

year = st.sidebar.selectbox(
    "Select Reporting Year",
    ["2025"]
)

# ----------------------------------
# SCOPE 1 SECTION
# ----------------------------------

st.header("🔥 Scope 1 Emissions")

st.write(
"""
Scope 1 emissions correspond to **direct greenhouse gas emissions** from
sources that are owned or controlled by the institution such as
fuel combustion or institutional vehicles.
"""
)

st.subheader("Scope 1 Data Table")
st.dataframe(scope1_df)

# KPI
if "Emission (kg CO2e)" in scope1_df.columns:
    
    total_scope1 = np.sum(scope1_df["Emission (kg CO2e)"])
    
    st.metric(
        label="Total Scope 1 Emissions",
        value=f"{total_scope1:,.0f} kg CO2e"
    )

# Simple chart without extra libraries
if "Emission (kg CO2e)" in scope1_df.columns:
    
    st.subheader("Scope 1 Emissions by Source")
    
    chart_data = scope1_df.set_index(scope1_df.columns[0])["Emission (kg CO2e)"]
    
    st.bar_chart(chart_data)

st.markdown("---")

# ----------------------------------
# SCOPE 2 SECTION
# ----------------------------------

st.header("⚡ Scope 2 Emissions")

st.write(
"""
Scope 2 emissions correspond to **indirect emissions from purchased electricity**
consumed by buildings and institutional facilities.
"""
)

st.subheader("Scope 2 Data Table")
st.dataframe(scope2_df)

# KPI
if "Emission (kg CO2e)" in scope2_df.columns:
    
    total_scope2 = np.sum(scope2_df["Emission (kg CO2e)"])
    
    st.metric(
        label="Total Scope 2 Emissions",
        value=f"{total_scope2:,.0f} kg CO2e"
    )

# Chart
if "Emission (kg CO2e)" in scope2_df.columns:
    
    st.subheader("Scope 2 Emissions by Source")
    
    chart_data2 = scope2_df.set_index(scope2_df.columns[0])["Emission (kg CO2e)"]
    
    st.bar_chart(chart_data2)

st.markdown("---")

# ----------------------------------
# TOTAL EMISSIONS SUMMARY
# ----------------------------------

st.header("📊 Emissions Summary")

scope1_total = 0
scope2_total = 0

if "Emission (kg CO2e)" in scope1_df.columns:
    scope1_total = np.sum(scope1_df["Emission (kg CO2e)"])

if "Emission (kg CO2e)" in scope2_df.columns:
    scope2_total = np.sum(scope2_df["Emission (kg CO2e)"])

summary_df = pd.DataFrame({
    "Scope": ["Scope 1", "Scope 2"],
    "Emissions (kg CO2e)": [scope1_total, scope2_total]
})

st.bar_chart(summary_df.set_index("Scope"))

st.markdown("---")

st.markdown(
"Dashboard developed for the **SMU Carbon Accounting Project – 2025**"
)
