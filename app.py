import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="SMU Carbon Dashboard",
    layout="wide"
)

# --------------------------------------------------
# GREEN THEME
# --------------------------------------------------

st.markdown("""
<style>

.main {
background-color:#f6fbf7;
}

h1,h2,h3 {
color:#1b5e20;
}

[data-testid="stMetricValue"]{
color:#1b5e20;
font-size:30px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_scope2():
    df = pd.read_csv("Scope 2 Emissions (3).csv")
    df.columns = df.columns.str.strip()
    return df


@st.cache_data
def load_scope1():
    df = pd.read_csv("Carbon_Accounting_Medtech.csv")
    df.columns = df.columns.str.strip()
    return df


scope2 = load_scope2()
scope1 = load_scope1()

# --------------------------------------------------
# HEADER WITH LOGOS
# --------------------------------------------------

col1, col2, col3 = st.columns([1,4,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=120)

with col2:
    st.title("SMU Carbon Emissions Dashboard")
    st.write("Monitoring Scope 1 and Scope 2 emissions for 2025")

with col3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.divider()

# --------------------------------------------------
# FIND IMPORTANT COLUMNS AUTOMATICALLY
# --------------------------------------------------

def detect_column(df, keywords):
    for col in df.columns:
        for k in keywords:
            if k in col.lower():
                return col
    return None


month_col = detect_column(scope2, ["month","period"])
cons_col = detect_column(scope2, ["consumption","kwh"])
building_col = detect_column(scope2, ["building"])
meter_col = detect_column(scope2, ["meter"])

emission_col = detect_column(scope1, ["co2","emission"])

# --------------------------------------------------
# CLEAN NUMERIC DATA
# --------------------------------------------------

if cons_col:
    scope2[cons_col] = pd.to_numeric(scope2[cons_col], errors="coerce").fillna(0)

if meter_col:
    scope2[meter_col] = pd.to_numeric(scope2[meter_col], errors="coerce").fillna(1)

if emission_col:
    scope1[emission_col] = pd.to_numeric(scope1[emission_col], errors="coerce").fillna(0)

# --------------------------------------------------
# MONTH ORDER
# --------------------------------------------------

month_order = [
"Jan","Feb","Mar","Apr","May","Jun",
"Jul","Aug","Sep","Oct","Nov","Dec"
]

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

if building_col:
    buildings = st.sidebar.multiselect(
        "Select Buildings",
        scope2[building_col].unique(),
        default=scope2[building_col].unique()
    )
    scope2 = scope2[scope2[building_col].isin(buildings)]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_consumption = scope2[cons_col].sum()

if emission_col:
    total_scope1 = scope1[emission_col].sum()
else:
    total_scope1 = 0

emission_factor = 0.233
scope2["CO2"] = scope2[cons_col] * emission_factor

total_scope2 = scope2["CO2"].sum()

k1,k2,k3 = st.columns(3)

k1.metric(
"Scope 1 Emissions",
f"{total_scope1:,.0f} kgCO₂"
)

k2.metric(
"Electricity Consumption",
f"{total_consumption:,.0f} kWh"
)

k3.metric(
"Scope 2 Emissions",
f"{total_scope2:,.0f} kgCO₂"
)

st.divider()

# --------------------------------------------------
# SCOPE 2 VISUALIZATION
# --------------------------------------------------

st.header("Scope 2 – Electricity Emissions")

# MONTHLY TREND

if month_col:

    scope2[month_col] = scope2[month_col].astype(str)

    monthly = scope2.groupby(month_col)[cons_col].sum()

    monthly = monthly.reindex(month_order)

    st.subheader("Monthly Electricity Consumption")

    st.line_chart(monthly)


# BUILDING CONSUMPTION

if building_col:

    building_use = scope2.groupby(building_col)[cons_col].sum()

    st.subheader("Electricity Consumption by Building")

    st.bar_chart(building_use)


# TOP METERS

if meter_col:

    scope2["Consumption_per_meter"] = scope2[cons_col] / scope2[meter_col]

    top_meters = scope2.sort_values(
        "Consumption_per_meter",
        ascending=False
    ).head(10)

    st.subheader("Top Electricity Meters")

    st.bar_chart(top_meters["Consumption_per_meter"])

# CO2 EMISSIONS TREND

if month_col:

    emissions_month = scope2.groupby(month_col)["CO2"].sum()

    emissions_month = emissions_month.reindex(month_order)

    st.subheader("Scope 2 CO₂ Emissions Trend")

    st.area_chart(emissions_month)

st.divider()

# --------------------------------------------------
# SCOPE 1 SECTION
# --------------------------------------------------

st.header("Scope 1 – Direct Emissions")

if emission_col:

    st.subheader("Scope 1 Emissions Distribution")

    st.bar_chart(scope1[emission_col])

    st.subheader("Scope 1 Dataset")

    st.dataframe(scope1)

else:
    st.warning("No emission column detected in Scope 1 dataset.")

st.divider()

st.success("SMU Carbon Dashboard Loaded Successfully")
