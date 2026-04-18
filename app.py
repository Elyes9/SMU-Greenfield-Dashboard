import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Carbon Accounting Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container { padding-top: 1.4rem; padding-bottom: 1rem; }
    [data-testid="stMetric"] {
        background: white;
        border: 0.5px solid #e2e8e4;
        border-radius: 10px;
        padding: 13px 16px;
    }
    .badge-s1 {
        background:#E6F1FB; color:#0C447C;
        padding:3px 10px; border-radius:6px;
        font-size:12px; font-weight:600; display:inline-block;
    }
    .badge-s2 {
        background:#E1F5EE; color:#085041;
        padding:3px 10px; border-radius:6px;
        font-size:12px; font-weight:600; display:inline-block;
    }
    .insight-box {
        background:#f7faf8;
        border-left:3px solid #1D9E75;
        border-radius:6px;
        padding:10px 14px;
        font-size:13px;
        margin-bottom:8px;
        line-height:1.6;
    }
    .section-label {
        font-size:11px; font-weight:600; letter-spacing:.06em;
        text-transform:uppercase; color:#888; margin-bottom:6px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS & MONTHS
# ─────────────────────────────────────────────────────────────────────────────
MONTHS     = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTH_NUMS = list(range(1, 13))
COLOR_S1   = "#378ADD"
COLOR_S2   = "#1D9E75"
COLOR_TOT  = "#D4537E"
COLOR_CUM  = "#9B59B6"
COLOR_INT  = "#E67E22"
COLOR_AVG  = "#E74C3C"

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Emission factors")
    ef_diesel   = st.number_input("Diesel (kgCO₂e / L)",   value=2.68,  step=0.01,  format="%.3f")
    ef_gasoline = st.number_input("Gasoline (kgCO₂e / L)", value=2.31,  step=0.01,  format="%.3f")
    ef_bus_km   = st.number_input("Bus/Van (kgCO₂e / km)", value=0.089, step=0.001, format="%.4f")
    ef_grid     = st.number_input("Grid (kgCO₂e / kWh)",   value=0.267, step=0.001, format="%.4f")

    st.divider()
    st.markdown("### 🎛️ Chart options")
    show_rolling  = st.checkbox("Show 3-month rolling average",  value=True)
    show_cum      = st.checkbox("Show cumulative curve",          value=True)
    show_target   = st.checkbox("Show reduction target (−10%)",   value=True)
    show_proj     = st.checkbox("Show linear projection",         value=True)

    st.divider()
    st.markdown("**Framework:** GHG Protocol Corporate Standard")
    st.markdown("**Reporting year:** 2025")
    st.markdown("**Grid:** Tunisia (STEG)")
    st.markdown('<span class="badge-s1">Scope 1</span> Mobile combustion',     unsafe_allow_html=True)
    st.markdown("")
    st.markdown('<span class="badge-s2">Scope 2</span> Purchased electricity', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# RAW DATA
# ─────────────────────────────────────────────────────────────────────────────
elec_kwh = np.array([28429,30287,30262,19625,22097,37937,
                     48569,43843,38143,28139,23532,23039])

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

elec_df = pd.DataFrame({
    "Month":     MONTHS,
    "Month_num": MONTH_NUMS,
    "kWh":       elec_kwh,
    "Meters":    np.full(12, 15),
})
elec_df["MWh"]   = elec_df["kWh"] / 1000
elec_df["tCO2e"] = elec_df["kWh"] * ef_grid / 1000

# ─────────────────────────────────────────────────────────────────────────────
# AGGREGATES & DERIVED SERIES
# ─────────────────────────────────────────────────────────────────────────────
total_s2  = elec_df["tCO2e"].sum()
total_s1v = vehicle_raw["tCO2e"].sum()
total_s1b = bus_raw["tCO2e"].sum()
total_s1  = total_s1v + total_s1b
total_all = total_s1 + total_s2
total_kwh = int(elec_kwh.sum())

# Monthly Scope 1
s1_monthly = np.zeros(12)
for _, row in vehicle_raw.iterrows():
    s1_monthly[int(row["Month_num"])-1] += row["tCO2e"]
for _, row in bus_raw.iterrows():
    s1_monthly[int(row["Month_num"])-1] += row["tCO2e"]

s2_monthly = elec_df["tCO2e"].values
total_monthly = s1_monthly + s2_monthly

# Rolling 3-month averages
def rolling3(arr):
    result = []
    for i in range(len(arr)):
        window = arr[max(0, i-1):i+2]
        result.append(window.mean())
    return np.array(result)

roll_s1  = rolling3(s1_monthly)
roll_s2  = rolling3(s2_monthly)
roll_tot = rolling3(total_monthly)

# Cumulative
cum_s1    = np.cumsum(s1_monthly)
cum_s2    = np.cumsum(s2_monthly)
cum_total = np.cumsum(total_monthly)

# Intensity (kgCO2e per kWh consumed — proxy for Scope 2 intensity)
intensity = (s2_monthly * 1000) / elec_kwh  # = ef_grid, constant unless EF changes

# Linear projection from existing trend (Scope 2, which has full 12 months)
x_fit = np.arange(12)
slope, intercept = np.polyfit(x_fit, s2_monthly, 1)
proj_s2 = slope * x_fit + intercept

# Target line: 10% below annual average
target_monthly = np.full(12, (total_monthly.mean()) * 0.90)

# Month-over-month change %
mom_change = np.concatenate([[0], np.diff(total_monthly) / total_monthly[:-1] * 100])

# Build master monthly DataFrame
trend_df = pd.DataFrame({
    "Month":      MONTHS,
    "Month_num":  MONTH_NUMS,
    "Scope1":     s1_monthly,
    "Scope2":     s2_monthly,
    "Total":      total_monthly,
    "Roll_S1":    roll_s1,
    "Roll_S2":    roll_s2,
    "Roll_Total": roll_tot,
    "Cum_S1":     cum_s1,
    "Cum_S2":     cum_s2,
    "Cum_Total":  cum_total,
    "Intensity":  intensity,
    "Proj_S2":    proj_s2,
    "Target":     target_monthly,
    "MoM_Change": mom_change,
    "kWh":        elec_kwh.astype(float),
})
trend_df["Month"] = pd.Categorical(trend_df["Month"], categories=MONTHS, ordered=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER — Altair base
# ─────────────────────────────────────────────────────────────────────────────
def base_chart(df, h=280):
    return alt.Chart(df).properties(height=h)

def month_axis():
    return alt.X("Month:N", sort=MONTHS, title=None, axis=alt.Axis(labelAngle=0))

# ─────────────────────────────────────────────────────────────────────────────
# HEADER + KPIs
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("## 🌿 Carbon Accounting Dashboard — 2025")
st.caption("GHG Protocol · Scope 1 (Mobile Combustion) · Scope 2 (Purchased Electricity) · Tunisia")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🌍 Grand total",        f"{total_all:.2f} tCO₂e",   "Scope 1 + 2")
k2.metric("🚗 Scope 1",           f"{total_s1:.4f} tCO₂e",    "Mobile combustion")
k3.metric("⚡ Scope 2",            f"{total_s2:.2f} tCO₂e",    "Electricity")
k4.metric("💡 Total electricity",  f"{total_kwh/1000:.1f} MWh","15 meters · 12 mo.")
k5.metric("📉 Avg intensity",      f"{intensity.mean():.3f}",   "kgCO₂e / kWh")
st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "📈 Trend & Curves",
    "🔄 Cumulative",
    "🚗 Scope 1 Detail",
    "⚡ Scope 2 Detail",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    c_left, c_right = st.columns(2)

    # Arc chart
    with c_left:
        st.markdown('<p class="section-label">Emissions split by scope</p>', unsafe_allow_html=True)
        donut_df = pd.DataFrame({
            "Scope": ["Scope 1 — Mobile Combustion","Scope 2 — Electricity"],
            "tCO2e": [round(total_s1,4), round(total_s2,4)],
            "Pct":   [round(total_s1/total_all*100,1), round(total_s2/total_all*100,1)],
        })
        arc = alt.Chart(donut_df).mark_arc(innerRadius=72, outerRadius=130).encode(
            theta=alt.Theta("tCO2e:Q"),
            color=alt.Color("Scope:N",
                scale=alt.Scale(domain=donut_df["Scope"].tolist(),
                                range=[COLOR_S1, COLOR_S2]),
                legend=alt.Legend(orient="bottom", labelLimit=400)),
            tooltip=[alt.Tooltip("Scope:N"),
                     alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e"),
                     alt.Tooltip("Pct:Q",   format=".1f",  title="%")],
        ).properties(height=290)
        st.altair_chart(arc, use_container_width=True)

    # Horizontal stacked overview bar by month
    with c_right:
        st.markdown('<p class="section-label">Monthly scope breakdown</p>', unsafe_allow_html=True)
        ov_long = trend_df[["Month","Scope1","Scope2"]].melt(
            id_vars="Month", value_vars=["Scope1","Scope2"],
            var_name="Scope", value_name="tCO2e"
        )
        ov_long["Scope"] = ov_long["Scope"].map({"Scope1":"Scope 1","Scope2":"Scope 2"})
        ov_bar = alt.Chart(ov_long).mark_bar(
            cornerRadiusTopLeft=3, cornerRadiusTopRight=3
        ).encode(
            x=month_axis(),
            y=alt.Y("tCO2e:Q", stack="zero", title="tCO₂e"),
            color=alt.Color("Scope:N",
                scale=alt.Scale(domain=["Scope 1","Scope 2"],
                                range=[COLOR_S1, COLOR_S2]),
                legend=alt.Legend(orient="top", title=None)),
            tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Scope:N"),
                     alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e")],
        ).properties(height=290)
        st.altair_chart(ov_bar, use_container_width=True)

    # Scope 1 source bar
    st.markdown('<p class="section-label">Scope 1 — source breakdown</p>', unsafe_allow_html=True)
    src_df = pd.DataFrame({
        "Source":   ["Diesel (fleet)","Gasoline (Feb)","Gasoline (Dec)","Bus/Van trips"],
        "tCO2e":    [
            vehicle_raw.loc[vehicle_raw["Fuel_type"]=="Diesel","tCO2e"].sum(),
            vehicle_raw.iloc[1]["tCO2e"],
            vehicle_raw.iloc[2]["tCO2e"],
            bus_raw["tCO2e"].sum(),
        ],
        "Category": ["Vehicle fuel","Vehicle fuel","Vehicle fuel","Distance-based"],
    })
    src_bar = alt.Chart(src_df).mark_bar(
        cornerRadiusTopRight=4, cornerRadiusBottomRight=4
    ).encode(
        x=alt.X("tCO2e:Q", title="tCO₂e"),
        y=alt.Y("Source:N", sort="-x", title=None),
        color=alt.Color("Category:N",
            scale=alt.Scale(domain=["Vehicle fuel","Distance-based"],
                            range=[COLOR_S1,"#5DCAA5"]),
            legend=alt.Legend(orient="right")),
        tooltip=[alt.Tooltip("Source:N"), alt.Tooltip("tCO2e:Q", format=".5f", title="tCO₂e")],
    ).properties(height=160)
    src_txt = src_bar.mark_text(align="left", dx=5, fontSize=11).encode(
        text=alt.Text("tCO2e:Q", format=".4f")
    )
    st.altair_chart(src_bar + src_txt, use_container_width=True)

    # Insights row
    ia, ib, ic = st.columns(3)
    with ia:
        st.markdown(f"""<div class="insight-box">
            <b>🚗 Diesel fleet dominant</b><br>
            {vehicle_raw.iloc[0]['tCO2e']:.3f} tCO₂e from 1,741 L diesel in February —
            the single largest Scope 1 event.
        </div>""", unsafe_allow_html=True)
    with ib:
        st.markdown(f"""<div class="insight-box">
            <b>⚡ July peak load</b><br>
            48,569 kWh → {elec_df.iloc[6]['tCO2e']:.2f} tCO₂e.
            Summer cooling drives a <b>{(elec_kwh[6]/elec_kwh.mean()-1)*100:.0f}%</b>
            spike above annual average.
        </div>""", unsafe_allow_html=True)
    with ic:
        st.markdown(f"""<div class="insight-box">
            <b>📊 Scope 2 dominates</b><br>
            Electricity = <b>{total_s2/total_all*100:.1f}%</b> of total GHG.
            Renewable procurement or efficiency measures would have the highest impact.
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TREND & CURVES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:

    # ── Chart 1: Multi-line total + scope lines + optional rolling + target ──
    st.markdown('<p class="section-label">Monthly emissions — all series</p>', unsafe_allow_html=True)

    color_scale_main = alt.Scale(
        domain=["Scope 1","Scope 2","Total"],
        range=[COLOR_S1, COLOR_S2, COLOR_TOT]
    )
    dash_scale_main = alt.Scale(
        domain=["Scope 1","Scope 2","Total"],
        range=[[1,0],[1,0],[6,3]]
    )

    long_main = trend_df[["Month","Scope1","Scope2","Total"]].melt(
        id_vars="Month", value_vars=["Scope1","Scope2","Total"],
        var_name="Series", value_name="tCO2e"
    )
    long_main["Series"] = long_main["Series"].map(
        {"Scope1":"Scope 1","Scope2":"Scope 2","Total":"Total"}
    )

    lines_main = alt.Chart(long_main).mark_line(strokeWidth=2).encode(
        x=month_axis(),
        y=alt.Y("tCO2e:Q", title="tCO₂e"),
        color=alt.Color("Series:N", scale=color_scale_main,
                        legend=alt.Legend(orient="top", title=None)),
        strokeDash=alt.StrokeDash("Series:N", scale=dash_scale_main),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Series:N"),
                 alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e")],
    )
    pts_main = alt.Chart(long_main).mark_point(filled=True, size=55).encode(
        x=month_axis(),
        y=alt.Y("tCO2e:Q"),
        color=alt.Color("Series:N", scale=color_scale_main),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Series:N"),
                 alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e")],
    )
    chart_main = lines_main + pts_main

    if show_rolling:
        long_roll = trend_df[["Month","Roll_S1","Roll_S2","Roll_Total"]].melt(
            id_vars="Month", value_vars=["Roll_S1","Roll_S2","Roll_Total"],
            var_name="Series", value_name="tCO2e"
        )
        long_roll["Series"] = long_roll["Series"].map(
            {"Roll_S1":"Rolling avg S1","Roll_S2":"Rolling avg S2","Roll_Total":"Rolling avg Total"}
        )
        roll_lines = alt.Chart(long_roll).mark_line(
            strokeDash=[4,3], strokeWidth=1.5, opacity=0.7
        ).encode(
            x=month_axis(),
            y=alt.Y("tCO2e:Q"),
            color=alt.Color("Series:N",
                scale=alt.Scale(
                    domain=["Rolling avg S1","Rolling avg S2","Rolling avg Total"],
                    range=[COLOR_S1, COLOR_S2, COLOR_TOT]
                ),
                legend=alt.Legend(orient="top", title="3-mo rolling")),
            tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Series:N"),
                     alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e")],
        )
        chart_main = chart_main + roll_lines

    if show_target:
        target_rule = alt.Chart(trend_df).mark_line(
            color=COLOR_AVG, strokeDash=[2,2], strokeWidth=1.5
        ).encode(
            x=month_axis(),
            y=alt.Y("Target:Q"),
            tooltip=[alt.Tooltip("Target:Q", format=".3f", title="Target (−10%)")],
        )
        target_label = alt.Chart(pd.DataFrame({
            "Month":["Dec"], "Target":[target_monthly[-1]],
            "label":["Target (−10%)"]
        })).mark_text(align="right", dx=-4, dy=-8, fontSize=10, color=COLOR_AVG).encode(
            x=alt.X("Month:N", sort=MONTHS),
            y=alt.Y("Target:Q"),
            text="label:N"
        )
        chart_main = chart_main + target_rule + target_label

    if show_proj:
        proj_line = alt.Chart(trend_df).mark_line(
            color=COLOR_INT, strokeDash=[3,2], strokeWidth=1.5, opacity=0.8
        ).encode(
            x=month_axis(),
            y=alt.Y("Proj_S2:Q"),
            tooltip=[alt.Tooltip("Month:N"),
                     alt.Tooltip("Proj_S2:Q", format=".3f", title="Linear projection S2")],
        )
        chart_main = chart_main + proj_line

    st.altair_chart(chart_main.properties(height=340), use_container_width=True)

    # ── Chart 2: Area chart — stacked Scope 1 + Scope 2 ──────────────────────
    st.markdown('<p class="section-label">Stacked area — scope contributions</p>', unsafe_allow_html=True)

    area_long = trend_df[["Month","Scope1","Scope2"]].melt(
        id_vars="Month", value_vars=["Scope1","Scope2"],
        var_name="Scope", value_name="tCO2e"
    )
    area_long["Scope"] = area_long["Scope"].map({"Scope1":"Scope 1","Scope2":"Scope 2"})

    area = alt.Chart(area_long).mark_area(opacity=0.75).encode(
        x=month_axis(),
        y=alt.Y("tCO2e:Q", stack="zero", title="tCO₂e"),
        color=alt.Color("Scope:N",
            scale=alt.Scale(domain=["Scope 1","Scope 2"],
                            range=[COLOR_S1, COLOR_S2]),
            legend=alt.Legend(orient="top", title=None)),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Scope:N"),
                 alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e")],
    )
    area_line = alt.Chart(trend_df).mark_line(
        color=COLOR_TOT, strokeWidth=2, point=True
    ).encode(
        x=month_axis(),
        y=alt.Y("Total:Q"),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("Total:Q", format=".4f", title="Total tCO₂e")],
    )
    st.altair_chart((area + area_line).properties(height=280), use_container_width=True)

    # ── Chart 3: Month-over-month % change ───────────────────────────────────
    st.markdown('<p class="section-label">Month-over-month change in total emissions (%)</p>', unsafe_allow_html=True)

    trend_df["MoM_Color"] = np.where(trend_df["MoM_Change"] >= 0, "Increase", "Decrease")
    mom_bar = alt.Chart(trend_df[trend_df["Month_num"] > 1]).mark_bar(
        cornerRadiusTopLeft=3, cornerRadiusTopRight=3,
        cornerRadiusBottomLeft=3, cornerRadiusBottomRight=3
    ).encode(
        x=month_axis(),
        y=alt.Y("MoM_Change:Q", title="% change vs prior month",
                axis=alt.Axis(format=".1f")),
        color=alt.Color("MoM_Color:N",
            scale=alt.Scale(domain=["Increase","Decrease"],
                            range=["#E24B4A","#1D9E75"]),
            legend=alt.Legend(orient="top", title=None)),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("MoM_Change:Q", format=".1f", title="MoM change %")],
    )
    zero_rule = alt.Chart(pd.DataFrame({"y":[0]})).mark_rule(
        color="#999", strokeWidth=0.8
    ).encode(y="y:Q")
    st.altair_chart((mom_bar + zero_rule).properties(height=220), use_container_width=True)

    # ── Chart 4: Scope 2 emissions vs electricity consumption scatter ─────────
    st.markdown('<p class="section-label">Electricity consumption vs Scope 2 emissions (scatter)</p>', unsafe_allow_html=True)

    scatter = alt.Chart(trend_df).mark_circle(size=80, opacity=0.85).encode(
        x=alt.X("kWh:Q", title="Monthly electricity (kWh)"),
        y=alt.Y("Scope2:Q", title="tCO₂e (Scope 2)"),
        color=alt.Color("Month:N",
            scale=alt.Scale(scheme="viridis"),
            legend=alt.Legend(orient="right", title="Month")),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("kWh:Q", format=",.0f", title="kWh"),
                 alt.Tooltip("Scope2:Q", format=".3f", title="tCO₂e")],
    )
    reg_line = scatter.transform_regression(
        "kWh","Scope2", method="linear"
    ).mark_line(color=COLOR_AVG, strokeDash=[4,2], strokeWidth=1.5)
    st.altair_chart((scatter + reg_line).properties(height=260), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CUMULATIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-label">Cumulative CO₂e — year-to-date build-up</p>', unsafe_allow_html=True)

    # ── Chart 1: Cumulative line chart ───────────────────────────────────────
    cum_long = trend_df[["Month","Cum_S1","Cum_S2","Cum_Total"]].melt(
        id_vars="Month", value_vars=["Cum_S1","Cum_S2","Cum_Total"],
        var_name="Series", value_name="tCO2e"
    )
    cum_long["Series"] = cum_long["Series"].map(
        {"Cum_S1":"Scope 1 cumul.","Cum_S2":"Scope 2 cumul.","Cum_Total":"Total cumul."}
    )

    cum_color = alt.Scale(
        domain=["Scope 1 cumul.","Scope 2 cumul.","Total cumul."],
        range=[COLOR_S1, COLOR_S2, COLOR_CUM]
    )
    cum_line = alt.Chart(cum_long).mark_line(strokeWidth=2.5).encode(
        x=month_axis(),
        y=alt.Y("tCO2e:Q", title="Cumulative tCO₂e"),
        color=alt.Color("Series:N", scale=cum_color,
                        legend=alt.Legend(orient="top", title=None)),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Series:N"),
                 alt.Tooltip("tCO2e:Q", format=".3f", title="Cumul. tCO₂e")],
    )
    cum_pts = alt.Chart(cum_long).mark_point(filled=True, size=60).encode(
        x=month_axis(),
        y=alt.Y("tCO2e:Q"),
        color=alt.Color("Series:N", scale=cum_color),
    )

    # Annotate year-end values
    year_end = cum_long[cum_long["Month"]=="Dec"].copy()
    cum_annot = alt.Chart(year_end).mark_text(
        align="right", dx=-6, dy=-10, fontSize=11, fontWeight="normal"
    ).encode(
        x=month_axis(),
        y=alt.Y("tCO2e:Q"),
        color=alt.Color("Series:N", scale=cum_color, legend=None),
        text=alt.Text("tCO2e:Q", format=".2f"),
    )
    st.altair_chart((cum_line + cum_pts + cum_annot).properties(height=320), use_container_width=True)

    # ── Chart 2: Cumulative area ─────────────────────────────────────────────
    st.markdown('<p class="section-label">Cumulative area — Scope 1 vs Scope 2 build-up</p>', unsafe_allow_html=True)

    cum_area_long = trend_df[["Month","Cum_S1","Cum_S2"]].melt(
        id_vars="Month", value_vars=["Cum_S1","Cum_S2"],
        var_name="Scope", value_name="tCO2e"
    )
    cum_area_long["Scope"] = cum_area_long["Scope"].map(
        {"Cum_S1":"Scope 1","Cum_S2":"Scope 2"}
    )
    cum_area = alt.Chart(cum_area_long).mark_area(opacity=0.7).encode(
        x=month_axis(),
        y=alt.Y("tCO2e:Q", stack=None, title="Cumulative tCO₂e"),
        color=alt.Color("Scope:N",
            scale=alt.Scale(domain=["Scope 1","Scope 2"], range=[COLOR_S1, COLOR_S2]),
            legend=alt.Legend(orient="top", title=None)),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Scope:N"),
                 alt.Tooltip("tCO2e:Q", format=".3f", title="Cumul. tCO₂e")],
    )
    st.altair_chart(cum_area.properties(height=260), use_container_width=True)

    # ── Chart 3: % of annual total reached each month ────────────────────────
    st.markdown('<p class="section-label">Year-to-date progress — % of annual total reached</p>', unsafe_allow_html=True)

    trend_df["Pct_of_Annual"] = trend_df["Cum_Total"] / total_all * 100
    pct_area = alt.Chart(trend_df).mark_area(
        color=COLOR_CUM, opacity=0.25, line={"color": COLOR_CUM, "strokeWidth":2}
    ).encode(
        x=month_axis(),
        y=alt.Y("Pct_of_Annual:Q", title="% of annual total",
                scale=alt.Scale(domain=[0, 100])),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("Pct_of_Annual:Q", format=".1f", title="% of annual")],
    )
    half_rule = alt.Chart(pd.DataFrame({"y":[50]})).mark_rule(
        color="#999", strokeDash=[3,2], strokeWidth=1
    ).encode(y="y:Q")
    pct_pts = alt.Chart(trend_df).mark_point(
        color=COLOR_CUM, filled=True, size=55
    ).encode(
        x=month_axis(),
        y=alt.Y("Pct_of_Annual:Q"),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("Pct_of_Annual:Q", format=".1f", title="% of annual")],
    )
    st.altair_chart((pct_area + half_rule + pct_pts).properties(height=240),
                    use_container_width=True)

    # ── Summary table ─────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Cumulative data table</p>', unsafe_allow_html=True)
    cum_table = trend_df[["Month","Scope1","Scope2","Total","Cum_S1","Cum_S2","Cum_Total","Pct_of_Annual"]].copy()
    cum_table.columns = ["Month","S1 (t)","S2 (t)","Total (t)",
                         "Cum S1","Cum S2","Cum Total","% of annual"]
    for col in ["S1 (t)","S2 (t)","Total (t)","Cum S1","Cum S2","Cum Total"]:
        cum_table[col] = cum_table[col].map("{:.4f}".format)
    cum_table["% of annual"] = cum_table["% of annual"].map("{:.1f}%".format)
    st.dataframe(cum_table, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — SCOPE 1 DETAIL
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<span class="badge-s1">Scope 1</span>&nbsp; Mobile Combustion', unsafe_allow_html=True)
    st.markdown(" ")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Scope 1",      f"{total_s1:.5f} tCO₂e")
    m2.metric("From fuel vouchers", f"{total_s1v:.4f} tCO₂e", "3 transactions")
    m3.metric("From bus/van trips", f"{total_s1b:.5f} tCO₂e", "5 trips")
    m4.metric("Total distance",     "124.5 km", "bus routes")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p class="section-label">Fuel consumption by vehicle type</p>', unsafe_allow_html=True)
        fuel_df = pd.DataFrame({
            "Vehicle":  ["Diesel fleet","Peugeot Bipper (Feb)","Peugeot Bipper (Dec)"],
            "Liters":   [1741.5, 1520.8, 1520.8],
            "tCO2e":    [vehicle_raw.iloc[0]["tCO2e"],
                         vehicle_raw.iloc[1]["tCO2e"],
                         vehicle_raw.iloc[2]["tCO2e"]],
            "Fuel":     ["Diesel","Super Gasoline","Super Gasoline"],
        })
        fuel_bar = alt.Chart(fuel_df).mark_bar(
            cornerRadiusTopLeft=3, cornerRadiusTopRight=3
        ).encode(
            x=alt.X("Vehicle:N", title=None, axis=alt.Axis(labelAngle=-20, labelLimit=150)),
            y=alt.Y("tCO2e:Q", title="tCO₂e"),
            color=alt.Color("Fuel:N",
                scale=alt.Scale(domain=["Diesel","Super Gasoline"],
                                range=["#378ADD","#85B7EB"]),
                legend=alt.Legend(orient="top")),
            tooltip=[alt.Tooltip("Vehicle:N"), alt.Tooltip("Liters:Q", format=",.1f"),
                     alt.Tooltip("tCO2e:Q", format=".5f", title="tCO₂e")],
        )
        fuel_txt = fuel_bar.mark_text(dy=-8, fontSize=11).encode(
            text=alt.Text("tCO2e:Q", format=".3f")
        )
        st.altair_chart((fuel_bar+fuel_txt).properties(height=240), use_container_width=True)

    with col_b:
        st.markdown('<p class="section-label">Bus trip distances and emissions</p>', unsafe_allow_html=True)
        bus_bar = alt.Chart(bus_raw).mark_bar(
            color="#5DCAA5", cornerRadiusTopRight=3, cornerRadiusBottomRight=3
        ).encode(
            x=alt.X("Distance_km:Q", title="km"),
            y=alt.Y("Destination:N", sort="-x", title=None),
            tooltip=[alt.Tooltip("Destination:N"),
                     alt.Tooltip("Distance_km:Q", title="km"),
                     alt.Tooltip("tCO2e:Q", format=".6f", title="tCO₂e"),
                     alt.Tooltip("Source:N")],
        )
        bus_txt = bus_bar.mark_text(align="left", dx=4, fontSize=10).encode(
            text=alt.Text("Distance_km:Q", format=".1f")
        )
        st.altair_chart((bus_bar+bus_txt).properties(height=240), use_container_width=True)

    # Monthly S1 profile
    st.markdown('<p class="section-label">Monthly Scope 1 profile — stacked by type</p>', unsafe_allow_html=True)
    fuel_monthly_arr = np.zeros(12)
    bus_monthly_arr  = np.zeros(12)
    for _, row in vehicle_raw.iterrows():
        fuel_monthly_arr[int(row["Month_num"])-1] += row["tCO2e"]
    for _, row in bus_raw.iterrows():
        bus_monthly_arr[int(row["Month_num"])-1] += row["tCO2e"]

    s1_long = pd.DataFrame({
        "Month":  MONTHS*2,
        "Type":   ["Fuel vouchers"]*12 + ["Bus/Van trips"]*12,
        "tCO2e":  list(fuel_monthly_arr) + list(bus_monthly_arr),
    })
    s1_long["Month"] = pd.Categorical(s1_long["Month"], categories=MONTHS, ordered=True)

    s1_bar = alt.Chart(s1_long).mark_bar(
        cornerRadiusTopLeft=3, cornerRadiusTopRight=3
    ).encode(
        x=month_axis(),
        y=alt.Y("tCO2e:Q", stack="zero", title="tCO₂e"),
        color=alt.Color("Type:N",
            scale=alt.Scale(domain=["Fuel vouchers","Bus/Van trips"],
                            range=[COLOR_S1,"#5DCAA5"]),
            legend=alt.Legend(orient="top", title=None)),
        tooltip=[alt.Tooltip("Month:N"), alt.Tooltip("Type:N"),
                 alt.Tooltip("tCO2e:Q", format=".5f", title="tCO₂e")],
    )
    s1_line = alt.Chart(trend_df).mark_line(
        color=COLOR_TOT, strokeWidth=1.5, strokeDash=[4,2], point=True
    ).encode(
        x=month_axis(),
        y=alt.Y("Scope1:Q"),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("Scope1:Q", format=".5f", title="Total S1 tCO₂e")],
    )
    st.altair_chart((s1_bar+s1_line).properties(height=260), use_container_width=True)

    st.markdown("#### Transactions")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        disp_v = vehicle_raw[["Date","Source","Fuel_type","Liters","tCO2e"]].copy()
        disp_v.columns = ["Date","Source","Fuel","Liters","tCO₂e"]
        disp_v["Liters"] = disp_v["Liters"].map("{:,.1f}".format)
        disp_v["tCO₂e"]  = disp_v["tCO₂e"].map("{:.5f}".format)
        st.markdown("**Fuel vouchers**")
        st.dataframe(disp_v, use_container_width=True, hide_index=True)
    with col_t2:
        disp_b = bus_raw[["Date","Destination","Source","Distance_km","tCO2e"]].copy()
        disp_b.columns = ["Date","Destination","Vehicle","km","tCO₂e"]
        disp_b["tCO₂e"] = disp_b["tCO₂e"].map("{:.6f}".format)
        st.markdown("**Bus/Van trips**")
        st.dataframe(disp_b, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SCOPE 2 DETAIL
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<span class="badge-s2">Scope 2</span>&nbsp; Purchased Electricity — location-based', unsafe_allow_html=True)
    st.markdown(" ")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Scope 2",      f"{total_s2:.3f} tCO₂e")
    m2.metric("Total consumption",  f"{total_kwh/1000:.1f} MWh")
    m3.metric("Monthly avg",        f"{int(total_kwh/12):,} kWh")
    m4.metric("Peak month",         "July — 48,569 kWh")
    m5.metric("Grid factor",        f"{ef_grid:.3f} kgCO₂e/kWh")

    # ── Chart 1: Dual-axis bar (kWh) + line (tCO2e) ───────────────────────
    st.markdown('<p class="section-label">Monthly consumption (kWh) vs emissions (tCO₂e)</p>', unsafe_allow_html=True)

    elec_plot = elec_df.copy()
    elec_plot["Month"] = pd.Categorical(elec_plot["Month"], categories=MONTHS, ordered=True)

    bar_kwh = alt.Chart(elec_plot).mark_bar(
        color="#9FE1CB", cornerRadiusTopLeft=3, cornerRadiusTopRight=3
    ).encode(
        x=month_axis(),
        y=alt.Y("kWh:Q", title="kWh", axis=alt.Axis(titleColor="#1D9E75")),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("kWh:Q",   format=",.0f", title="kWh"),
                 alt.Tooltip("tCO2e:Q", format=".3f",  title="tCO₂e")],
    )
    line_co2 = alt.Chart(elec_plot).mark_line(
        color="#0F6E56", strokeWidth=2.5
    ).encode(
        x=month_axis(),
        y=alt.Y("tCO2e:Q", title="tCO₂e",
                axis=alt.Axis(titleColor="#0F6E56")),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("tCO2e:Q", format=".3f", title="tCO₂e")],
    )
    pts_co2 = alt.Chart(elec_plot).mark_point(
        color="#0F6E56", filled=True, size=55
    ).encode(
        x=month_axis(),
        y=alt.Y("tCO2e:Q"),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("tCO2e:Q", format=".3f", title="tCO₂e")],
    )
    avg_line = alt.Chart(pd.DataFrame({"y":[elec_kwh.mean()]})).mark_rule(
        color=COLOR_AVG, strokeDash=[4,2], strokeWidth=1.4
    ).encode(y="y:Q")

    dual = alt.layer(bar_kwh, avg_line, line_co2+pts_co2).resolve_scale(y="independent")
    st.altair_chart(dual.properties(height=300), use_container_width=True)
    st.caption(f"Dashed red line = annual average ({elec_kwh.mean():,.0f} kWh)")

    # ── Chart 2: Scope 2 area + rolling avg ──────────────────────────────────
    st.markdown('<p class="section-label">Scope 2 emissions — area with 3-month rolling average</p>', unsafe_allow_html=True)

    s2_area = alt.Chart(trend_df).mark_area(
        color=COLOR_S2, opacity=0.2,
        line={"color": COLOR_S2, "strokeWidth":2}
    ).encode(
        x=month_axis(),
        y=alt.Y("Scope2:Q", title="tCO₂e"),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("Scope2:Q", format=".3f", title="tCO₂e")],
    )
    s2_roll_line = alt.Chart(trend_df).mark_line(
        color=COLOR_AVG, strokeWidth=2, strokeDash=[4,2]
    ).encode(
        x=month_axis(),
        y=alt.Y("Roll_S2:Q"),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("Roll_S2:Q", format=".3f", title="3-mo rolling avg")],
    )
    s2_proj_line = alt.Chart(trend_df).mark_line(
        color=COLOR_INT, strokeWidth=1.5, strokeDash=[2,2], opacity=0.8
    ).encode(
        x=month_axis(),
        y=alt.Y("Proj_S2:Q"),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("Proj_S2:Q", format=".3f", title="Linear projection")],
    )
    scope2_chart = s2_area + s2_roll_line
    if show_proj:
        scope2_chart = scope2_chart + s2_proj_line
    st.altair_chart(scope2_chart.properties(height=280), use_container_width=True)
    st.caption("Dashed red = 3-month rolling average  ·  Orange dashes = linear trend projection")

    # ── Chart 3: Carbon intensity (flat if EF constant, but dynamic with EF changes) ──
    st.markdown('<p class="section-label">Scope 2 carbon intensity (kgCO₂e per kWh)</p>', unsafe_allow_html=True)

    intensity_area = alt.Chart(trend_df).mark_area(
        color=COLOR_INT, opacity=0.15,
        line={"color": COLOR_INT, "strokeWidth":2}
    ).encode(
        x=month_axis(),
        y=alt.Y("Intensity:Q", title="kgCO₂e / kWh",
                scale=alt.Scale(domain=[0, intensity.max()*1.3])),
        tooltip=[alt.Tooltip("Month:N"),
                 alt.Tooltip("Intensity:Q", format=".4f", title="kgCO₂e/kWh"),
                 alt.Tooltip("kWh:Q", format=",.0f")],
    )
    intensity_pts = alt.Chart(trend_df).mark_point(
        color=COLOR_INT, filled=True, size=60
    ).encode(
        x=month_axis(),
        y=alt.Y("Intensity:Q"),
    )
    avg_intensity_rule = alt.Chart(pd.DataFrame({"y":[intensity.mean()]})).mark_rule(
        color=COLOR_AVG, strokeDash=[3,2], strokeWidth=1.2
    ).encode(y="y:Q")
    st.altair_chart((intensity_area+intensity_pts+avg_intensity_rule).properties(height=220),
                    use_container_width=True)

    # ── Table ─────────────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Monthly breakdown</p>', unsafe_allow_html=True)
    disp_e = elec_df[["Month","kWh","MWh","tCO2e","Meters"]].copy()
    disp_e.columns = ["Month","kWh","MWh","tCO₂e","Meters"]
    disp_e["kWh"]   = disp_e["kWh"].map("{:,.0f}".format)
    disp_e["MWh"]   = disp_e["MWh"].map("{:.3f}".format)
    disp_e["tCO₂e"] = disp_e["tCO₂e"].map("{:.4f}".format)
    st.dataframe(disp_e, use_container_width=True, hide_index=True)
    st.caption(f"Grid emission factor: {ef_grid:.4f} kgCO₂e/kWh (Tunisia STEG) · Adjust in sidebar → all charts update live")
