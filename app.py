import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SMU Carbon Dashboard", layout="wide")

# -------------------------------------------------
# HEADER WITH LOGOS
# -------------------------------------------------

col1, col2, col3 = st.columns([1,3,1])

with col1:
    st.image("LOGO_SMU_2023_FINAL.png", width=140)

with col2:
    st.title("SMU Carbon Accounting Dashboard")
    st.write("Scope 1 and Scope 2 Emissions Monitoring – 2025")

with col3:
    st.image("carbon_jar_logo (1).jfif", width=120)

st.markdown("---")


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():

    scope1 = pd.read_csv("Carbon_Accounting_Medtech.csv")
    scope2 = pd.read_csv("Scope 2 Emissions (3).csv")

    # clean column names
    scope1.columns = scope1.columns.str.strip().str.lower()
    scope2.columns = scope2.columns.str.strip().str.lower()

    return scope1, scope2


scope1_df, scope2_df = load_data()


# -------------------------------------------------
# DETECT IMPORTANT COLUMNS AUTOMATICALLY
# -------------------------------------------------

def find_column(df, keywords):

    for col in df.columns:
        for key in keywords:
            if key in col:
                return col
    return None


building_col = find_column(scope2_df, ["building","site","location"])
consumption_col = find_column(scope2_df, ["consumption","kwh"])
meter_col = find_column(scope2_df, ["meter"])
month_col = find_column(scope2_df, ["month"])
emission_col = find_column(scope2_df, ["emission","co2"])


# -------------------------------------------------
# FIX NUMERIC COLUMNS
# -------------------------------------------------

if consumption_col:
    scope2_df[consumption_col] = pd.to_numeric(scope2_df[consumption_col], errors="coerce")

if meter_col:
    scope2_df[meter_col] = pd.to_numeric(scope2_df[meter_col], errors="coerce")

if emission_col:
    scope2_df[emission_col] = pd.to_numeric(scope2_df[emission_col], errors="coerce")


# -------------------------------------------------
# MONTH ORDER
# -------------------------------------------------

month_order = [
    "jan","feb","mar","apr","may","jun",
    "jul","aug","sep","oct","nov","dec"
]

if month_col:
    scope2_df[month_col] = scope2_df[month_col].astype(str).str.lower()

    scope2_df[month_col] = pd.Categorical(
        scope2_df[month_col],
        categories=month_order,
        ordered=True
    )


# -------------------------------------------------
# SCOPE 1 SECTION
# -------------------------------------------------

st.header("🔥 Scope 1 Emissions")

st.write("Direct emissions from fuels and owned sources.")

st.dataframe(scope1_df)


# KPI
if "emission" in "".join(scope1_df.columns):

    emission_column_scope1 = find_column(scope1_df, ["emission","co2"])

    total_scope1 = scope1_df[emission_column_scope1].sum()

    st.metric("Total Scope 1 Emissions", f"{total_scope1:,.0f} kgCO2e")


# Plot 1
st.subheader("Scope 1 Emissions Distribution")

if emission_column_scope1:
    st.bar_chart(scope1_df[emission_column_scope1])


st.markdown("---")


# -------------------------------------------------
# SCOPE 2 SECTION
# -------------------------------------------------

st.header("⚡ Scope 2 Emissions")

st.write("Indirect emissions from purchased electricity.")

st.dataframe(scope2_df)


# KPI

if emission_col:
    total_scope2 = scope2_df[emission_col].sum()
    st.metric("Total Scope 2 Emissions", f"{total_scope2:,.0f} kgCO2e")


# -------------------------------------------------
# PLOT 1 – EMISSIONS BY BUILDING
# -------------------------------------------------

if building_col and emission_col:

    st.subheader("Emissions by Building")

    emissions_building = scope2_df.groupby(building_col)[emission_col].sum()

    st.bar_chart(emissions_building)


# -------------------------------------------------
# PLOT 2 – ELECTRICITY CONSUMPTION
# -------------------------------------------------

if building_col and consumption_col:

    st.subheader("Electricity Consumption by Building")

    consumption_building = scope2_df.groupby(building_col)[consumption_col].sum()

    st.bar_chart(consumption_building)


# -------------------------------------------------
# PLOT 3 – MONTHLY CONSUMPTION
# -------------------------------------------------

if month_col and consumption_col:

    st.subheader("Monthly Electricity Consumption")

    monthly_consumption = scope2_df.groupby(month_col)[consumption_col].sum()

    st.line_chart(monthly_consumption)


# -------------------------------------------------
# PLOT 4 – MONTHLY EMISSIONS
# -------------------------------------------------

if month_col and emission_col:

    st.subheader("Monthly Scope 2 Emissions")

    monthly_emissions = scope2_df.groupby(month_col)[emission_col].sum()

    st.line_chart(monthly_emissions)


# -------------------------------------------------
# PLOT 5 – CONSUMPTION PER METER
# -------------------------------------------------

if consumption_col and meter_col and building_col:

    st.subheader("Consumption per Meter")

    scope2_df["consumption_per_meter"] = (
        scope2_df[consumption_col] /
        scope2_df[meter_col]
    )

    meter_chart = scope2_df.groupby(building_col)["consumption_per_meter"].mean()

    st.bar_chart(meter_chart)


st.markdown("---")


# -------------------------------------------------
# SCOPE COMPARISON
# -------------------------------------------------

st.header("Scope Comparison")

scope1_total = 0
scope2_total = 0

if emission_column_scope1:
    scope1_total = scope1_df[emission_column_scope1].sum()

if emission_col:
    scope2_total = scope2_df[emission_col].sum()

comparison = pd.DataFrame({
    "Scope":["Scope 1","Scope 2"],
    "Emissions":[scope1_total,scope2_total]
})

st.bar_chart(comparison.set_index("Scope"))


st.markdown("---")
st.caption("SMU Carbon Accounting Dashboard – 2025")
