import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="GHG Carbon Monitor · 2025",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #060A10; color: #DCE6EE; }
  .block-container { padding: 1.8rem 2.4rem 2.4rem; max-width: 100%; }

  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1018 0%, #080D14 100%);
    border-right: 1px solid rgba(255,255,255,.04);
  }
  [data-testid="stSidebar"] * { color: #A8BDD0 !important; }
  [data-testid="stSidebar"] .stNumberInput input {
    background: #0F1922 !important; border: 1px solid #1A2D40 !important;
    color: #DCE6EE !important; border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important; font-size: 12px !important;
  }
  [data-testid="stSidebar"] h3 {
    font-family: 'Syne', sans-serif !important; font-size: 12px !important;
    color: #DCE6EE !important; letter-spacing:.06em; text-transform: uppercase;
  }

  [data-testid="stMetric"] {
    background: linear-gradient(140deg, #0D1825 0%, #091420 100%);
    border: 1px solid #162030; border-radius: 14px;
    padding: 16px 20px 14px; position: relative; overflow: hidden;
    transition: border-color .2s, transform .15s;
  }
  [data-testid="stMetric"]:hover { border-color: #223348; transform: translateY(-1px); }
  [data-testid="stMetric"]::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg,#00C9A7 0%,#0096FF 50%,#B57BFF 100%);
  }
  [data-testid="stMetricLabel"] {
    font-family:'DM Mono',monospace !important; font-size:9px !important;
    letter-spacing:.15em !important; text-transform:uppercase !important; color:#3D5F7A !important;
  }
  [data-testid="stMetricValue"] {
    font-family:'Syne',sans-serif !important; font-size:1.55rem !important;
    font-weight:700 !important; color:#E8F0F7 !important; line-height:1.15 !important;
  }
  [data-testid="stMetricDelta"] {
    font-family:'DM Mono',monospace !important; font-size:9.5px !important; color:#00C9A7 !important;
  }

  [data-testid="stTabs"] [data-baseweb="tab-list"] {
    background:transparent !important; border-bottom:1px solid #162030 !important; gap:2px;
  }
  [data-testid="stTabs"] [data-baseweb="tab"] {
    font-family:'DM Mono',monospace !important; font-size:10px !important;
    letter-spacing:.1em !important; text-transform:uppercase !important;
    color:#2D4D66 !important; background:transparent !important;
    border:none !important; padding:10px 20px !important;
    border-radius:8px 8px 0 0 !important; transition:all .18s;
  }
  [data-testid="stTabs"] [data-baseweb="tab"]:hover { color:#6B9AB8 !important; background:rgba(0,201,167,.04) !important; }
  [data-testid="stTabs"] [aria-selected="true"] {
    color:#00C9A7 !important; border-bottom:2px solid #00C9A7 !important;
    background:rgba(0,201,167,.07) !important;
  }

  .sec-label {
    font-family:'DM Mono',monospace; font-size:9px; font-weight:500;
    letter-spacing:.18em; text-transform:uppercase; color:#2D4D66;
    margin:22px 0 10px; display:flex; align-items:center; gap:10px;
  }
  .sec-label::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,#162030 0%,transparent 100%); }

  .dash-header {
    display:flex; align-items:flex-end; justify-content:space-between;
    margin-bottom:1.6rem; padding-bottom:1.2rem; border-bottom:1px solid #162030;
  }
  .dash-title { font-family:'Syne',sans-serif; font-size:2.2rem; font-weight:800; color:#E8F0F7; letter-spacing:-.03em; line-height:1.05; }
  .dash-title span { color:#00C9A7; }
  .dash-sub { font-family:'DM Mono',monospace; font-size:9.5px; color:#2D4D66; letter-spacing:.1em; text-transform:uppercase; margin-top:6px; }
  .dash-badge { font-family:'DM Mono',monospace; font-size:9px; letter-spacing:.08em; text-transform:uppercase; color:#3D5F7A; border:1px solid #162030; border-radius:20px; padding:4px 12px; display:inline-block; margin-right:6px; }

  .icard {
    background:linear-gradient(135deg,#0D1825 0%,#091520 100%);
    border:1px solid #162030; border-radius:12px; padding:16px 18px;
    font-size:12.5px; color:#6B8BA4; line-height:1.7; height:100%;
    position:relative; overflow:hidden;
  }
  .icard::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; border-radius:3px 0 0 3px; }
  .icard.teal::before  { background:#00C9A7; }
  .icard.blue::before  { background:#0096FF; }
  .icard.amber::before { background:#FF8C42; }
  .icard.violet::before{ background:#B57BFF; }
  .icard strong { display:block; font-family:'Syne',sans-serif; font-weight:600; font-size:13px; color:#E8F0F7; margin-bottom:5px; }
  .icard .val { font-family:'DM Mono',monospace; color:#00C9A7; font-size:11px; }

  .hvac-calc-card {
    background:linear-gradient(135deg,#0D1825 0%,#091520 100%);
    border:1px solid #162030; border-radius:14px; padding:20px 22px;
    position:relative; overflow:hidden;
  }
  .hvac-calc-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
  .hvac-calc-card.amber::before { background:linear-gradient(90deg,#FF8C42,#FFB347); }
  .hvac-calc-card.violet::before{ background:linear-gradient(90deg,#B57BFF,#D4A8FF); }
  .hvac-calc-card.teal::before  { background:linear-gradient(90deg,#00C9A7,#00E8C3); }
  .hvac-calc-card.blue::before  { background:linear-gradient(90deg,#B57BFF,#0096FF); }
  .hvac-calc-label { font-family:'DM Mono',monospace; font-size:9px; letter-spacing:.15em; text-transform:uppercase; color:#2D4D66; margin-bottom:8px; }
  .hvac-calc-formula { font-family:'DM Mono',monospace; font-size:12px; color:#4E7090; margin-bottom:6px; }
  .hvac-calc-result { font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:700; line-height:1.1; }
  .hvac-calc-unit { font-family:'DM Mono',monospace; font-size:10px; color:#4E7090; margin-top:4px; }

  .badge-s1 { background:rgba(0,150,255,.12); color:#4AACFF; border:1px solid rgba(0,150,255,.22); padding:4px 12px; border-radius:20px; font-family:'DM Mono',monospace; font-size:10px; letter-spacing:.08em; text-transform:uppercase; display:inline-block; }
  .badge-s2 { background:rgba(0,201,167,.1); color:#00C9A7; border:1px solid rgba(0,201,167,.2); padding:4px 12px; border-radius:20px; font-family:'DM Mono',monospace; font-size:10px; letter-spacing:.08em; text-transform:uppercase; display:inline-block; }

  hr { border:none !important; border-top:1px solid #162030 !important; margin:1.2rem 0 !important; }
  [data-testid="stDataFrame"] { border:1px solid #162030; border-radius:10px; overflow:hidden; }
  .stCaption { font-family:'DM Mono',monospace !important; font-size:9px !important; color:#1E3348 !important; letter-spacing:.05em !important; }
  [data-testid="stCheckbox"] label { font-family:'DM Mono',monospace !important; font-size:10.5px !important; }
  ::-webkit-scrollbar { width:4px; height:4px; }
  ::-webkit-scrollbar-track { background:#060A10; }
  ::-webkit-scrollbar-thumb { background:#162030; border-radius:4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ALTAIR THEME
# ─────────────────────────────────────────────────────────────────────────────
GRID_C = "#162030"; LABEL_C = "#2D4D66"; TEXT_M = "#C8DAEA"; TEXT_C = "#6B8BA4"

def dark_theme():
    return {"config": {
        "background": "transparent",
        "view": {"fill": "transparent", "stroke": "transparent"},
        "axis": {"domainColor": GRID_C, "gridColor": GRID_C, "tickColor": "transparent",
                 "labelColor": LABEL_C, "titleColor": LABEL_C,
                 "labelFont": "DM Mono, monospace", "titleFont": "DM Mono, monospace",
                 "labelFontSize": 10, "titleFontSize": 10, "gridOpacity": 0.4, "labelPadding": 6},
        "legend": {"labelColor": TEXT_M, "titleColor": LABEL_C,
                   "labelFont": "DM Mono, monospace", "titleFont": "DM Mono, monospace",
                   "labelFontSize": 10, "titleFontSize": 10, "symbolStrokeWidth": 2, "symbolSize": 80, "padding": 8},
        "title": {"color": TEXT_M, "font": "Syne, sans-serif", "fontSize": 13},
        "point": {"filled": True},
    }}
alt.themes.register("dark_carbon", dark_theme)
alt.themes.enable("dark_carbon")

C_S1   = "#0096FF"; C_S2  = "#00C9A7"; C_TOT = "#FF8C42"
C_CUM  = "#B57BFF"; C_ROLL= "#FF4FA0"; C_PROJ= "#FFD166"
C_TGT  = "#EF4444"; C_HEAT= "#FF8C42"; C_COOL= "#B57BFF"

MONTHS     = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTH_NUMS = list(range(1, 13))

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Emission Factors")
    ef_diesel   = st.number_input("Diesel (kgCO₂e / L)",      value=2.68,   step=0.01,  format="%.3f")
    ef_gasoline = st.number_input("Gasoline (kgCO₂e / L)",    value=2.31,   step=0.01,  format="%.3f")
    ef_bus_km   = st.number_input("Bus/Van (kgCO₂e / km)",    value=0.089,  step=0.001, format="%.4f")
    ef_grid     = st.number_input("Grid (kgCO₂e / kWh)",      value=0.267,  step=0.001, format="%.4f")
    st.markdown("---")
    st.markdown("### 🌡️ HVAC — R410A Refrigerant")
    ef_refrigerant = st.number_input("R410A EF (kgCO₂e / kg)", value=2088.0, step=1.0,  format="%.0f",
                                      help="GWP100 of R410A — IPCC AR5")
    hvac_heat_kg   = st.number_input("Heating circuit (kg)",    value=15.0,   step=0.1,  format="%.1f")
    hvac_cool_kg   = st.number_input("Cooling circuit (kg)",    value=25.0,   step=0.1,  format="%.1f")
    st.markdown("---")
    st.markdown("### 🎛️ Chart overlays")
    show_rolling = st.checkbox("3-month rolling average", value=True)
    show_target  = st.checkbox("Reduction target (−10%)", value=True)
    show_proj    = st.checkbox("Linear projection",       value=True)
    show_band    = st.checkbox("Confidence band",         value=True)
    interp = st.selectbox("Interpolation", ["monotone","linear","step","basis"], index=0)
    st.markdown("---")
    st.markdown("**Framework** · GHG Protocol · 2025")
    st.markdown('<span class="badge-s1">Scope 1</span>&nbsp; Mobile + HVAC', unsafe_allow_html=True)
    st.markdown("")
    st.markdown('<span class="badge-s2">Scope 2</span>&nbsp; Electricity', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HVAC CALCULATIONS — single source of truth
# Everything stored in tCO₂e for chart mixing
# kgCO₂e computed separately for display only
# ─────────────────────────────────────────────────────────────────────────────
# Step 1: raw kgCO₂e (display labels only)
HVAC_HEAT_KGCO2E = hvac_heat_kg * ef_refrigerant          # e.g. 15×2088 = 31,320 kgCO₂e
HVAC_COOL_KGCO2E = hvac_cool_kg * ef_refrigerant          # e.g. 25×2088 = 52,200 kgCO₂e
HVAC_TOTAL_KGCO2E = HVAC_HEAT_KGCO2E + HVAC_COOL_KGCO2E  # 83,520 kgCO₂e

# Step 2: convert to tCO₂e for all calculations (÷1000 once, here only)
HVAC_HEAT_TCO2E  = HVAC_HEAT_KGCO2E / 1000   # 31.32 tCO₂e
HVAC_COOL_TCO2E  = HVAC_COOL_KGCO2E / 1000   # 52.20 tCO₂e
HVAC_TOTAL_TCO2E = HVAC_TOTAL_KGCO2E / 1000  # 83.52 tCO₂e

REFRIGERANT_TYPE = "R410A"
HVAC_HOURS       = 1700

# Step 3: monthly tCO₂e distribution (equal split across active months)
HEAT_MONTHS = [0,1,2,3,10,11]   # Jan Feb Mar Apr Nov Dec
COOL_MONTHS = [4,5,6,7,8,9]     # May Jun Jul Aug Sep Oct

hvac_heat_tco2e_mo = np.zeros(12)
hvac_cool_tco2e_mo = np.zeros(12)
for i in HEAT_MONTHS:
    hvac_heat_tco2e_mo[i] = HVAC_HEAT_TCO2E / len(HEAT_MONTHS)
for i in COOL_MONTHS:
    hvac_cool_tco2e_mo[i] = HVAC_COOL_TCO2E / len(COOL_MONTHS)

# Monthly kgCO₂e for chart C display (kgCO₂e axis)
hvac_heat_kgco2e_mo = hvac_heat_tco2e_mo * 1000
hvac_cool_kgco2e_mo = hvac_cool_tco2e_mo * 1000

hvac_heating_kwh = np.array([2287.5, 2316.8, 2391.0, 2415.5,    0,    0,
                                  0,      0,      0,      0, 2349.1, 2305.8])
hvac_cooling_kwh = np.array([   0,      0,      0,      0, 2445.0, 2500.0,
                              2502.3, 2498.5, 2456.8, 2403.7,    0,     0])

hvac_df = pd.DataFrame({
    "Month":             MONTHS,
    "Month_num":         MONTH_NUMS,
    "Heating_kWh":       hvac_heating_kwh,
    "Cooling_kWh":       hvac_cooling_kwh,
    "Heating_tCO2e":     hvac_heat_tco2e_mo,    # tCO₂e — for chart mixing
    "Cooling_tCO2e":     hvac_cool_tco2e_mo,    # tCO₂e — for chart mixing
    "Heating_kgCO2e":    hvac_heat_kgco2e_mo,   # kgCO₂e — for HVAC-only charts
    "Cooling_kgCO2e":    hvac_cool_kgco2e_mo,   # kgCO₂e — for HVAC-only charts
})
hvac_df["Month"] = pd.Categorical(hvac_df["Month"], categories=MONTHS, ordered=True)

# ─────────────────────────────────────────────────────────────────────────────
# VEHICLE & BUS DATA
# ─────────────────────────────────────────────────────────────────────────────
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

elec_kwh = np.array([28429,30287,30262,19625,22097,37937,
                     48569,43843,38143,28139,23532,23039], dtype=float)
elec_df = pd.DataFrame({
    "Month":     MONTHS,
    "Month_num": MONTH_NUMS,
    "kWh":       elec_kwh,
    "Meters":    np.full(12, 15),
})
elec_df["MWh"]   = elec_df["kWh"] / 1000
elec_df["tCO2e"] = elec_df["kWh"] * ef_grid / 1000

# ─────────────────────────────────────────────────────────────────────────────
# AGGREGATES — all in tCO₂e
# ─────────────────────────────────────────────────────────────────────────────
total_s2      = elec_df["tCO2e"].sum()
total_s1v     = vehicle_raw["tCO2e"].sum()
total_s1b     = bus_raw["tCO2e"].sum()
total_s1heat  = HVAC_HEAT_TCO2E    # 31.32 tCO₂e
total_s1cool  = HVAC_COOL_TCO2E    # 52.20 tCO₂e
total_s1hvac  = HVAC_TOTAL_TCO2E   # 83.52 tCO₂e
total_s1      = total_s1v + total_s1b + total_s1hvac
total_all     = total_s1 + total_s2
total_kwh     = int(elec_kwh.sum())

# Monthly Scope 1 in tCO₂e — no further division needed
s1_mobile = np.zeros(12)
for _, row in vehicle_raw.iterrows():
    s1_mobile[int(row["Month_num"])-1] += row["tCO2e"]
for _, row in bus_raw.iterrows():
    s1_mobile[int(row["Month_num"])-1] += row["tCO2e"]

s1_monthly    = s1_mobile + hvac_heat_tco2e_mo + hvac_cool_tco2e_mo
s2_monthly    = elec_df["tCO2e"].values.copy()
total_monthly = s1_monthly + s2_monthly

# ─────────────────────────────────────────────────────────────────────────────
# DERIVED SERIES
# ─────────────────────────────────────────────────────────────────────────────
def rolling_n(arr, n=3):
    return pd.Series(arr).rolling(n, center=True, min_periods=1).mean().values

roll_s1    = rolling_n(s1_monthly)
roll_s2    = rolling_n(s2_monthly)
roll_total = rolling_n(total_monthly)
roll_std   = rolling_n(np.abs(total_monthly - total_monthly.mean()))

cum_s1    = np.cumsum(s1_monthly)
cum_s2    = np.cumsum(s2_monthly)
cum_total = np.cumsum(total_monthly)

x_fit = np.arange(12, dtype=float)
proj_s2    = np.polyval(np.polyfit(x_fit, s2_monthly, 1),    x_fit)
proj_total = np.polyval(np.polyfit(x_fit, total_monthly, 1), x_fit)

target_monthly = np.full(12, total_monthly.mean() * 0.90)
mom_change     = np.concatenate([[np.nan], np.diff(total_monthly)/total_monthly[:-1]*100])
seasonal_idx   = total_monthly / total_monthly.mean()
band_upper     = roll_total + roll_std * 0.5
band_lower     = np.maximum(roll_total - roll_std * 0.5, 0)

trend_df = pd.DataFrame({
    "Month":      MONTHS, "Month_num": MONTH_NUMS,
    "Scope1":     s1_monthly,    "Scope2":    s2_monthly,
    "Total":      total_monthly, "HVAC_Heat": hvac_heat_tco2e_mo,
    "HVAC_Cool":  hvac_cool_tco2e_mo,
    "Roll_S1":    roll_s1,       "Roll_S2":   roll_s2,
    "Roll_Total": roll_total,    "Band_Upper":band_upper,
    "Band_Lower": band_lower,    "Cum_S1":    cum_s1,
    "Cum_S2":     cum_s2,        "Cum_Total": cum_total,
    "Proj_S2":    proj_s2,       "Proj_Total":proj_total,
    "Target":     target_monthly,"MoM_Change":mom_change,
    "Seasonal":   seasonal_idx,  "kWh":       elec_kwh,
    "Pct_Annual": cum_total / total_all * 100,
})
trend_df["Month"] = pd.Categorical(trend_df["Month"], categories=MONTHS, ordered=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def mx(angle=0):
    return alt.X("Month:N", sort=MONTHS, title=None,
                 axis=alt.Axis(labelAngle=angle, labelFontSize=10, tickColor="transparent"))

def smooth_line(df, y_col, color, width=2.5, dash=None, opacity=1.0, label=None, y_title="tCO₂e"):
    props = dict(color=color, strokeWidth=width, opacity=opacity, interpolate=interp)
    if dash: props["strokeDash"] = dash
    return alt.Chart(df).mark_line(**props).encode(
        x=mx(), y=alt.Y(f"{y_col}:Q", title=y_title),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip(f"{y_col}:Q", format=".4f", title=label or y_col)],
    )

def glow_point(df, y_col, color, size=60, y_title="tCO₂e", fmt=".4f"):
    return alt.Chart(df).mark_point(color=color, filled=True, size=size, opacity=0.9).encode(
        x=mx(), y=alt.Y(f"{y_col}:Q", title=y_title),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip(f"{y_col}:Q", format=fmt)],
    )

def area_fill(df, y_col, color, opacity=0.13, y_title="tCO₂e"):
    return alt.Chart(df).mark_area(
        color=color, opacity=opacity, interpolate=interp,
        line={"color": color, "strokeWidth": 2.2, "opacity": .9},
    ).encode(
        x=mx(), y=alt.Y(f"{y_col}:Q", title=y_title),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip(f"{y_col}:Q", format=".4f", title=y_title)],
    )

def hline(val, color, dash=[5,3]):
    return alt.Chart(pd.DataFrame({"y":[val]})).mark_rule(
        color=color, strokeDash=dash, strokeWidth=1.1, opacity=.6
    ).encode(y="y:Q")

def hp(h=300): return {"height": h}

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
  <div>
    <div class="dash-title">🌿 GHG Carbon <span>Monitor</span></div>
    <div class="dash-sub">GHG Protocol · Scope 1 & 2 · Medtech · Tunisia · 2025</div>
  </div>
  <div style="text-align:right">
    <span class="dash-badge">Scope 1 · Mobile + HVAC</span>
    <span class="dash-badge">Scope 2 · Electricity</span><br><br>
    <span style="font-family:DM Mono,monospace;font-size:9px;color:#1A2D40;letter-spacing:.06em">
      R410A · {HVAC_TOTAL_KGCO2E:,.0f} kgCO₂e HVAC · 2025
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

k1,k2,k3,k4,k5,k6 = st.columns(6)
k1.metric("Grand Total",       f"{total_all:.2f}",               "tCO₂e · S1+S2")
k2.metric("Scope 1",           f"{total_s1:.2f}",                "tCO₂e · mobile+HVAC")
k3.metric("Scope 2",           f"{total_s2:.2f}",                "tCO₂e · electricity")
k4.metric("🔥 HVAC Heating",  f"{HVAC_HEAT_KGCO2E:,.0f}",       "kgCO₂e · R410A")
k5.metric("❄️ HVAC Cooling",  f"{HVAC_COOL_KGCO2E:,.0f}",       "kgCO₂e · R410A")
k6.metric("S2 Share",          f"{total_s2/total_all*100:.1f}%", "of total emissions")
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
    "◉ Overview","〰 Trend & Curves","∫ Cumulative",
    "⧖ Seasonality","🚗 Scope 1","⚡ Scope 2",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    cl, cr = st.columns([1, 1.65])
    with cl:
        st.markdown('<div class="sec-label">Emissions split by source</div>', unsafe_allow_html=True)
        donut_df = pd.DataFrame({
            "Scope": ["S1 · Mobile","S1 · HVAC Heating","S1 · HVAC Cooling","Scope 2 · Electricity"],
            "tCO2e": [round(total_s1v+total_s1b,4), round(total_s1heat,4),
                      round(total_s1cool,4),         round(total_s2,4)],
            "Pct":   [round((total_s1v+total_s1b)/total_all*100,1),
                      round(total_s1heat/total_all*100,1),
                      round(total_s1cool/total_all*100,1),
                      round(total_s2/total_all*100,1)],
        })
        arc = alt.Chart(donut_df).mark_arc(innerRadius=78, outerRadius=132, padAngle=0.025).encode(
            theta=alt.Theta("tCO2e:Q"),
            color=alt.Color("Scope:N",
                scale=alt.Scale(domain=donut_df["Scope"].tolist(),
                                range=[C_S1, C_HEAT, C_COOL, C_S2]),
                legend=alt.Legend(orient="bottom", labelLimit=400, symbolType="circle", symbolSize=90, labelFontSize=10)),
            tooltip=[alt.Tooltip("Scope:N"), alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e"),
                     alt.Tooltip("Pct:Q", format=".1f", title="%")],
        ).properties(height=310)
        st.altair_chart(arc, use_container_width=True)

    with cr:
        st.markdown('<div class="sec-label">Monthly stacked emissions — all sources</div>', unsafe_allow_html=True)
        ov_long = trend_df[["Month","Scope1","Scope2"]].melt(
            id_vars="Month", value_vars=["Scope1","Scope2"], var_name="Scope", value_name="tCO2e")
        ov_long["Scope"] = ov_long["Scope"].map({"Scope1":"Scope 1","Scope2":"Scope 2"})
        stacked = alt.Chart(ov_long).mark_bar(
            cornerRadiusTopLeft=4, cornerRadiusTopRight=4, width={"band":.68}
        ).encode(
            x=mx(), y=alt.Y("tCO2e:Q", stack="zero", title="tCO₂e"),
            color=alt.Color("Scope:N",
                scale=alt.Scale(domain=["Scope 1","Scope 2"], range=[C_S1, C_S2]),
                legend=alt.Legend(orient="top", title=None)),
            tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Scope:N"),
                     alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e")],
        )
        st.altair_chart((stacked + smooth_line(trend_df,"Total",C_TOT,2.2) +
                         glow_point(trend_df,"Total",C_TOT,50)).properties(**hp(310)),
                        use_container_width=True)

    st.markdown('<div class="sec-label">Scope 1 — source breakdown</div>', unsafe_allow_html=True)
    src_df = pd.DataFrame({
        "Source":   ["Diesel fleet","Gasoline Feb","Gasoline Dec","Bus/Van","HVAC Heating","HVAC Cooling"],
        "tCO2e":    [vehicle_raw.loc[vehicle_raw["Fuel_type"]=="Diesel","tCO2e"].sum(),
                     vehicle_raw.iloc[1]["tCO2e"], vehicle_raw.iloc[2]["tCO2e"],
                     bus_raw["tCO2e"].sum(), total_s1heat, total_s1cool],
        "Category": ["Vehicle","Vehicle","Vehicle","Distance","HVAC Heating","HVAC Cooling"],
    })
    src_bar = alt.Chart(src_df).mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5).encode(
        x=alt.X("tCO2e:Q", title="tCO₂e"),
        y=alt.Y("Source:N", sort="-x", title=None),
        color=alt.Color("Category:N",
            scale=alt.Scale(domain=["Vehicle","Distance","HVAC Heating","HVAC Cooling"],
                            range=[C_S1, C_S2, C_HEAT, C_COOL]),
            legend=alt.Legend(orient="right")),
        tooltip=[alt.Tooltip("Source:N"), alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e")],
    ).properties(height=185)
    st.altair_chart(src_bar + src_bar.mark_text(align="left", dx=6, fontSize=10, color=TEXT_M,
        font="DM Mono, monospace").encode(text=alt.Text("tCO2e:Q", format=".3f")),
        use_container_width=True)

    ia, ib, ic, id_ = st.columns(4)
    with ia:
        st.markdown(f"""<div class="icard blue"><strong>🚗 Diesel — top Scope 1 event</strong>
            <span class="val">{vehicle_raw.iloc[0]['tCO2e']:.3f} tCO₂e</span> from
            1,742 L diesel in February.</div>""", unsafe_allow_html=True)
    with ib:
        st.markdown(f"""<div class="icard amber"><strong>🔥 HVAC Heating — R410A</strong>
            <span class="val">{HVAC_HEAT_KGCO2E:,.0f} kgCO₂e = {total_s1heat:.2f} tCO₂e</span>
            · 15 kg × 2,088 · Jan–Apr &amp; Nov–Dec.</div>""", unsafe_allow_html=True)
    with ic:
        st.markdown(f"""<div class="icard violet"><strong>❄️ HVAC Cooling — R410A</strong>
            <span class="val">{HVAC_COOL_KGCO2E:,.0f} kgCO₂e = {total_s1cool:.2f} tCO₂e</span>
            · 25 kg × 2,088 · May–Oct.</div>""", unsafe_allow_html=True)
    with id_:
        st.markdown(f"""<div class="icard teal"><strong>⚡ Electricity dominates</strong>
            <span class="val">{total_s2/total_all*100:.1f}%</span> of total GHG.
            July peak: 48,569 kWh → {elec_df.iloc[6]['tCO2e']:.2f} tCO₂e.</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TREND & CURVES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-label">All emission series — monthly tCO₂e</div>', unsafe_allow_html=True)
    chart_A = (smooth_line(trend_df,"Scope1",C_S1,2.0,label="Scope 1") + glow_point(trend_df,"Scope1",C_S1,42) +
               smooth_line(trend_df,"Scope2",C_S2,2.0,label="Scope 2") + glow_point(trend_df,"Scope2",C_S2,42) +
               smooth_line(trend_df,"Total", C_TOT,2.6,label="Total")  + glow_point(trend_df,"Total", C_TOT,58))
    if show_rolling:
        chart_A = chart_A + smooth_line(trend_df,"Roll_S1",C_S1,1.2,[4,3],.5,"Roll.S1")
        chart_A = chart_A + smooth_line(trend_df,"Roll_S2",C_S2,1.2,[4,3],.5,"Roll.S2")
        chart_A = chart_A + smooth_line(trend_df,"Roll_Total",C_ROLL,1.8,[3,2],.8,"Roll.Total")
    if show_band:
        chart_A = alt.Chart(trend_df).mark_area(color=C_ROLL,opacity=0.05,interpolate=interp).encode(
            x=mx(), y=alt.Y("Band_Lower:Q",title="tCO₂e"), y2="Band_Upper:Q") + chart_A
    if show_target:
        chart_A = chart_A + hline(target_monthly[0], C_TGT)
    if show_proj:
        chart_A = chart_A + smooth_line(trend_df,"Proj_Total",C_PROJ,1.4,[5,3],.65,"Projection")
    st.altair_chart(chart_A.properties(**hp(360)), use_container_width=True)

    st.markdown('<div class="sec-label">Stacked area — scope contributions</div>', unsafe_allow_html=True)
    area_long = trend_df[["Month","Scope1","Scope2"]].melt(
        id_vars="Month", value_vars=["Scope1","Scope2"], var_name="Scope", value_name="tCO2e")
    area_long["Scope"] = area_long["Scope"].map({"Scope1":"Scope 1","Scope2":"Scope 2"})
    area_stk = alt.Chart(area_long).mark_area(opacity=0.78,interpolate=interp).encode(
        x=mx(), y=alt.Y("tCO2e:Q",stack="zero",title="tCO₂e"),
        color=alt.Color("Scope:N",
            scale=alt.Scale(domain=["Scope 1","Scope 2"],range=[C_S1,C_S2]),
            legend=alt.Legend(orient="top",title=None)),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Scope:N"),alt.Tooltip("tCO2e:Q",format=".4f",title="tCO₂e")],
    )
    st.altair_chart((area_stk+smooth_line(trend_df,"Total",C_TOT,2.2)+
                     glow_point(trend_df,"Total",C_TOT,42)).properties(**hp(260)),use_container_width=True)

    cc, cd = st.columns(2)
    with cc:
        st.markdown('<div class="sec-label">Month-over-month Δ total (%)</div>', unsafe_allow_html=True)
        mom_df = trend_df.dropna(subset=["MoM_Change"]).copy()
        mom_df["Dir"] = np.where(mom_df["MoM_Change"]>=0,"▲ Increase","▼ Decrease")
        mom_bar = alt.Chart(mom_df).mark_bar(cornerRadiusTopLeft=3,cornerRadiusTopRight=3,
            cornerRadiusBottomLeft=3,cornerRadiusBottomRight=3,width={"band":.6}).encode(
            x=mx(), y=alt.Y("MoM_Change:Q",title="% vs prior month",axis=alt.Axis(format=".1f")),
            color=alt.Color("Dir:N",scale=alt.Scale(domain=["▲ Increase","▼ Decrease"],range=[C_TGT,C_S2]),
                            legend=alt.Legend(orient="top",title=None)),
            tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("MoM_Change:Q",format=".1f",title="MoM %")],
        )
        zero = alt.Chart(pd.DataFrame({"y":[0]})).mark_rule(color=GRID_C,strokeWidth=1).encode(y="y:Q")
        st.altair_chart((mom_bar+zero+smooth_line(mom_df,"MoM_Change",C_ROLL,1.4,[3,2],.5,"Trend")
                         ).properties(**hp(250)),use_container_width=True)
    with cd:
        st.markdown('<div class="sec-label">kWh vs Scope 2 tCO₂e scatter</div>', unsafe_allow_html=True)
        scatter = alt.Chart(trend_df).mark_circle(size=85,opacity=.88).encode(
            x=alt.X("kWh:Q",title="Monthly kWh",axis=alt.Axis(format=",.0f")),
            y=alt.Y("Scope2:Q",title="tCO₂e (S2)"),
            color=alt.Color("Month:N",scale=alt.Scale(scheme="plasma"),
                            legend=alt.Legend(orient="right",title="Month",labelFontSize=9,symbolSize=55)),
            tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("kWh:Q",format=",.0f",title="kWh"),
                     alt.Tooltip("Scope2:Q",format=".3f",title="tCO₂e")],
        )
        st.altair_chart((scatter+scatter.transform_regression("kWh","Scope2").mark_line(
            color=C_PROJ,strokeDash=[5,3],strokeWidth=1.8)).properties(**hp(250)),use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CUMULATIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-label">Year-to-date cumulative tCO₂e</div>', unsafe_allow_html=True)
    cum_chart = (area_fill(trend_df,"Cum_Total",C_CUM,0.09) +
                 smooth_line(trend_df,"Cum_Total",C_CUM,2.6,label="Total cumul.") + glow_point(trend_df,"Cum_Total",C_CUM,58) +
                 smooth_line(trend_df,"Cum_S2",C_S2,2.0,label="S2 cumul.")       + glow_point(trend_df,"Cum_S2",C_S2,42) +
                 smooth_line(trend_df,"Cum_S1",C_S1,1.8,[4,3],.9,"S1 cumul.")    + glow_point(trend_df,"Cum_S1",C_S1,42))
    ey = trend_df[trend_df["Month"]=="Dec"]
    for col,color in [("Cum_Total",C_CUM),("Cum_S2",C_S2),("Cum_S1",C_S1)]:
        cum_chart = cum_chart + alt.Chart(ey).mark_text(
            align="right",dx=-7,dy=-11,fontSize=10,color=color,font="DM Mono, monospace"
        ).encode(x=mx(),y=alt.Y(f"{col}:Q"),text=alt.Text(f"{col}:Q",format=".2f"))
    st.altair_chart(cum_chart.properties(**hp(330)),use_container_width=True)

    cl2,cr2 = st.columns(2)
    with cl2:
        st.markdown('<div class="sec-label">YTD % of annual total</div>', unsafe_allow_html=True)
        pct_a = alt.Chart(trend_df).mark_area(color=C_CUM,opacity=0.11,interpolate=interp,
            line={"color":C_CUM,"strokeWidth":2.2}).encode(
            x=mx(), y=alt.Y("Pct_Annual:Q",title="% of annual",scale=alt.Scale(domain=[0,108])),
            tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Pct_Annual:Q",format=".1f",title="% annual")],
        )
        st.altair_chart((pct_a+glow_point(trend_df,"Pct_Annual",C_CUM,52,"% of annual")+
                         hline(50,TEXT_C,[4,3])+hline(100,C_TGT,[2,2])).properties(**hp(260)),use_container_width=True)
    with cr2:
        st.markdown('<div class="sec-label">Cumulative S1 vs S2 overlap</div>', unsafe_allow_html=True)
        st.altair_chart((area_fill(trend_df,"Cum_S2",C_S2,0.22)+area_fill(trend_df,"Cum_S1",C_S1,0.32)+
                         smooth_line(trend_df,"Cum_S2",C_S2,2.0,label="S2")+
                         smooth_line(trend_df,"Cum_S1",C_S1,2.0,label="S1")).properties(**hp(260)),use_container_width=True)

    ct = trend_df[["Month","Scope1","Scope2","Total","Cum_S1","Cum_S2","Cum_Total","Pct_Annual"]].copy()
    ct.columns = ["Month","S1 (t)","S2 (t)","Total (t)","Cum S1","Cum S2","Cum Total","% Annual"]
    for c in ["S1 (t)","S2 (t)","Total (t)","Cum S1","Cum S2","Cum Total"]:
        ct[c] = ct[c].map("{:.4f}".format)
    ct["% Annual"] = ct["% Annual"].map("{:.1f}%".format)
    st.dataframe(ct,use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — SEASONALITY
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    cs, cb = st.columns(2)
    with cs:
        st.markdown('<div class="sec-label">Seasonal index — ratio to monthly mean</div>', unsafe_allow_html=True)
        st.altair_chart((area_fill(trend_df,"Seasonal",C_TOT,0.12,"Index")+
                         smooth_line(trend_df,"Seasonal",C_TOT,2.4,y_title="Index",label="Seasonal")+
                         glow_point(trend_df,"Seasonal",C_TOT,55,"Index")+hline(1.0,TEXT_C,[4,3])
                         ).properties(**hp(270)),use_container_width=True)
    with cb:
        st.markdown('<div class="sec-label">Monthly share of annual total — S1 vs S2</div>', unsafe_allow_html=True)
        share_data = []
        for i,m in enumerate(MONTHS):
            share_data.append({"Month":m,"Scope":"Scope 1","Share":s1_monthly[i]/total_s1*100 if total_s1>0 else 0})
            share_data.append({"Month":m,"Scope":"Scope 2","Share":s2_monthly[i]/total_s2*100})
        share_df = pd.DataFrame(share_data)
        share_df["Month"] = pd.Categorical(share_df["Month"],categories=MONTHS,ordered=True)
        st.altair_chart(alt.Chart(share_df).mark_bar(cornerRadiusTopLeft=3,cornerRadiusTopRight=3,width={"band":.6}).encode(
            x=mx(), y=alt.Y("Share:Q",title="% of annual scope total"),
            color=alt.Color("Scope:N",scale=alt.Scale(domain=["Scope 1","Scope 2"],range=[C_S1,C_S2]),
                            legend=alt.Legend(orient="top",title=None)),
            xOffset=alt.XOffset("Scope:N"),
            tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Scope:N"),alt.Tooltip("Share:Q",format=".1f",title="%")],
        ).properties(**hp(270)),use_container_width=True)

    st.markdown('<div class="sec-label">Monthly total tCO₂e — radial</div>', unsafe_allow_html=True)
    st.altair_chart(alt.Chart(trend_df).mark_arc(innerRadius=45).encode(
        theta=alt.Theta("Month_num:O",stack=True),
        radius=alt.Radius("Total:Q",scale=alt.Scale(type="sqrt",zero=True,rangeMin=45)),
        color=alt.Color("Total:Q",scale=alt.Scale(scheme="plasma"),legend=alt.Legend(title="tCO₂e",orient="right")),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Total:Q",format=".4f",title="Total tCO₂e")],
    ).properties(height=300),use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SCOPE 1
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<span class="badge-s1">Scope 1</span>&nbsp; Mobile Combustion + HVAC (R410A)', unsafe_allow_html=True)
    st.markdown(" ")

    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Total Scope 1",  f"{total_s1:.2f}",             "tCO₂e")
    m2.metric("Fuel vouchers",  f"{total_s1v:.3f}",            "tCO₂e · 3 tx")
    m3.metric("Bus / Van",      f"{total_s1b:.4f}",            "tCO₂e · 5 trips")
    m4.metric("🔥 HVAC Heat",  f"{HVAC_HEAT_KGCO2E:,.0f}",    "kgCO₂e · R410A")
    m5.metric("❄️ HVAC Cool",  f"{HVAC_COOL_KGCO2E:,.0f}",    "kgCO₂e · R410A")

    # ── R410A Calculation Panel ───────────────────────────────────────────────
    st.markdown('<div class="sec-label">R410A refrigerant — emission calculation</div>', unsafe_allow_html=True)
    ra, rb, rc, rd = st.columns(4)
    with ra:
        st.markdown(f"""<div class="hvac-calc-card blue">
            <div class="hvac-calc-label">Refrigerant type</div>
            <div class="hvac-calc-result" style="color:#B57BFF;font-size:2rem">{REFRIGERANT_TYPE}</div>
            <div class="hvac-calc-unit">EF = {ef_refrigerant:,.0f} kgCO₂e / kg</div>
        </div>""", unsafe_allow_html=True)
    with rb:
        st.markdown(f"""<div class="hvac-calc-card amber">
            <div class="hvac-calc-label">🔥 Heating load</div>
            <div class="hvac-calc-formula">{hvac_heat_kg:.0f} kg × {ef_refrigerant:,.0f} kgCO₂e/kg</div>
            <div class="hvac-calc-result" style="color:#FF8C42">{HVAC_HEAT_KGCO2E:,.0f} <span style="font-size:.9rem;font-weight:400">kgCO₂e</span></div>
            <div class="hvac-calc-unit">= {total_s1heat:.2f} tCO₂e · Scope 1</div>
        </div>""", unsafe_allow_html=True)
    with rc:
        st.markdown(f"""<div class="hvac-calc-card violet">
            <div class="hvac-calc-label">❄️ Cooling load</div>
            <div class="hvac-calc-formula">{hvac_cool_kg:.0f} kg × {ef_refrigerant:,.0f} kgCO₂e/kg</div>
            <div class="hvac-calc-result" style="color:#B57BFF">{HVAC_COOL_KGCO2E:,.0f} <span style="font-size:.9rem;font-weight:400">kgCO₂e</span></div>
            <div class="hvac-calc-unit">= {total_s1cool:.2f} tCO₂e · Scope 1</div>
        </div>""", unsafe_allow_html=True)
    with rd:
        st.markdown(f"""<div class="hvac-calc-card teal">
            <div class="hvac-calc-label">∑ Total HVAC</div>
            <div class="hvac-calc-formula">{HVAC_HEAT_KGCO2E:,.0f} + {HVAC_COOL_KGCO2E:,.0f} kgCO₂e</div>
            <div class="hvac-calc-result" style="color:#00C9A7">{HVAC_TOTAL_KGCO2E:,.0f} <span style="font-size:.9rem;font-weight:400">kgCO₂e</span></div>
            <div class="hvac-calc-unit">= {HVAC_TOTAL_TCO2E:.2f} tCO₂e · Scope 1</div>
        </div>""", unsafe_allow_html=True)

    # ── Chart A: Stacked Scope 1 monthly ─────────────────────────────────────
    st.markdown('<div class="sec-label">Monthly Scope 1 — stacked by source (fuel + HVAC heating + HVAC cooling)</div>', unsafe_allow_html=True)
    fuel_mo = np.zeros(12)
    bus_mo  = np.zeros(12)
    for _, row in vehicle_raw.iterrows():
        fuel_mo[int(row["Month_num"])-1] += row["tCO2e"]
    for _, row in bus_raw.iterrows():
        bus_mo[int(row["Month_num"])-1] += row["tCO2e"]

    s1_long = pd.DataFrame({
        "Month":   MONTHS * 4,
        "Type":    ["Fuel vouchers"]*12 + ["Bus/Van"]*12 + ["HVAC Heating"]*12 + ["HVAC Cooling"]*12,
        "tCO2e":  list(fuel_mo) + list(bus_mo) + list(hvac_heat_tco2e_mo) + list(hvac_cool_tco2e_mo),
        "kgCO2e": [0.0]*24 + list(hvac_heat_kgco2e_mo) + list(hvac_cool_kgco2e_mo),
        "Unit":   ["tCO₂e"]*24 + ["kgCO₂e"]*24,
    })
    s1_long["Month"] = pd.Categorical(s1_long["Month"], categories=MONTHS, ordered=True)

    fuel_bus_long = s1_long[s1_long["Unit"]=="tCO₂e"]
    hvac_long_bar = s1_long[s1_long["Unit"]=="kgCO₂e"]

    col_scale = alt.Scale(domain=["Fuel vouchers","Bus/Van","HVAC Heating","HVAC Cooling"],
                          range=[C_S1,"#54A0FF",C_HEAT,C_COOL])
    bars_fuel = alt.Chart(fuel_bus_long).mark_bar(cornerRadiusTopLeft=4,cornerRadiusTopRight=4,width={"band":.7}).encode(
        x=mx(), y=alt.Y("tCO2e:Q",stack="zero",title="tCO₂e"),
        color=alt.Color("Type:N",scale=col_scale,legend=alt.Legend(orient="top",title=None)),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Type:N"),alt.Tooltip("tCO2e:Q",format=".5f",title="tCO₂e")],
    )
    bars_hvac = alt.Chart(hvac_long_bar).mark_bar(cornerRadiusTopLeft=4,cornerRadiusTopRight=4,width={"band":.7}).encode(
        x=mx(), y=alt.Y("tCO2e:Q",stack="zero",title="tCO₂e"),
        color=alt.Color("Type:N",scale=col_scale,legend=None),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Type:N"),alt.Tooltip("kgCO2e:Q",format=",.2f",title="kgCO₂e")],
    )
    st.altair_chart((bars_fuel+bars_hvac+smooth_line(trend_df,"Scope1",C_ROLL,1.8,[4,2],label="Total S1")+
                     glow_point(trend_df,"Scope1",C_ROLL,42)).properties(**hp(300)),use_container_width=True)
    st.caption(f"Y-axis = tCO₂e · HVAC tooltip shows kgCO₂e · Heating: {HVAC_HEAT_KGCO2E:,.0f} kgCO₂e/yr · Cooling: {HVAC_COOL_KGCO2E:,.0f} kgCO₂e/yr")

    # ── Chart B: HVAC kWh bars + kgCO₂e lines ────────────────────────────────
    st.markdown('<div class="sec-label">HVAC — heating & cooling loads · kWh bars + kgCO₂e lines</div>', unsafe_allow_html=True)
    hvac_long2 = pd.DataFrame({
        "Month":   MONTHS*2,
        "Type":    ["🔥 Heating"]*12 + ["❄️ Cooling"]*12,
        "kWh":     list(hvac_heating_kwh) + list(hvac_cooling_kwh),
        "kgCO2e":  list(hvac_heat_kgco2e_mo) + list(hvac_cool_kgco2e_mo),
    })
    hvac_long2["Month"] = pd.Categorical(hvac_long2["Month"],categories=MONTHS,ordered=True)

    hvac_bars2 = alt.Chart(hvac_long2[hvac_long2["kWh"]>0]).mark_bar(
        cornerRadiusTopLeft=4,cornerRadiusTopRight=4,width={"band":.75}
    ).encode(
        x=mx(), y=alt.Y("kWh:Q",title="kWh (load)",axis=alt.Axis(titleColor=TEXT_C)),
        color=alt.Color("Type:N",scale=alt.Scale(domain=["🔥 Heating","❄️ Cooling"],range=[C_HEAT,C_COOL]),
                        legend=alt.Legend(orient="top",title="HVAC Load",labelFontSize=11)),
        xOffset=alt.XOffset("Type:N"),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Type:N"),
                 alt.Tooltip("kWh:Q",format=",.1f",title="kWh"),
                 alt.Tooltip("kgCO2e:Q",format=",.2f",title="kgCO₂e (S1)")],
    )
    heat_df2 = hvac_df[hvac_df["Heating_kWh"]>0].copy()
    cool_df2 = hvac_df[hvac_df["Cooling_kWh"]>0].copy()

    heat_line2 = alt.Chart(heat_df2).mark_line(color=C_HEAT,strokeWidth=2.4,interpolate=interp).encode(
        x=mx(), y=alt.Y("Heating_kgCO2e:Q",title="kgCO₂e",axis=alt.Axis(titleColor=C_HEAT)),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Heating_kgCO2e:Q",format=",.2f",title="Heating kgCO₂e")],
    )
    heat_pts2 = alt.Chart(heat_df2).mark_point(color=C_HEAT,filled=True,size=60,shape="triangle-up").encode(
        x=mx(), y=alt.Y("Heating_kgCO2e:Q"),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Heating_kgCO2e:Q",format=",.2f",title="Heating kgCO₂e")],
    )
    cool_line2 = alt.Chart(cool_df2).mark_line(color=C_COOL,strokeWidth=2.4,interpolate=interp,strokeDash=[4,2]).encode(
        x=mx(), y=alt.Y("Cooling_kgCO2e:Q",title="kgCO₂e"),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Cooling_kgCO2e:Q",format=",.2f",title="Cooling kgCO₂e")],
    )
    cool_pts2 = alt.Chart(cool_df2).mark_point(color=C_COOL,filled=True,size=60,shape="triangle-down").encode(
        x=mx(), y=alt.Y("Cooling_kgCO2e:Q"),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Cooling_kgCO2e:Q",format=",.2f",title="Cooling kgCO₂e")],
    )
    st.altair_chart(alt.layer(hvac_bars2,heat_line2+heat_pts2,cool_line2+cool_pts2
                              ).resolve_scale(y="independent").properties(**hp(320)),use_container_width=True)
    st.caption(f"Bars = kWh (left axis) · △ amber = heating {HVAC_HEAT_KGCO2E:,.0f} kgCO₂e/yr · ▽ violet = cooling {HVAC_COOL_KGCO2E:,.0f} kgCO₂e/yr · Right axis = kgCO₂e · R410A @ {ef_refrigerant:,.0f} kgCO₂e/kg")

    # ── Chart C: HVAC kgCO₂e area — both on same axis ────────────────────────
    st.markdown('<div class="sec-label">HVAC kgCO₂e — heating vs cooling, both Scope 1, same axis</div>', unsafe_allow_html=True)
    c_heat_area = alt.Chart(hvac_df).mark_area(color=C_HEAT,opacity=0.14,interpolate=interp,
        line={"color":C_HEAT,"strokeWidth":2.2}).encode(
        x=mx(), y=alt.Y("Heating_kgCO2e:Q",title="kgCO₂e",stack=None),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Heating_kgCO2e:Q",format=",.2f",title="Heating kgCO₂e (S1)")],
    )
    c_cool_area = alt.Chart(hvac_df).mark_area(color=C_COOL,opacity=0.14,interpolate=interp,
        line={"color":C_COOL,"strokeWidth":2.2,"strokeDash":[4,2]}).encode(
        x=mx(), y=alt.Y("Cooling_kgCO2e:Q",title="kgCO₂e",stack=None),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Cooling_kgCO2e:Q",format=",.2f",title="Cooling kgCO₂e (S1)")],
    )
    c_heat_pts = alt.Chart(hvac_df).mark_point(color=C_HEAT,filled=True,size=55).encode(
        x=mx(), y=alt.Y("Heating_kgCO2e:Q"),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Heating_kgCO2e:Q",format=",.2f",title="Heating kgCO₂e")],
    )
    c_cool_pts = alt.Chart(hvac_df).mark_point(color=C_COOL,filled=True,size=55).encode(
        x=mx(), y=alt.Y("Cooling_kgCO2e:Q"),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Cooling_kgCO2e:Q",format=",.2f",title="Cooling kgCO₂e")],
    )
    st.altair_chart((c_heat_area+c_cool_area+c_heat_pts+c_cool_pts).properties(**hp(280)),use_container_width=True)
    st.caption(f"Amber = heating · {hvac_heat_kg:.0f} kg × {ef_refrigerant:,.0f} = {HVAC_HEAT_KGCO2E:,.0f} kgCO₂e  ·  Violet = cooling · {hvac_cool_kg:.0f} kg × {ef_refrigerant:,.0f} = {HVAC_COOL_KGCO2E:,.0f} kgCO₂e  ·  Both Scope 1")

    # ── Chart D: Cumulative S1 ────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Cumulative Scope 1 — mobile vs HVAC heating vs HVAC cooling</div>', unsafe_allow_html=True)
    cum_s1_df = pd.DataFrame({
        "Month":  MONTHS*4,
        "Series": ["Mobile"]*12+["HVAC Heating"]*12+["HVAC Cooling"]*12+["Total S1"]*12,
        "Cum":    list(np.cumsum(fuel_mo+bus_mo)) + list(np.cumsum(hvac_heat_tco2e_mo)) +
                  list(np.cumsum(hvac_cool_tco2e_mo)) + list(np.cumsum(fuel_mo+bus_mo+hvac_heat_tco2e_mo+hvac_cool_tco2e_mo)),
    })
    cum_s1_df["Month"] = pd.Categorical(cum_s1_df["Month"],categories=MONTHS,ordered=True)
    cs1_sc = alt.Scale(domain=["Mobile","HVAC Heating","HVAC Cooling","Total S1"],range=[C_S1,C_HEAT,C_COOL,C_ROLL])
    st.altair_chart((alt.Chart(cum_s1_df).mark_line(strokeWidth=2.2,interpolate=interp).encode(
        x=mx(), y=alt.Y("Cum:Q",title="Cumulative tCO₂e"),
        color=alt.Color("Series:N",scale=cs1_sc,legend=alt.Legend(orient="top",title=None)),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("Series:N"),alt.Tooltip("Cum:Q",format=".4f",title="Cumul. tCO₂e")],
    )+alt.Chart(cum_s1_df).mark_point(filled=True,size=50).encode(
        x=mx(), y=alt.Y("Cum:Q"), color=alt.Color("Series:N",scale=cs1_sc),
    )).properties(**hp(260)),use_container_width=True)

    # ── Vehicle and Bus ───────────────────────────────────────────────────────
    va, vb = st.columns(2)
    with va:
        st.markdown('<div class="sec-label">Vehicle fuel</div>', unsafe_allow_html=True)
        fuel_df2 = pd.DataFrame({"Vehicle":["Diesel fleet","Peugeot Bipper Feb","Peugeot Bipper Dec"],
                                  "Liters":[1741.5,1520.8,1520.8],"tCO2e":list(vehicle_raw["tCO2e"]),
                                  "Fuel":["Diesel","Super Gasoline","Super Gasoline"]})
        fb = alt.Chart(fuel_df2).mark_bar(cornerRadiusTopLeft=4,cornerRadiusTopRight=4).encode(
            x=alt.X("Vehicle:N",title=None,axis=alt.Axis(labelAngle=-15,labelLimit=190)),
            y=alt.Y("tCO2e:Q",title="tCO₂e"),
            color=alt.Color("Fuel:N",scale=alt.Scale(domain=["Diesel","Super Gasoline"],range=[C_S1,"#54A0FF"]),
                            legend=alt.Legend(orient="top")),
            tooltip=[alt.Tooltip("Vehicle:N"),alt.Tooltip("Liters:Q",format=",.1f"),
                     alt.Tooltip("tCO2e:Q",format=".4f",title="tCO₂e")],
        )
        st.altair_chart((fb+fb.mark_text(dy=-8,fontSize=10,color=TEXT_M,font="DM Mono, monospace").encode(
            text=alt.Text("tCO2e:Q",format=".3f"))).properties(**hp(220)),use_container_width=True)
    with vb:
        st.markdown('<div class="sec-label">Bus & van trip distances</div>', unsafe_allow_html=True)
        bus_bar2 = alt.Chart(bus_raw).mark_bar(color=C_S2,cornerRadiusTopRight=5,cornerRadiusBottomRight=5).encode(
            x=alt.X("Distance_km:Q",title="km"), y=alt.Y("Destination:N",sort="-x",title=None),
            tooltip=[alt.Tooltip("Destination:N"),alt.Tooltip("Distance_km:Q",title="km"),
                     alt.Tooltip("tCO2e:Q",format=".6f",title="tCO₂e"),alt.Tooltip("Source:N")],
        )
        st.altair_chart((bus_bar2+bus_bar2.mark_text(align="left",dx=5,fontSize=10,
            color=TEXT_M,font="DM Mono, monospace").encode(text=alt.Text("Distance_km:Q",format=".1f"))
            ).properties(**hp(180)),use_container_width=True)

    ct1,ct2,ct3 = st.columns(3)
    with ct1:
        st.markdown("**Fuel vouchers**")
        dv = vehicle_raw[["Date","Source","Fuel_type","Liters","tCO2e"]].copy()
        dv.columns = ["Date","Source","Fuel","Liters","tCO₂e"]
        dv["Liters"] = dv["Liters"].map("{:,.1f}".format)
        dv["tCO₂e"]  = dv["tCO₂e"].map("{:.5f}".format)
        st.dataframe(dv,use_container_width=True,hide_index=True)
    with ct2:
        st.markdown("**Bus / van trips**")
        db = bus_raw[["Date","Destination","Source","Distance_km","tCO2e"]].copy()
        db.columns = ["Date","Destination","Vehicle","km","tCO₂e"]
        db["tCO₂e"] = db["tCO₂e"].map("{:.6f}".format)
        st.dataframe(db,use_container_width=True,hide_index=True)
    with ct3:
        st.markdown("**HVAC monthly**")
        dh = hvac_df[["Month","Heating_kWh","Heating_kgCO2e","Cooling_kWh","Cooling_kgCO2e"]].copy()
        dh.columns = ["Month","Heat kWh","Heat kgCO₂e","Cool kWh","Cool kgCO₂e"]
        for col in ["Heat kWh","Cool kWh"]:
            dh[col] = dh[col].map(lambda x: f"{x:,.1f}" if x>0 else "—")
        for col in ["Heat kgCO₂e","Cool kgCO₂e"]:
            dh[col] = dh[col].map(lambda x: f"{x:,.2f}" if x>0 else "—")
        st.dataframe(dh,use_container_width=True,hide_index=True)
    st.caption(f"R410A · EF = {ef_refrigerant:,.0f} kgCO₂e/kg · Heating: {hvac_heat_kg:.0f} kg → {HVAC_HEAT_KGCO2E:,.0f} kgCO₂e = {total_s1heat:.2f} tCO₂e · Cooling: {hvac_cool_kg:.0f} kg → {HVAC_COOL_KGCO2E:,.0f} kgCO₂e = {total_s1cool:.2f} tCO₂e · {HVAC_HOURS:,} avg hrs/month")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — SCOPE 2
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<span class="badge-s2">Scope 2</span>&nbsp; Purchased Electricity — location-based', unsafe_allow_html=True)
    st.markdown(" ")

    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Total Scope 2",     f"{total_s2:.3f}","tCO₂e")
    m2.metric("Total consumption", f"{total_kwh/1000:.1f}","MWh")
    m3.metric("Monthly average",   f"{int(total_kwh/12):,}","kWh")
    m4.metric("Peak month",        "July · 48,569","kWh")
    m5.metric("Grid factor",       f"{ef_grid:.3f}","kgCO₂e / kWh")

    st.markdown('<div class="sec-label">Monthly kWh vs tCO₂e</div>', unsafe_allow_html=True)
    elec_plot = elec_df.copy()
    elec_plot["Month"] = pd.Categorical(elec_plot["Month"],categories=MONTHS,ordered=True)
    bar_kwh = alt.Chart(elec_plot).mark_bar(color=C_S2,opacity=0.32,
        cornerRadiusTopLeft=4,cornerRadiusTopRight=4,width={"band":.7}).encode(
        x=mx(), y=alt.Y("kWh:Q",title="kWh",axis=alt.Axis(titleColor=C_S2)),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("kWh:Q",format=",.0f",title="kWh"),
                 alt.Tooltip("tCO2e:Q",format=".3f",title="tCO₂e")],
    )
    line_co2 = alt.Chart(elec_plot).mark_line(color=C_S2,strokeWidth=2.8,interpolate=interp).encode(
        x=mx(), y=alt.Y("tCO2e:Q",title="tCO₂e",axis=alt.Axis(titleColor=C_S2)),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("tCO2e:Q",format=".3f",title="tCO₂e")],
    )
    pts_co2 = alt.Chart(elec_plot).mark_point(color=C_S2,filled=True,size=65).encode(
        x=mx(), y=alt.Y("tCO2e:Q"),
    )
    st.altair_chart(alt.layer(bar_kwh,hline(elec_kwh.mean(),C_TGT),line_co2+pts_co2
                              ).resolve_scale(y="independent").properties(**hp(310)),use_container_width=True)
    st.caption(f"Dashed line = annual avg {elec_kwh.mean():,.0f} kWh")

    st.markdown('<div class="sec-label">Scope 2 — area + trend overlays</div>', unsafe_allow_html=True)
    s2_chart = area_fill(trend_df,"Scope2",C_S2,0.14)+smooth_line(trend_df,"Scope2",C_S2,2.5)+glow_point(trend_df,"Scope2",C_S2,58)
    if show_rolling: s2_chart = s2_chart + smooth_line(trend_df,"Roll_S2",C_ROLL,1.8,[4,2],.75,"Rolling avg")
    if show_proj:    s2_chart = s2_chart + smooth_line(trend_df,"Proj_S2",C_PROJ,1.4,[5,3],.68,"Projection")
    if show_target:  s2_chart = s2_chart + hline(target_monthly[0]*total_s2/total_all,C_TGT)
    st.altair_chart(s2_chart.properties(**hp(290)),use_container_width=True)

    st.markdown('<div class="sec-label">kWh deviation from annual average</div>', unsafe_allow_html=True)
    trend_df["kWh_Dev"] = trend_df["kWh"] - elec_kwh.mean()
    trend_df["Dev_Dir"] = np.where(trend_df["kWh_Dev"]>=0,"Above avg","Below avg")
    dev_bar = alt.Chart(trend_df).mark_bar(cornerRadiusTopLeft=3,cornerRadiusTopRight=3,
        cornerRadiusBottomLeft=3,cornerRadiusBottomRight=3,width={"band":.65}).encode(
        x=mx(), y=alt.Y("kWh_Dev:Q",title="kWh Δ from avg",axis=alt.Axis(format=",.0f")),
        color=alt.Color("Dev_Dir:N",scale=alt.Scale(domain=["Above avg","Below avg"],range=[C_TGT,C_S2]),
                        legend=alt.Legend(orient="top",title=None)),
        tooltip=[alt.Tooltip("Month:N"),alt.Tooltip("kWh:Q",format=",.0f",title="kWh"),
                 alt.Tooltip("kWh_Dev:Q",format=",.0f",title="Δ from avg")],
    )
    st.altair_chart((dev_bar+hline(0,GRID_C,[3,2])+smooth_line(trend_df,"kWh_Dev",C_ROLL,1.5,[3,2],.55,"Trend")
                     ).properties(**hp(240)),use_container_width=True)

    de = elec_df[["Month","kWh","MWh","tCO2e","Meters"]].copy()
    de.columns = ["Month","kWh","MWh","tCO₂e","Meters"]
    de["kWh"]   = de["kWh"].map("{:,.0f}".format)
    de["MWh"]   = de["MWh"].map("{:.3f}".format)
    de["tCO₂e"] = de["tCO₂e"].map("{:.4f}".format)
    st.dataframe(de,use_container_width=True,hide_index=True)
    st.caption(f"Grid EF: {ef_grid:.4f} kgCO₂e/kWh (Tunisia STEG) · All values update live with sidebar sliders")
