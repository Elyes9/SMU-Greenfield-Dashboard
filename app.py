import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="MedTech Carbon Dashboard",
    layout="wide"
)

st.title("🌍 MedTech Carbon Emissions Dashboard")
st.markdown("Monitoring Scope 1 and Scope 2 emissions for 2025")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    scope1 = pd.read_csv("Carbon_Accounting_Medtech.csv")
    scope2 = pd.read_csv("Scope 2 Emissions (3).csv")
    return scope1, scope2

scope1_df, scope2_df = load_data()

# -----------------------------
# CLEAN COLUMN NAMES
# -----------------------------
scope1_df.columns = scope1_df.columns.str.strip()
scope2_df.columns = scope2_df.columns.str.strip()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    [2025]
)

# -----------------------------
# SCOPE 1 SECTION
# -----------------------------
st.header("🔥 Scope 1 Emissions")

st.markdown(
"""
Scope 1 includes **direct emissions from sources owned or controlled by the institution**, 
such as fuel consumption from company vehicles or on-site combustion.
"""
)

# Show data
st.subheader("Scope 1 Data Overview")
st.dataframe(scope1_df)

# Scope 1 chart
if "Emission (kg CO2e)" in scope1_df.columns:

    fig_scope1 = px.bar(
        scope1_df,
        x=scope1_df.columns[0],
        y="Emission (kg CO2e)",
        title="Scope 1 Emissions Distribution"
    )

    st.plotly_chart(fig_scope1, use_container_width=True)

# KPI
if "Emission (kg CO2e)" in scope1_df.columns:
    total_scope1 = scope1_df["Emission (kg CO2e)"].sum()

    st.metric(
        label="Total Scope 1 Emissions",
        value=f"{total_scope1:,.0f} kg CO2e"
    )

# -----------------------------
# SCOPE 2 SECTION
# -----------------------------
st.header("⚡ Scope 2 Emissions")

st.markdown(
"""
Scope 2 emissions come from **purchased electricity, heating, or cooling** 
consumed by the organization.
"""
)

# Show scope 2 data
st.subheader("Scope 2 Data Overview")
st.dataframe(scope2_df)

# Chart
if "Emission (kg CO2e)" in scope2_df.columns:

    fig_scope2 = px.bar(
        scope2_df,
        x=scope2_df.columns[0],
        y="Emission (kg CO2e)",
        title="Scope 2 Emissions Distribution"
    )

    st.plotly_chart(fig_scope2, use_container_width=True)

# KPI
if "Emission (kg CO2e)" in scope2_df.columns:
    total_scope2 = scope2_df["Emission (kg CO2e)"].sum()

    st.metric(
        label="Total Scope 2 Emissions",
        value=f"{total_scope2:,.0f} kg CO2e"
    )

# -----------------------------
# COMPARISON SECTION
# -----------------------------
st.header("📊 Scope Comparison")

comparison_df = pd.DataFrame({
    "Scope": ["Scope 1", "Scope 2"],
    "Emissions": [
        scope1_df["Emission (kg CO2e)"].sum() if "Emission (kg CO2e)" in scope1_df.columns else 0,
        scope2_df["Emission (kg CO2e)"].sum() if "Emission (kg CO2e)" in scope2_df.columns else 0
    ]
})

fig_compare = px.pie(
    comparison_df,
    names="Scope",
    values="Emissions",
    title="Share of Scope 1 vs Scope 2 Emissions"
)

st.plotly_chart(fig_compare, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("Developed for the MedTech Carbon Accounting Project (2025)")
