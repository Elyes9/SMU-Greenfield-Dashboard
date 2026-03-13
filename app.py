import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Carbon Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HEADER ---
st.title("🌍 Carbon Emissions Dashboard")
st.markdown("Explore carbon emissions data interactively with filters and charts.")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Example dataset: OWID CO₂ data
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    df = pd.read_csv(url)
    # Keep only a few relevant columns for simplicity
    df = df[["country", "year", "co2", "co2_per_capita", "population"]]
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
countries = df["country"].unique()
selected_countries = st.sidebar.multiselect(
    "Select countries", countries, default=["World"]
)

years = df["year"].unique()
selected_year_range = st.sidebar.slider(
    "Select year range",
    int(min(years)),
    int(max(years)),
    (2000, 2023)
)

# Filter data
df_filtered = df[df["country"].isin(selected_countries)]
df_filtered = df_filtered[
    (df_filtered["year"] >= selected_year_range[0]) &
    (df_filtered["year"] <= selected_year_range[1])
]

# --- MAIN DASHBOARD ---
st.markdown("## 📊 CO₂ Emissions Over Time")

# Line chart using Streamlit
for country in selected_countries:
    df_country = df_filtered[df_filtered["country"] == country]
    st.line_chart(df_country.set_index("year")["co2"], height=300, width=700)

# Bar chart for latest year
latest_year = df_filtered["year"].max()
df_latest = df_filtered[df_filtered["year"] == latest_year]

st.markdown(f"## 📈 CO₂ Emissions by Country in {latest_year}")

# Bar chart using Streamlit
st.bar_chart(df_latest.set_index("country")["co2"], height=400)

# --- KPI METRICS ---
st.markdown(f"## 📌 Key Metrics ({latest_year})")

total_co2 = np.sum(df_latest["co2"])
avg_per_capita = np.mean(df_latest["co2_per_capita"].dropna())

col1, col2 = st.columns(2)
col1.metric("🌐 Total CO₂ Emissions (Mt)", f"{total_co2:,.0f}")
col2.metric("👤 Average CO₂ per Capita (t)", f"{avg_per_capita:.2f}")

# --- RAW DATA ---
with st.expander("View Raw Data"):
    st.dataframe(df_filtered)

st.markdown("---")
st.caption("Data source: Our World in Data (https://ourworldindata.org/co2-emissions)")
