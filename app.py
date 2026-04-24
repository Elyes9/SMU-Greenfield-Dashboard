import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GHG Carbon Monitor · 2025",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM — dark refined theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  /* ── App background ── */
  .stApp {
    background: #0E1117;
    color: #E8EDF2;
  }
  .block-container {
    padding: 1.6rem 2.2rem 2rem 2.2rem;
    max-width: 100%;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: #13181F;
    border-right: 1px solid #1E2730;
  }
  [data-testid="stSidebar"] * {
    color: #C8D4DF !important;
  }
  [data-testid="stSidebar"] .stNumberInput input,
  [data-testid="stSidebar"] .stSelectbox select {
    background: #1A2230 !important;
    border: 1px solid #2A3850 !important;
    color: #E8EDF2 !important;
    border-radius: 6px !important;
  }

  /* ── Metric cards ── */
  [data-testid="stMetric"] {
    background: linear-gradient(135deg, #141B26 0%, #0F1520 100%);
    border: 1px solid #1E2D3D;
    border-radius: 12px;
    padding: 16px 20px;
    position: relative;
    overflow: hidden;
  }
  [data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00C9A7, #0096FF);
  }
  [data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    color: #6B8BA4 !important;
  }
  [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    color: #E8EDF2 !important;
  }
  [data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    color: #00C9A7 !important;
  }

  /* ── Tabs ── */
  [data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1E2D3D !important;
    gap: 4px;
  }
  [data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    color: #4E6A82 !important;
    background: transparent !important;
    border: none !important;
    padding: 10px 18px !important;
    border-radius: 6px 6px 0 0 !important;
    transition: color .2s;
  }
  [data-testid="stTabs"] [aria-selected="true"] {
    color: #00C9A7 !important;
    border-bottom: 2px solid #00C9A7 !important;
    background: rgba(0,201,167,.06) !important;
  }

  /* ── Section labels ── */
  .sec-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #4E6A82;
    margin: 18px 0 8px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1E2D3D 0%, transparent 100%);
  }

  /* ── Page title ── */
  .dash-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #E8EDF2;
    letter-spacing: -.02em;
    line-height: 1.1;
    margin-bottom: 2px;
  }
  .dash-sub {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #4E6A82;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: 1.4rem;
  }

  /* ── Insight cards ── */
  .insight-card {
    background: linear-gradient(135deg, #141B26 0%, #0F1B24 100%);
    border: 1px solid #1E2D3D;
    border-left: 3px solid #00C9A7;
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 13px;
    color: #A8BDC9;
    line-height: 1.65;
    height: 100%;
  }
  .insight-card strong {
    display: block;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 14px;
    color: #E8EDF2;
    margin-bottom: 4px;
  }
  .insight-card.orange { border-left-color: #FF8C42; }
  .insight-card.blue   { border-left-color: #0096FF; }

  /* ── Badges ── */
  .badge-s1 {
    background: rgba(0,150,255,.15);
    color: #4AACFF;
    border: 1px solid rgba(0,150,255,.25);
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: .08em;
    text-transform: uppercase;
    display: inline-block;
  }
  .badge-s2 {
    background: rgba(0,201,167,.12);
    color: #00C9A7;
    border: 1px solid rgba(0,201,167,.22);
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: .08em;
    text-transform: uppercase;
    display: inline-block;
  }

  /* ── Divider ── */
  hr {
    border: none !important;
    border-top: 1px solid #1E2D3D !important;
    margin: 1rem 0 !important;
  }

  /* ── DataFrames ── */
  [data-testid="stDataFrame"] {
    border: 1px solid #1E2D3D;
    border-radius: 10px;
    overflow: hidden;
  }

  /* ── Caption ── */
  .stCaption {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    color: #3D5467 !important;
    letter-spacing: .05em !important;
  }

  /* ── Checkbox ── */
  [data-testid="stCheckbox"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: .04em !important;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: #0E1117; }
  ::-webkit-scrollbar-thumb { background: #1E2D3D; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ALTAIR DARK THEME
# ─────────────────────────────────────────────────────────────────────────────
DARK_BG   = "#0E1117"
DARK_CARD = "#141B26"
GRID_COL  = "#1E2D3D"
TEXT_COL  = "#6B8BA4"
TEXT_MAIN = "#C8D4DF"

def dark_theme():
    return {
        "config": {
            "background": "transparent",
            "view": {"fill": "transparent", "stroke": "transparent"},
            "axis": {
                "domainColor": GRID_COL,
                "gridColor": GRID_COL,
                "tickColor": GRID_COL,
                "labelColor": TEXT_COL,
                "titleColor": TEXT_COL,
                "labelFont": "DM Mono, monospace",
                "titleFont": "DM Mono, monospace",
                "labelFontSize": 10,
                "titleFontSize": 10,
                "gridOpacity": 0.6,
            },
            "legend": {
                "labelColor": TEXT_MAIN,
                "titleColor": TEXT_COL,
                "labelFont": "DM Mono, monospace",
                "titleFont": "DM Mono, monospace",
                "labelFontSize": 10,
                "titleFontSize": 10,
            },
            "title": {"color": TEXT_MAIN, "font": "Syne, sans-serif"},
            "point": {"filled": True},
            "mark": {"tooltip": True},
        }
    }

alt.themes.register("dark_carbon", dark_theme)
alt.themes.enable("dark_carbon")

# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
C_S1    = "#0096FF"   # blue  — Scope 1
C_S2    = "#00C9A7"   # teal  — Scope 2
C_TOT   = "#FF8C42"   # amber — Total
C_CUM   = "#B57BFF"   # violet — Cumulative
C_ROLL  = "#FF4FA0"   # pink  — Rolling avg
C_PROJ  = "#FFD166"   # gold  — Projection
C_TARGET= "#EF4444"   # red   — Target
C_INT   = "#06D6A0"   # mint  — Intensity

MONTHS     = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTH_NUMS = list(range(1, 13))

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Emission Factors")
    ef_diesel   = st.number_input("Diesel (kgCO₂e / L)",   value=2.68,  step=0.01,  format="%.3f")
    ef_gasoline = st.number_input("Gasoline (kgCO₂e / L)", value=2.31,  step=0.01,  format="%.3f")
    ef_bus_km   = st.number_input("Bus/Van (kgCO₂e / km)", value=0.089, step=0.001, format="%.4f")
    ef_grid     = st.number_input("Grid (kgCO₂e / kWh)",   value=0.267, step=0.001, format="%.4f")
    ef_hvac     = st.number_input("HVAC gas (kgCO₂e / kWh)", value=0.198, step=0.001, format="%.3f",
                                   help="Natural gas combustion EF for HVAC heating load")

    st.markdown("---")
    st.markdown("### 🎛️ Chart overlays")
    show_rolling = st.checkbox("3-month rolling average", value=True)
    show_target  = st.checkbox("Reduction target (−10%)", value=True)
    show_proj    = st.checkbox("Linear projection",        value=True)
    show_band    = st.checkbox("Confidence band",          value=True)
    interp       = st.selectbox("Line interpolation", ["monotone","linear","step","basis"], index=0)

    st.markdown("---")
    st.markdown("**Framework** · GHG Protocol")
    st.markdown("**Year** · 2025")
    st.markdown("**Grid** · Tunisia STEG")
    st.markdown('<span class="badge-s1">Scope 1</span> &nbsp; Mobile combustion + HVAC', unsafe_allow_html=True)
    st.markdown('<span class="badge-s2">Scope 2</span> &nbsp; Purchased electricity', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# RAW DATA
# ─────────────────────────────────────────────────────────────────────────────
elec_kwh = np.array([28429,30287,30262,19625,22097,37937,
                     48569,43843,38143,28139,23532,23039], dtype=float)

vehicle_raw = pd.DataFrame({
    "Date":      ["Feb 3, 2025","Feb 6, 2025","Dec 31, 2025"],
    "Month_num": [2, 2, 12],
    "Source":    ["Unknown fleet","Peugeot Bipper","Peugeot Bipper"],
    "Fuel_type": ["Diesel","Super Gasoline","Super Gasoline"],
    "Vouchers":  [96, 96, 96],
    "Total_DT":  [3840, 3840, 3840],
    "Liters":    [1741.496599, 1520.792079, 1520.792079],
})
vehicle_raw["EF"]    = np.where(vehicle_raw["Fuel_type"]=="Diesel", ef_diesel, ef_gasoline)
vehicle_raw["tCO2e"] = vehicle_raw["Liters"] * vehicle_raw["EF"] / 1000

bus_raw = pd.DataFrame({
    "Date":        ["Feb 4, 2025","Oct 1, 2025","Nov 4, 2025","Nov 12, 2025","Nov 15, 2025"],
    "Month_num":   [2, 10, 11, 11, 11],
    "Destination": ["BAKO MOTORS Fouchana","SOFTEN Grombalia",
                    "BAKO MOTORS Fouchana","STEG Radés","BOOTCAMP"],
    "Source":      ["S-CAPADE Van","S-CAPADE Bus","S-CAPADE Bus","S-CAPADE Bus","S-CAPADE Bus"],
    "Fuel":        ["Gasoil 50"]*5,
    "Distance_km": [22.7, 53.2, 22.7, 14.6, 11.3],
})
bus_raw["tCO2e"] = bus_raw["Distance_km"] * ef_bus_km / 1000

# HVAC — Medtech heating & cooling loads (kWh)
# Heating = natural gas combustion → Scope 1
# Cooling = electrically driven     → Scope 2 (tracked separately via grid meter)
hvac_heating_kwh = np.array([2287.5, 2316.8, 2391.0, 2415.5,    0,    0,
                                  0,      0,      0,      0, 2349.1, 2305.8])
hvac_cooling_kwh = np.array([   0,      0,      0,      0, 2445.0, 2500.0,
                              2502.3, 2498.5, 2456.8, 2403.7,    0,     0])
HVAC_HOURS_PER_MONTH = 1700  # average working hours

hvac_df = pd.DataFrame({
    "Month":          MONTHS,
    "Month_num":      MONTH_NUMS,
    "Heating_kWh":    hvac_heating_kwh,
    "Cooling_kWh":    hvac_cooling_kwh,
})
# Heating combustion → tCO2e (natural gas, Scope 1)
hvac_df["Heating_tCO2e"] = hvac_df["Heating_kWh"] * ef_hvac / 1000
# Cooling via electricity → tCO2e (Scope 2 — informational, already in grid meter)
hvac_df["Cooling_tCO2e"] = hvac_df["Cooling_kWh"] * ef_grid / 1000
hvac_df["Total_kWh"]     = hvac_df["Heating_kWh"] + hvac_df["Cooling_kWh"]
hvac_df["Month"] = pd.Categorical(hvac_df["Month"], categories=MONTHS, ordered=True)

total_hvac_heating = hvac_df["Heating_tCO2e"].sum()
total_hvac_cooling = hvac_df["Cooling_tCO2e"].sum()
hvac_s1_monthly    = hvac_df["Heating_tCO2e"].values  # only heating is Scope 1

elec_df = pd.DataFrame({
    "Month":     MONTHS,
    "Month_num": MONTH_NUMS,
    "kWh":       elec_kwh,
    "Meters":    np.full(12, 15),
})
elec_df["MWh"]   = elec_df["kWh"] / 1000
elec_df["tCO2e"] = elec_df["kWh"] * ef_grid / 1000

# ─────────────────────────────────────────────────────────────────────────────
# COMPUTED SERIES
# ─────────────────────────────────────────────────────────────────────────────
total_s2      = elec_df["tCO2e"].sum()
total_s1v     = vehicle_raw["tCO2e"].sum()
total_s1b     = bus_raw["tCO2e"].sum()
total_s1hvac  = total_hvac_heating
total_s1      = total_s1v + total_s1b + total_s1hvac
total_all     = total_s1 + total_s2
total_kwh     = int(elec_kwh.sum())

s1_monthly = np.zeros(12)
for _, row in vehicle_raw.iterrows():
    s1_monthly[int(row["Month_num"])-1] += row["tCO2e"]
for _, row in bus_raw.iterrows():
    s1_monthly[int(row["Month_num"])-1] += row["tCO2e"]
# Add HVAC heating to Scope 1
s1_monthly = s1_monthly + hvac_s1_monthly

s2_monthly    = elec_df["tCO2e"].values.copy()
total_monthly = s1_monthly + s2_monthly

def rolling_n(arr, n=3):
    s = pd.Series(arr)
    return s.rolling(n, center=True, min_periods=1).mean().values

roll_s1    = rolling_n(s1_monthly)
roll_s2    = rolling_n(s2_monthly)
roll_total = rolling_n(total_monthly)

# Rolling std for confidence band
roll_std  = rolling_n(np.array([abs(v - total_monthly.mean()) for v in total_monthly]))

cum_s1    = np.cumsum(s1_monthly)
cum_s2    = np.cumsum(s2_monthly)
cum_total = np.cumsum(total_monthly)

intensity = s2_monthly * 1000 / elec_kwh  # kgCO2e/kWh

# Linear trend on Scope 2
x_fit = np.arange(12, dtype=float)
slope2, intercept2 = np.polyfit(x_fit, s2_monthly, 1)
proj_s2 = slope2 * x_fit + intercept2

# Linear trend on Total
slopeT, interceptT = np.polyfit(x_fit, total_monthly, 1)
proj_total = slopeT * x_fit + interceptT

# Target: −10% from mean per month
target_monthly = np.full(12, total_monthly.mean() * 0.90)

# MoM change
mom_change = np.concatenate([[np.nan],
    np.diff(total_monthly) / total_monthly[:-1] * 100])

# Seasonal index (ratio to 12-month mean)
seasonal_idx = total_monthly / total_monthly.mean()

# Efficiency score: lower = better (inverse normalised intensity)
efficiency = 1 - (intensity - intensity.min()) / (intensity.max() - intensity.min() + 1e-9)

# Confidence band (±0.5 std dev of rolling window)
band_upper = roll_total + roll_std * 0.5
band_lower = np.maximum(roll_total - roll_std * 0.5, 0)

# Master DataFrame
trend_df = pd.DataFrame({
    "Month":       MONTHS,
    "Month_num":   MONTH_NUMS,
    "Scope1":      s1_monthly,
    "Scope2":      s2_monthly,
    "Total":       total_monthly,
    "HVAC_S1":     hvac_s1_monthly,
    "Roll_S1":     roll_s1,
    "Roll_S2":     roll_s2,
    "Roll_Total":  roll_total,
    "Band_Upper":  band_upper,
    "Band_Lower":  band_lower,
    "Cum_S1":      cum_s1,
    "Cum_S2":      cum_s2,
    "Cum_Total":   cum_total,
    "Intensity":   intensity,
    "Proj_S2":     proj_s2,
    "Proj_Total":  proj_total,
    "Target":      target_monthly,
    "MoM_Change":  mom_change,
    "Seasonal":    seasonal_idx,
    "Efficiency":  efficiency,
    "kWh":         elec_kwh,
    "Pct_Annual":  cum_total / total_all * 100,
})
trend_df["Month"] = pd.Categorical(trend_df["Month"], categories=MONTHS, ordered=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def mx():
    return alt.X("Month:N", sort=MONTHS, title=None,
                 axis=alt.Axis(labelAngle=0, labelFontSize=10,
                               tickColor="transparent"))

def smooth_line(df, y_col, color, width=2.5, dash=None, opacity=1.0, label=None):
    props = dict(color=color, strokeWidth=width, opacity=opacity,
                 interpolate=interp)
    if dash:
        props["strokeDash"] = dash
    encode = dict(
        x=mx(),
        y=alt.Y(f"{y_col}:Q", title="tCO₂e"),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip(f"{y_col}:Q", format=".4f", title=label or y_col)],
    )
    return alt.Chart(df).mark_line(**props).encode(**encode)

def glow_point(df, y_col, color, size=60):
    return alt.Chart(df).mark_point(
        color=color, filled=True, size=size, opacity=0.9
    ).encode(
        x=mx(),
        y=alt.Y(f"{y_col}:Q"),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip(f"{y_col}:Q", format=".4f")],
    )

def area_chart(df, y_col, color, opacity=0.12, y_title="tCO₂e"):
    return alt.Chart(df).mark_area(
        color=color, opacity=opacity,
        line={"color": color, "strokeWidth": 2, "opacity": 0.9},
        interpolate=interp,
    ).encode(
        x=mx(),
        y=alt.Y(f"{y_col}:Q", title=y_title),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip(f"{y_col}:Q", format=".4f", title=y_title)],
    )

def rule_line(val, color, dash=[5,3]):
    return alt.Chart(pd.DataFrame({"y":[val]})).mark_rule(
        color=color, strokeDash=dash, strokeWidth=1.2, opacity=0.7
    ).encode(y="y:Q")

def h_props(h=300):
    return {"height": h}

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="dash-title">🌿 GHG Carbon Monitor</div>', unsafe_allow_html=True)
st.markdown('<div class="dash-sub">GHG Protocol · Scope 1 & 2 · Tunisia · Reporting Year 2025</div>', unsafe_allow_html=True)

# KPI STRIP
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Grand Total",       f"{total_all:.2f}",              "tCO₂e · S1+S2")
k2.metric("Scope 1",           f"{total_s1:.3f}",               "tCO₂e · mobile+HVAC")
k3.metric("Scope 2",           f"{total_s2:.2f}",               "tCO₂e · electricity")
k4.metric("HVAC Heating S1",   f"{total_s1hvac:.3f}",           "tCO₂e · combustion")
k5.metric("Avg Intensity",     f"{intensity.mean():.3f}",       "kgCO₂e / kWh")
k6.metric("S2 Share",          f"{total_s2/total_all*100:.1f}%","of total emissions")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "◉ Overview",
    "〰 Trend & Curves",
    "∫ Cumulative",
    "⧖ Seasonality",
    "🚗 Scope 1",
    "⚡ Scope 2",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns([1, 1.6])

    with col_l:
        st.markdown('<div class="sec-label">Emissions split by scope</div>', unsafe_allow_html=True)
        donut_df = pd.DataFrame({
            "Scope": ["S1 · Mobile Combustion", "S1 · HVAC Heating", "Scope 2 · Electricity"],
            "tCO2e": [round(total_s1v+total_s1b,4), round(total_s1hvac,4), round(total_s2,4)],
            "Pct":   [round((total_s1v+total_s1b)/total_all*100,1),
                      round(total_s1hvac/total_all*100,1),
                      round(total_s2/total_all*100,1)],
        })
        arc = alt.Chart(donut_df).mark_arc(innerRadius=75, outerRadius=130, padAngle=0.02).encode(
            theta=alt.Theta("tCO2e:Q"),
            color=alt.Color("Scope:N",
                scale=alt.Scale(domain=donut_df["Scope"].tolist(),
                                range=[C_S1, "#FF8C42", C_S2]),
                legend=alt.Legend(orient="bottom", labelLimit=350,
                                  symbolType="circle", symbolSize=80)),
            tooltip=[alt.Tooltip("Scope:N"),
                     alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e"),
                     alt.Tooltip("Pct:Q",   format=".1f",  title="%")],
        ).properties(height=300)
        st.altair_chart(arc, use_container_width=True)

    with col_r:
        st.markdown('<div class="sec-label">Monthly stacked emissions — Scope 1 + Scope 2</div>', unsafe_allow_html=True)
        ov_long = trend_df[["Month","Scope1","Scope2"]].melt(
            id_vars="Month", value_vars=["Scope1","Scope2"],
            var_name="Scope", value_name="tCO2e")
        ov_long["Scope"] = ov_long["Scope"].map({"Scope1":"Scope 1","Scope2":"Scope 2"})

        stacked_bars = alt.Chart(ov_long).mark_bar(
            cornerRadiusTopLeft=4, cornerRadiusTopRight=4, width={"band": 0.7}
        ).encode(
            x=mx(),
            y=alt.Y("tCO2e:Q", stack="zero", title="tCO₂e"),
            color=alt.Color("Scope:N",
                scale=alt.Scale(domain=["Scope 1","Scope 2"],
                                range=[C_S1, C_S2]),
                legend=alt.Legend(orient="top", title=None)),
            tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Scope:N"),
                     alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e")],
        )
        total_line = smooth_line(trend_df, "Total", C_TOT, 2, label="Total")
        total_pts  = glow_point(trend_df, "Total", C_TOT, 45)
        st.altair_chart((stacked_bars + total_line + total_pts).properties(**h_props(300)),
                        use_container_width=True)

    # Source breakdown
    st.markdown('<div class="sec-label">Scope 1 — emission source breakdown</div>', unsafe_allow_html=True)
    src_df = pd.DataFrame({
        "Source":   ["Diesel (fleet)","Gasoline Feb","Gasoline Dec","Bus/Van trips","HVAC Heating"],
        "tCO2e":    [
            vehicle_raw.loc[vehicle_raw["Fuel_type"]=="Diesel","tCO2e"].sum(),
            vehicle_raw.iloc[1]["tCO2e"],
            vehicle_raw.iloc[2]["tCO2e"],
            bus_raw["tCO2e"].sum(),
            total_s1hvac,
        ],
        "Category": ["Vehicle fuel","Vehicle fuel","Vehicle fuel","Distance-based","HVAC"],
    })
    src_bar = alt.Chart(src_df).mark_bar(
        cornerRadiusTopRight=4, cornerRadiusBottomRight=4
    ).encode(
        x=alt.X("tCO2e:Q", title="tCO₂e"),
        y=alt.Y("Source:N", sort="-x", title=None),
        color=alt.Color("Category:N",
            scale=alt.Scale(domain=["Vehicle fuel","Distance-based","HVAC"],
                            range=[C_S1, C_S2, C_TOT]),
            legend=alt.Legend(orient="right")),
        tooltip=[alt.Tooltip("Source:N"),
                 alt.Tooltip("tCO2e:Q", format=".5f", title="tCO₂e")],
    ).properties(height=150)
    src_txt = src_bar.mark_text(align="left", dx=5, fontSize=10,
                                 color=TEXT_MAIN, font="DM Mono, monospace").encode(
        text=alt.Text("tCO2e:Q", format=".4f"))
    st.altair_chart(src_bar+src_txt, use_container_width=True)

    ia, ib, ic, id_ = st.columns(4)
    with ia:
        st.markdown(f"""<div class="insight-card blue">
            <strong>🚗 Diesel dominates Scope 1</strong>
            {vehicle_raw.iloc[0]['tCO2e']:.3f} tCO₂e from 1,742 L diesel in February —
            the single largest mobile combustion event.
        </div>""", unsafe_allow_html=True)
    with ib:
        st.markdown(f"""<div class="insight-card">
            <strong>🌡️ HVAC heating — Scope 1</strong>
            {total_s1hvac:.3f} tCO₂e from natural gas combustion across
            8 heating months (Jan–Apr, Nov–Dec).
        </div>""", unsafe_allow_html=True)
    with ic:
        st.markdown(f"""<div class="insight-card">
            <strong>⚡ July electricity surge</strong>
            +{(elec_kwh[6]/elec_kwh.mean()-1)*100:.0f}% above annual avg.
            Summer cooling drives 48,569 kWh → {elec_df.iloc[6]['tCO2e']:.2f} tCO₂e.
        </div>""", unsafe_allow_html=True)
    with id_:
        st.markdown(f"""<div class="insight-card orange">
            <strong>📊 Scope 2 is the lever</strong>
            Electricity = <b>{total_s2/total_all*100:.1f}%</b> of total GHG.
            Renewable procurement offers the highest impact.
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TREND & CURVES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    # ── Chart A: Full multi-line with all overlays ──────────────────────────
    st.markdown('<div class="sec-label">All emission series — monthly tCO₂e</div>', unsafe_allow_html=True)

    chart_A = (
        smooth_line(trend_df, "Scope1", C_S1,  2.0, label="Scope 1") +
        glow_point(trend_df,  "Scope1", C_S1,  40) +
        smooth_line(trend_df, "Scope2", C_S2,  2.0, label="Scope 2") +
        glow_point(trend_df,  "Scope2", C_S2,  40) +
        smooth_line(trend_df, "Total",  C_TOT, 2.5, label="Total") +
        glow_point(trend_df,  "Total",  C_TOT, 55)
    )
    if show_rolling:
        chart_A = chart_A + smooth_line(trend_df, "Roll_S1",    C_S1,  1.2, [4,3], 0.6, "Roll. avg S1")
        chart_A = chart_A + smooth_line(trend_df, "Roll_S2",    C_S2,  1.2, [4,3], 0.6, "Roll. avg S2")
        chart_A = chart_A + smooth_line(trend_df, "Roll_Total", C_ROLL,1.8, [3,2], 0.8, "Roll. avg Total")
    if show_band:
        band = alt.Chart(trend_df).mark_area(
            color=C_ROLL, opacity=0.06, interpolate=interp
        ).encode(
            x=mx(),
            y=alt.Y("Band_Lower:Q", title="tCO₂e"),
            y2="Band_Upper:Q",
        )
        chart_A = band + chart_A
    if show_target:
        chart_A = chart_A + rule_line(target_monthly[0], C_TARGET)
        lbl_tgt = alt.Chart(pd.DataFrame({
            "Month":["Dec"],"y":[target_monthly[-1]],"t":["← target −10%"]}
        )).mark_text(align="right", dx=-4, dy=-9, fontSize=9,
                     color=C_TARGET, font="DM Mono, monospace").encode(
            x=alt.X("Month:N", sort=MONTHS), y="y:Q", text="t:N")
        chart_A = chart_A + lbl_tgt
    if show_proj:
        chart_A = chart_A + smooth_line(trend_df, "Proj_Total", C_PROJ, 1.5, [5,3], 0.7, "Trend projection")

    st.altair_chart(chart_A.properties(**h_props(360)), use_container_width=True)

    # ── Chart B: Stacked area ────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Stacked area — scope contribution over time</div>', unsafe_allow_html=True)
    area_long = trend_df[["Month","Scope1","Scope2"]].melt(
        id_vars="Month", value_vars=["Scope1","Scope2"],
        var_name="Scope", value_name="tCO2e")
    area_long["Scope"] = area_long["Scope"].map({"Scope1":"Scope 1","Scope2":"Scope 2"})
    area_stacked = alt.Chart(area_long).mark_area(
        opacity=0.8, interpolate=interp
    ).encode(
        x=mx(),
        y=alt.Y("tCO2e:Q", stack="zero", title="tCO₂e"),
        color=alt.Color("Scope:N",
            scale=alt.Scale(domain=["Scope 1","Scope 2"], range=[C_S1, C_S2]),
            legend=alt.Legend(orient="top", title=None)),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Scope:N"),
                 alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e")],
    )
    total_overlay = smooth_line(trend_df, "Total", C_TOT, 2, label="Total") + \
                    glow_point(trend_df, "Total", C_TOT, 40)
    st.altair_chart((area_stacked + total_overlay).properties(**h_props(260)),
                    use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        # ── Chart C: MoM % change ─────────────────────────────────────────
        st.markdown('<div class="sec-label">Month-over-month Δ total emissions (%)</div>', unsafe_allow_html=True)
        mom_df = trend_df.dropna(subset=["MoM_Change"]).copy()
        mom_df["Dir"] = np.where(mom_df["MoM_Change"] >= 0, "▲ Increase", "▼ Decrease")
        mom_bar = alt.Chart(mom_df).mark_bar(
            cornerRadiusTopLeft=3, cornerRadiusTopRight=3,
            cornerRadiusBottomLeft=3, cornerRadiusBottomRight=3,
            width={"band": 0.65}
        ).encode(
            x=mx(),
            y=alt.Y("MoM_Change:Q", title="% vs prior month",
                    axis=alt.Axis(format=".1f")),
            color=alt.Color("Dir:N",
                scale=alt.Scale(domain=["▲ Increase","▼ Decrease"],
                                range=[C_TARGET, C_S2]),
                legend=alt.Legend(orient="top", title=None)),
            tooltip=[alt.Tooltip("Month:N"),
                     alt.Tooltip("MoM_Change:Q", format=".1f", title="MoM %")],
        )
        # smooth zero line
        zero = alt.Chart(pd.DataFrame({"y":[0]})).mark_rule(
            color=GRID_COL, strokeWidth=1.2).encode(y="y:Q")
        mom_line = smooth_line(mom_df, "MoM_Change", C_ROLL, 1.5,
                               dash=[3,2], opacity=0.6, label="Trend")
        st.altair_chart((mom_bar + zero + mom_line).properties(**h_props(250)),
                        use_container_width=True)

    with col_d:
        # ── Chart D: Scope 2 scatter + regression ─────────────────────────
        st.markdown('<div class="sec-label">kWh consumption vs Scope 2 emissions</div>', unsafe_allow_html=True)
        scatter = alt.Chart(trend_df).mark_circle(size=90, opacity=0.85).encode(
            x=alt.X("kWh:Q", title="Monthly kWh",
                    axis=alt.Axis(format=",.0f")),
            y=alt.Y("Scope2:Q", title="tCO₂e (S2)"),
            color=alt.Color("Month:N",
                scale=alt.Scale(scheme="plasma"),
                legend=alt.Legend(orient="right", title="Month",
                                  labelFontSize=9, symbolSize=60)),
            tooltip=[alt.Tooltip("Month:N"),
                     alt.Tooltip("kWh:Q", format=",.0f", title="kWh"),
                     alt.Tooltip("Scope2:Q", format=".3f", title="tCO₂e")],
        )
        reg = scatter.transform_regression("kWh","Scope2").mark_line(
            color=C_PROJ, strokeDash=[5,3], strokeWidth=1.8)
        st.altair_chart((scatter + reg).properties(**h_props(250)),
                        use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CUMULATIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    # ── Chart A: Cumulative lines ────────────────────────────────────────────
    st.markdown('<div class="sec-label">Year-to-date cumulative tCO₂e build-up</div>', unsafe_allow_html=True)

    cum_chart = (
        area_chart(trend_df, "Cum_Total", C_CUM, 0.10) +
        smooth_line(trend_df, "Cum_Total",  C_CUM, 2.5, label="Total cumul.") +
        glow_point(trend_df,  "Cum_Total",  C_CUM, 55) +
        smooth_line(trend_df, "Cum_S2",     C_S2,  2.0, label="S2 cumul.") +
        glow_point(trend_df,  "Cum_S2",     C_S2,  40) +
        smooth_line(trend_df, "Cum_S1",     C_S1,  1.8, [4,3], 0.9, "S1 cumul.") +
        glow_point(trend_df,  "Cum_S1",     C_S1,  40)
    )
    # End-of-year annotations
    ey = trend_df[trend_df["Month"]=="Dec"].copy()
    for col, color, label in [("Cum_Total",C_CUM,"Total"),("Cum_S2",C_S2,"S2"),("Cum_S1",C_S1,"S1")]:
        ann = alt.Chart(ey).mark_text(
            align="right", dx=-6, dy=-11, fontSize=10,
            color=color, font="DM Mono, monospace"
        ).encode(x=mx(), y=alt.Y(f"{col}:Q"),
                 text=alt.Text(f"{col}:Q", format=".2f"))
        cum_chart = cum_chart + ann

    st.altair_chart(cum_chart.properties(**h_props(340)), use_container_width=True)

    col_l, col_r = st.columns(2)

    with col_l:
        # ── Chart B: % of annual total reached ───────────────────────────
        st.markdown('<div class="sec-label">Year-to-date progress — % of annual total</div>', unsafe_allow_html=True)
        pct_area = alt.Chart(trend_df).mark_area(
            color=C_CUM, opacity=0.12, interpolate=interp,
            line={"color": C_CUM, "strokeWidth": 2}
        ).encode(
            x=mx(),
            y=alt.Y("Pct_Annual:Q", title="% of annual total",
                    scale=alt.Scale(domain=[0,105])),
            tooltip=[alt.Tooltip("Month:N"),
                     alt.Tooltip("Pct_Annual:Q", format=".1f", title="% annual")],
        )
        pct_pts = glow_point(trend_df, "Pct_Annual", C_CUM, 50)
        half_rule = rule_line(50, TEXT_COL, [4,3])
        full_rule  = rule_line(100, C_TARGET, [2,2])
        st.altair_chart((pct_area + pct_pts + half_rule + full_rule).properties(**h_props(260)),
                        use_container_width=True)
        st.caption("Dashed grey = 50% mark · Dashed red = 100% (year-end)")

    with col_r:
        # ── Chart C: Cumulative area unstacked ───────────────────────────
        st.markdown('<div class="sec-label">Cumulative area — S1 vs S2 overlap</div>', unsafe_allow_html=True)
        cum_ovlp = (
            area_chart(trend_df, "Cum_S2", C_S2, 0.25) +
            area_chart(trend_df, "Cum_S1", C_S1, 0.35) +
            smooth_line(trend_df, "Cum_S2", C_S2, 2.0, label="S2 cumul.") +
            smooth_line(trend_df, "Cum_S1", C_S1, 2.0, label="S1 cumul.")
        )
        st.altair_chart(cum_ovlp.properties(**h_props(260)), use_container_width=True)

    # ── Table ────────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Cumulative data table</div>', unsafe_allow_html=True)
    cum_tbl = trend_df[["Month","Scope1","Scope2","Total",
                         "Cum_S1","Cum_S2","Cum_Total","Pct_Annual"]].copy()
    cum_tbl.columns = ["Month","S1 (t)","S2 (t)","Total (t)",
                        "Cum S1","Cum S2","Cum Total","% Annual"]
    for c in ["S1 (t)","S2 (t)","Total (t)","Cum S1","Cum S2","Cum Total"]:
        cum_tbl[c] = cum_tbl[c].map("{:.4f}".format)
    cum_tbl["% Annual"] = cum_tbl["% Annual"].map("{:.1f}%".format)
    st.dataframe(cum_tbl, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — SEASONALITY
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-label">Seasonal index — ratio to monthly mean (1.0 = average)</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        sea_area = alt.Chart(trend_df).mark_area(
            color=C_TOT, opacity=0.13, interpolate=interp,
            line={"color": C_TOT, "strokeWidth": 2.5}
        ).encode(
            x=mx(),
            y=alt.Y("Seasonal:Q", title="Seasonal index",
                    scale=alt.Scale(domain=[0, trend_df["Seasonal"].max()*1.2])),
            tooltip=[alt.Tooltip("Month:N"),
                     alt.Tooltip("Seasonal:Q", format=".3f", title="Index")],
        )
        sea_pts = glow_point(trend_df, "Seasonal", C_TOT, 55)
        avg_rule = rule_line(1.0, TEXT_COL, [4,3])
        st.altair_chart((sea_area + sea_pts + avg_rule).properties(**h_props(270)),
                        use_container_width=True)
        st.caption("Values > 1.0 indicate above-average emission months")

    with col_b:
        # Efficiency score chart
        st.markdown('<div class="sec-label">Carbon efficiency score (higher = better)</div>', unsafe_allow_html=True)
        eff_area = alt.Chart(trend_df).mark_area(
            color=C_S2, opacity=0.15, interpolate=interp,
            line={"color": C_S2, "strokeWidth": 2.5}
        ).encode(
            x=mx(),
            y=alt.Y("Efficiency:Q", title="Efficiency (0–1)",
                    scale=alt.Scale(domain=[0,1.1])),
            tooltip=[alt.Tooltip("Month:N"),
                     alt.Tooltip("Efficiency:Q", format=".3f", title="Efficiency")],
        )
        eff_pts = glow_point(trend_df, "Efficiency", C_S2, 55)
        eff_roll = rolling_n(efficiency)
        trend_df["Roll_Eff"] = eff_roll
        eff_roll_line = smooth_line(trend_df, "Roll_Eff", C_ROLL, 1.8,
                                    [4,2], 0.7, "Rolling avg")
        st.altair_chart((eff_area + eff_pts + eff_roll_line).properties(**h_props(270)),
                        use_container_width=True)
        st.caption("Based on inverse normalised Scope 2 intensity")

    # ── Heatmap-style: monthly contribution % by scope ───────────────────────
    st.markdown('<div class="sec-label">Monthly share of annual totals — Scope 1 vs Scope 2</div>', unsafe_allow_html=True)
    share_data = []
    for i, m in enumerate(MONTHS):
        share_data.append({"Month": m, "Scope": "Scope 1",
                           "Share": s1_monthly[i]/total_s1*100 if total_s1>0 else 0})
        share_data.append({"Month": m, "Scope": "Scope 2",
                           "Share": s2_monthly[i]/total_s2*100})
    share_df = pd.DataFrame(share_data)
    share_df["Month"] = pd.Categorical(share_df["Month"], categories=MONTHS, ordered=True)

    share_bar = alt.Chart(share_df).mark_bar(
        cornerRadiusTopLeft=3, cornerRadiusTopRight=3, width={"band": 0.6}
    ).encode(
        x=mx(),
        y=alt.Y("Share:Q", title="% of annual scope total"),
        color=alt.Color("Scope:N",
            scale=alt.Scale(domain=["Scope 1","Scope 2"], range=[C_S1, C_S2]),
            legend=alt.Legend(orient="top", title=None)),
        xOffset=alt.XOffset("Scope:N"),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Scope:N"),
                 alt.Tooltip("Share:Q", format=".1f", title="%")],
    ).properties(**h_props(260))
    st.altair_chart(share_bar, use_container_width=True)

    # ── Radial / polar energy-like chart — monthly kWh as bar-in-circle ──────
    st.markdown('<div class="sec-label">Monthly total tCO₂e — radial bars</div>', unsafe_allow_html=True)
    trend_df["theta_start"] = (trend_df["Month_num"]-1) / 12 * 2 * np.pi
    trend_df["theta_end"]   = trend_df["Month_num"] / 12 * 2 * np.pi
    radial = alt.Chart(trend_df).mark_arc(innerRadius=40).encode(
        theta=alt.Theta("Month_num:O", stack=True),
        radius=alt.Radius("Total:Q", scale=alt.Scale(type="sqrt", zero=True,
                                                       rangeMin=40)),
        color=alt.Color("Total:Q",
            scale=alt.Scale(scheme="plasma"),
            legend=alt.Legend(title="tCO₂e", orient="right")),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("Total:Q", format=".4f", title="Total tCO₂e")],
    ).properties(height=300)
    st.altair_chart(radial, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SCOPE 1 DETAIL
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<span class="badge-s1">Scope 1</span>&nbsp; Mobile Combustion + HVAC Heating', unsafe_allow_html=True)
    st.markdown(" ")

    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Total Scope 1",     f"{total_s1:.3f}",      "tCO₂e")
    m2.metric("Fuel vouchers",     f"{total_s1v:.4f}",     "tCO₂e · 3 tx")
    m3.metric("Bus / Van trips",   f"{total_s1b:.5f}",     "tCO₂e · 5 trips")
    m4.metric("HVAC Heating",      f"{total_s1hvac:.3f}",  "tCO₂e · 8 months")
    m5.metric("HVAC cooling",      f"{total_hvac_cooling:.3f}", "tCO₂e · S2 (info)")

    # ── Chart A: Monthly stacked S1 — fuel + bus + HVAC ──────────────────────
    st.markdown('<div class="sec-label">Monthly Scope 1 — stacked by source type (vehicles + HVAC heating)</div>', unsafe_allow_html=True)

    fuel_mo = np.zeros(12)
    bus_mo  = np.zeros(12)
    for _, row in vehicle_raw.iterrows():
        fuel_mo[int(row["Month_num"])-1] += row["tCO2e"]
    for _, row in bus_raw.iterrows():
        bus_mo[int(row["Month_num"])-1] += row["tCO2e"]

    s1_long = pd.DataFrame({
        "Month": MONTHS * 3,
        "Type":  ["Fuel vouchers"]*12 + ["Bus/Van"]*12 + ["HVAC Heating"]*12,
        "tCO2e": list(fuel_mo) + list(bus_mo) + list(hvac_s1_monthly),
    })
    s1_long["Month"] = pd.Categorical(s1_long["Month"], categories=MONTHS, ordered=True)

    s1_bars = alt.Chart(s1_long).mark_bar(
        cornerRadiusTopLeft=3, cornerRadiusTopRight=3
    ).encode(
        x=mx(),
        y=alt.Y("tCO2e:Q", stack="zero", title="tCO₂e"),
        color=alt.Color("Type:N",
            scale=alt.Scale(domain=["Fuel vouchers","Bus/Van","HVAC Heating"],
                            range=[C_S1, C_S2, C_TOT]),
            legend=alt.Legend(orient="top", title=None)),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Type:N"),
                 alt.Tooltip("tCO2e:Q", format=".5f", title="tCO₂e")],
    )
    s1_line_ov = smooth_line(trend_df, "Scope1", C_ROLL, 1.8, [4,2], label="Total S1")
    s1_pts_ov  = glow_point(trend_df, "Scope1", C_ROLL, 40)
    st.altair_chart((s1_bars + s1_line_ov + s1_pts_ov).properties(**h_props(300)),
                    use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # ── Chart B: HVAC heating & cooling loads ────────────────────────────
        st.markdown('<div class="sec-label">HVAC monthly load — heating vs cooling (kWh)</div>', unsafe_allow_html=True)
        hvac_long = pd.DataFrame({
            "Month":  MONTHS * 2,
            "Type":   ["Heating (Scope 1)"]*12 + ["Cooling (Scope 2)"]*12,
            "kWh":    list(hvac_heating_kwh) + list(hvac_cooling_kwh),
        })
        hvac_long["Month"] = pd.Categorical(hvac_long["Month"], categories=MONTHS, ordered=True)

        hvac_bars = alt.Chart(hvac_long).mark_bar(
            cornerRadiusTopLeft=3, cornerRadiusTopRight=3, width={"band": 0.65}
        ).encode(
            x=mx(),
            y=alt.Y("kWh:Q", title="kWh", stack=None),
            color=alt.Color("Type:N",
                scale=alt.Scale(domain=["Heating (Scope 1)","Cooling (Scope 2)"],
                                range=[C_TOT, C_S2]),
                legend=alt.Legend(orient="top", title=None)),
            xOffset=alt.XOffset("Type:N"),
            opacity=alt.condition(
                alt.datum.kWh > 0, alt.value(0.9), alt.value(0.0)
            ),
            tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Type:N"),
                     alt.Tooltip("kWh:Q", format=",.1f", title="kWh")],
        )

        # Heating emissions line (right axis)
        hvac_line = alt.Chart(hvac_df[hvac_df["Heating_kWh"]>0]).mark_line(
            color=C_TOT, strokeWidth=2.2, interpolate=interp, strokeDash=[4,2]
        ).encode(
            x=mx(),
            y=alt.Y("Heating_tCO2e:Q", title="tCO₂e",
                    axis=alt.Axis(titleColor=C_TOT)),
            tooltip=[alt.Tooltip("Month:N"),
                     alt.Tooltip("Heating_tCO2e:Q", format=".4f", title="Heating tCO₂e")],
        )
        hvac_pts = alt.Chart(hvac_df[hvac_df["Heating_kWh"]>0]).mark_point(
            color=C_TOT, filled=True, size=55
        ).encode(
            x=mx(), y=alt.Y("Heating_tCO2e:Q"),
        )
        hvac_chart = alt.layer(hvac_bars, hvac_line + hvac_pts).resolve_scale(y="independent")
        st.altair_chart(hvac_chart.properties(**h_props(290)), use_container_width=True)
        st.caption("Bars = kWh load  ·  Dashed line = Scope 1 tCO₂e (heating only, natural gas combustion)")

    with col_b:
        # ── Chart C: HVAC tCO2e area — heating Scope 1 ──────────────────────
        st.markdown('<div class="sec-label">HVAC heating — monthly tCO₂e (Scope 1)</div>', unsafe_allow_html=True)
        hvac_area_df = hvac_df.copy()

        hvac_area = alt.Chart(hvac_area_df).mark_area(
            color=C_TOT, opacity=0.15, interpolate=interp,
            line={"color": C_TOT, "strokeWidth": 2.5}
        ).encode(
            x=mx(),
            y=alt.Y("Heating_tCO2e:Q", title="tCO₂e"),
            tooltip=[alt.Tooltip("Month:N"),
                     alt.Tooltip("Heating_tCO2e:Q", format=".4f", title="Heating tCO₂e"),
                     alt.Tooltip("Heating_kWh:Q",   format=",.1f",  title="Heating kWh")],
        )
        hvac_pts2 = glow_point(hvac_area_df, "Heating_tCO2e", C_TOT, 55)

        # Rolling avg of heating
        hvac_area_df["Roll_Heat"] = rolling_n(hvac_area_df["Heating_tCO2e"].values)
        hvac_roll = smooth_line(hvac_area_df, "Roll_Heat", C_ROLL, 1.8,
                                [4,2], 0.75, "Rolling avg")
        hvac_avg_rule = rule_line(hvac_area_df["Heating_tCO2e"].mean(), C_PROJ)

        st.altair_chart((hvac_area + hvac_pts2 + hvac_roll + hvac_avg_rule).properties(**h_props(290)),
                        use_container_width=True)
        st.caption(f"Gold dashed = annual mean  ·  Pink = 3-mo rolling avg  ·  EF: {ef_hvac:.3f} kgCO₂e/kWh")

    # ── Chart D: Cumulative HVAC vs vehicle S1 ───────────────────────────────
    st.markdown('<div class="sec-label">Cumulative Scope 1 build-up — HVAC vs mobile combustion</div>', unsafe_allow_html=True)

    cum_fuel_bus = np.cumsum(fuel_mo + bus_mo)
    cum_hvac_s1  = np.cumsum(hvac_s1_monthly)
    cum_s1_total = np.cumsum(fuel_mo + bus_mo + hvac_s1_monthly)

    cum_s1_df = pd.DataFrame({
        "Month":       MONTHS * 3,
        "Series":      ["Mobile combustion"]*12 + ["HVAC Heating"]*12 + ["Total S1"]*12,
        "Cumul_tCO2e": list(cum_fuel_bus) + list(cum_hvac_s1) + list(cum_s1_total),
    })
    cum_s1_df["Month"] = pd.Categorical(cum_s1_df["Month"], categories=MONTHS, ordered=True)

    cum_s1_color = alt.Scale(
        domain=["Mobile combustion","HVAC Heating","Total S1"],
        range=[C_S1, C_TOT, C_ROLL]
    )
    cum_s1_lines = alt.Chart(cum_s1_df).mark_line(strokeWidth=2.2, interpolate=interp).encode(
        x=mx(),
        y=alt.Y("Cumul_tCO2e:Q", title="Cumulative tCO₂e"),
        color=alt.Color("Series:N", scale=cum_s1_color,
                        legend=alt.Legend(orient="top", title=None)),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Series:N"),
                 alt.Tooltip("Cumul_tCO2e:Q", format=".4f", title="Cumulative tCO₂e")],
    )
    cum_s1_pts = alt.Chart(cum_s1_df).mark_point(filled=True, size=50).encode(
        x=mx(),
        y=alt.Y("Cumul_tCO2e:Q"),
        color=alt.Color("Series:N", scale=cum_s1_color),
    )
    st.altair_chart((cum_s1_lines + cum_s1_pts).properties(**h_props(270)),
                    use_container_width=True)

    # ── Vehicle fuel bar ─────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Vehicle fuel — liters & emissions</div>', unsafe_allow_html=True)
    fuel_df = pd.DataFrame({
        "Vehicle":["Diesel fleet","Peugeot Bipper (Feb)","Peugeot Bipper (Dec)"],
        "Liters": [1741.5, 1520.8, 1520.8],
        "tCO2e":  list(vehicle_raw["tCO2e"]),
        "Fuel":   ["Diesel","Super Gasoline","Super Gasoline"],
    })
    fb = alt.Chart(fuel_df).mark_bar(
        cornerRadiusTopLeft=3, cornerRadiusTopRight=3
    ).encode(
        x=alt.X("Vehicle:N", title=None,
                axis=alt.Axis(labelAngle=-15, labelLimit=180)),
        y=alt.Y("tCO2e:Q", title="tCO₂e"),
        color=alt.Color("Fuel:N",
            scale=alt.Scale(domain=["Diesel","Super Gasoline"],
                            range=[C_S1,"#54A0FF"]),
            legend=alt.Legend(orient="top")),
        tooltip=[alt.Tooltip("Vehicle:N"), alt.Tooltip("Liters:Q", format=",.1f"),
                 alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e")],
    )
    fb_txt = fb.mark_text(dy=-8, fontSize=10, color=TEXT_MAIN,
                           font="DM Mono, monospace").encode(
        text=alt.Text("tCO2e:Q", format=".3f"))
    st.altair_chart((fb+fb_txt).properties(**h_props(230)), use_container_width=True)

    # ── Bus distances ─────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Bus & van trip distances</div>', unsafe_allow_html=True)
    bus_bar = alt.Chart(bus_raw).mark_bar(
        color=C_S2, cornerRadiusTopRight=4, cornerRadiusBottomRight=4
    ).encode(
        x=alt.X("Distance_km:Q", title="Distance (km)"),
        y=alt.Y("Destination:N", sort="-x", title=None),
        tooltip=[alt.Tooltip("Destination:N"), alt.Tooltip("Distance_km:Q", title="km"),
                 alt.Tooltip("tCO2e:Q", format=".6f", title="tCO₂e"),
                 alt.Tooltip("Source:N")],
    )
    bus_txt = bus_bar.mark_text(align="left", dx=5, fontSize=10,
                                 color=TEXT_MAIN, font="DM Mono, monospace").encode(
        text=alt.Text("Distance_km:Q", format=".1f"))
    st.altair_chart((bus_bar+bus_txt).properties(**h_props(180)), use_container_width=True)

    # ── Data tables ──────────────────────────────────────────────────────────
    ct1, ct2, ct3 = st.columns(3)
    with ct1:
        st.markdown("**Fuel voucher transactions**")
        dv = vehicle_raw[["Date","Source","Fuel_type","Liters","tCO2e"]].copy()
        dv.columns = ["Date","Source","Fuel","Liters","tCO₂e"]
        dv["Liters"] = dv["Liters"].map("{:,.1f}".format)
        dv["tCO₂e"]  = dv["tCO₂e"].map("{:.5f}".format)
        st.dataframe(dv, use_container_width=True, hide_index=True)
    with ct2:
        st.markdown("**Bus / van trips**")
        db = bus_raw[["Date","Destination","Source","Distance_km","tCO2e"]].copy()
        db.columns = ["Date","Destination","Vehicle","km","tCO₂e"]
        db["tCO₂e"] = db["tCO₂e"].map("{:.6f}".format)
        st.dataframe(db, use_container_width=True, hide_index=True)
    with ct3:
        st.markdown("**HVAC monthly data**")
        dh = hvac_df[["Month","Heating_kWh","Heating_tCO2e","Cooling_kWh","Cooling_tCO2e"]].copy()
        dh.columns = ["Month","Heating kWh","Heating tCO₂e","Cooling kWh","Cooling tCO₂e (S2)"]
        dh["Heating kWh"]       = dh["Heating kWh"].map(lambda x: f"{x:,.1f}" if x>0 else "—")
        dh["Heating tCO₂e"]     = dh["Heating tCO₂e"].map(lambda x: f"{x:.4f}" if x>0 else "—")
        dh["Cooling kWh"]       = dh["Cooling kWh"].map(lambda x: f"{x:,.1f}" if x>0 else "—")
        dh["Cooling tCO₂e (S2)"]= dh["Cooling tCO₂e (S2)"].map(lambda x: f"{x:.4f}" if x>0 else "—")
        st.dataframe(dh, use_container_width=True, hide_index=True)
    st.caption(f"HVAC heating EF: {ef_hvac:.3f} kgCO₂e/kWh (natural gas) · Cooling is Scope 2 (electricity) · Avg {HVAC_HOURS_PER_MONTH:,} working hours/month")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — SCOPE 2 DETAIL
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<span class="badge-s2">Scope 2</span>&nbsp; Purchased Electricity — location-based', unsafe_allow_html=True)
    st.markdown(" ")

    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Total Scope 2",     f"{total_s2:.3f}", "tCO₂e")
    m2.metric("Total consumption", f"{total_kwh/1000:.1f}", "MWh")
    m3.metric("Monthly average",   f"{int(total_kwh/12):,}", "kWh")
    m4.metric("Peak month",        "July · 48,569",          "kWh")
    m5.metric("Grid factor",       f"{ef_grid:.3f}",          "kgCO₂e / kWh")

    # ── Chart A: Dual-axis bar + CO2e line ───────────────────────────────────
    st.markdown('<div class="sec-label">Monthly electricity (kWh) vs emissions (tCO₂e)</div>', unsafe_allow_html=True)
    elec_plot = elec_df.copy()
    elec_plot["Month"] = pd.Categorical(elec_plot["Month"], categories=MONTHS, ordered=True)

    bar_kwh = alt.Chart(elec_plot).mark_bar(
        color=C_S2, opacity=0.35,
        cornerRadiusTopLeft=4, cornerRadiusTopRight=4, width={"band": 0.7}
    ).encode(
        x=mx(),
        y=alt.Y("kWh:Q", title="kWh", axis=alt.Axis(titleColor=C_S2)),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("kWh:Q",   format=",.0f", title="kWh"),
                 alt.Tooltip("tCO2e:Q", format=".3f",  title="tCO₂e")],
    )
    line_co2 = alt.Chart(elec_plot).mark_line(
        color=C_S2, strokeWidth=2.8, interpolate=interp
    ).encode(
        x=mx(),
        y=alt.Y("tCO2e:Q", title="tCO₂e", axis=alt.Axis(titleColor=C_S2)),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("tCO2e:Q", format=".3f", title="tCO₂e")],
    )
    pts_co2 = alt.Chart(elec_plot).mark_point(
        color=C_S2, filled=True, size=65
    ).encode(
        x=mx(), y=alt.Y("tCO2e:Q"),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("tCO2e:Q", format=".3f", title="tCO₂e")],
    )
    avg_rule = rule_line(elec_kwh.mean(), C_TARGET)
    dual = alt.layer(bar_kwh, avg_rule, line_co2+pts_co2).resolve_scale(y="independent")
    st.altair_chart(dual.properties(**h_props(300)), use_container_width=True)
    st.caption(f"Dashed line = annual avg {elec_kwh.mean():,.0f} kWh")

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        # ── Chart B: Scope 2 area + rolling + projection ──────────────────
        st.markdown('<div class="sec-label">Scope 2 emissions — area + trend overlays</div>', unsafe_allow_html=True)
        s2_chart = area_chart(trend_df, "Scope2", C_S2, 0.14)
        s2_chart = s2_chart + smooth_line(trend_df, "Scope2", C_S2, 2.5, label="S2 monthly")
        s2_chart = s2_chart + glow_point(trend_df, "Scope2", C_S2, 55)
        if show_rolling:
            s2_chart = s2_chart + smooth_line(trend_df, "Roll_S2", C_ROLL, 1.8,
                                               [4,2], 0.75, "Rolling avg")
        if show_proj:
            s2_chart = s2_chart + smooth_line(trend_df, "Proj_S2", C_PROJ, 1.5,
                                               [5,3], 0.7, "Linear projection")
        if show_target:
            s2_chart = s2_chart + rule_line(target_monthly[0]*total_s2/total_all, C_TARGET)
        st.altair_chart(s2_chart.properties(**h_props(270)), use_container_width=True)

    with col_r2:
        # ── Chart C: Carbon intensity ─────────────────────────────────────
        st.markdown('<div class="sec-label">Carbon intensity — kgCO₂e per kWh</div>', unsafe_allow_html=True)
        int_chart = (
            area_chart(trend_df, "Intensity", C_INT, 0.12, "kgCO₂e / kWh") +
            smooth_line(trend_df, "Intensity", C_INT, 2.2, label="Intensity") +
            glow_point(trend_df,  "Intensity", C_INT, 55) +
            rule_line(intensity.mean(), C_PROJ)
        )
        st.altair_chart(int_chart.properties(**h_props(270)), use_container_width=True)
        st.caption("Flat line = constant grid factor; changes when EF is adjusted in sidebar")

    # ── Chart D: kWh deviation from mean ────────────────────────────────────
    st.markdown('<div class="sec-label">kWh deviation from annual average</div>', unsafe_allow_html=True)
    trend_df["kWh_Dev"] = trend_df["kWh"] - elec_kwh.mean()
    trend_df["Dev_Dir"] = np.where(trend_df["kWh_Dev"] >= 0, "Above avg", "Below avg")

    dev_bar = alt.Chart(trend_df).mark_bar(
        cornerRadiusTopLeft=3, cornerRadiusTopRight=3,
        cornerRadiusBottomLeft=3, cornerRadiusBottomRight=3,
        width={"band": 0.65}
    ).encode(
        x=mx(),
        y=alt.Y("kWh_Dev:Q", title="kWh deviation", axis=alt.Axis(format=",.0f")),
        color=alt.Color("Dev_Dir:N",
            scale=alt.Scale(domain=["Above avg","Below avg"],
                            range=[C_TARGET, C_S2]),
            legend=alt.Legend(orient="top", title=None)),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("kWh:Q",    format=",.0f", title="kWh"),
                 alt.Tooltip("kWh_Dev:Q",format=",.0f", title="Δ from avg")],
    )
    dev_line = smooth_line(trend_df, "kWh_Dev", C_ROLL, 1.5, [3,2], 0.6, "Trend")
    zero_r   = rule_line(0, GRID_COL, [3,2])
    st.altair_chart((dev_bar + zero_r + dev_line).properties(**h_props(240)),
                    use_container_width=True)

    # ── Table ────────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Monthly breakdown</div>', unsafe_allow_html=True)
    de = elec_df[["Month","kWh","MWh","tCO2e","Meters"]].copy()
    de.columns = ["Month","kWh","MWh","tCO₂e","Meters"]
    de["kWh"]   = de["kWh"].map("{:,.0f}".format)
    de["MWh"]   = de["MWh"].map("{:.3f}".format)
    de["tCO₂e"] = de["tCO₂e"].map("{:.4f}".format)
    st.dataframe(de, use_container_width=True, hide_index=True)
    st.caption(f"Grid EF: {ef_grid:.4f} kgCO₂e/kWh (Tunisia STEG) · All charts update live with sidebar sliders")
