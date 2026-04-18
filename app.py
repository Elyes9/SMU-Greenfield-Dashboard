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
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    [data-testid="stMetric"] {
        background: white;
        border: 0.5px solid #e0e0e0;
        border-radius: 10px;
        padding: 14px 18px;
    }
    .badge-s1 {
        background: #E6F1FB; color: #0C447C;
        padding: 3px 10px; border-radius: 6px;
        font-size: 12px; font-weight: 600;
    }
    .badge-s2 {
        background: #E1F5EE; color: #085041;
        padding: 3px 10px; border-radius: 6px;
        font-size: 12px; font-weight: 600;
    }
    .insight-box {
        background: #f8fafb;
        border-left: 3px solid #378ADD;
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 13px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]

# ── Sidebar — adjustable emission factors ──────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Emission factors")
    ef_diesel   = st.number_input("Diesel (kgCO₂e / L)",   value=2.68,  step=0.01,  format="%.3f")
    ef_gasoline = st.number_input("Gasoline (kgCO₂e / L)", value=2.31,  step=0.01,  format="%.3f")
    ef_bus_km   = st.number_input("Bus/Van (kgCO₂e / km)", value=0.089, step=0.001, format="%.4f")
    ef_grid     = st.number_input("Grid (kgCO₂e / kWh)",   value=0.267, step=0.001, format="%.4f")
    st.divider()
    st.markdown("**Framework:** GHG Protocol")
    st.markdown("**Reporting year:** 2025")
    st.markdown("**Grid:** Tunisia (STEG)")
    st.markdown('<span class="badge-s1">Scope 1</span> Mobile combustion',    unsafe_allow_html=True)
    st.markdown('<span class="badge-s2">Scope 2</span> Purchased electricity', unsafe_allow_html=True)

# ── Raw data ───────────────────────────────────────────────────────────────────
elec_kwh = np.array([28429, 30287, 30262, 19625, 22097, 37937,
                     48569, 43843, 38143, 28139, 23532, 23039])

vehicle_raw = pd.DataFrame({
    "Date":      ["Feb 3, 2025", "Feb 6, 2025", "Dec 31, 2025"],
    "Month_num": [2, 2, 12],
    "Source":    ["Unknown fleet", "Peugeot Bipper", "Peugeot Bipper"],
    "Fuel_type": ["Diesel", "Super Gasoline", "Super Gasoline"],
    "Vouchers":  [96, 96, 96],
    "Total_DT":  [3840, 3840, 3840],
    "Liters":    [1741.496599, 1520.792079, 1520.792079],
})
vehicle_raw["EF"]    = np.where(vehicle_raw["Fuel_type"] == "Diesel", ef_diesel, ef_gasoline)
vehicle_raw["tCO2e"] = vehicle_raw["Liters"] * vehicle_raw["EF"] / 1000

bus_raw = pd.DataFrame({
    "Date":        ["Feb 4, 2025","Oct 1, 2025","Nov 4, 2025","Nov 12, 2025","Nov 15, 2025"],
    "Month_num":   [2, 10, 11, 11, 11],
    "Destination": ["BAKO MOTORS Fouchana","SOFTEN Grombalia",
                    "BAKO MOTORS Fouchana","STEG Radés","BOOTCAMP"],
    "Source":      ["S-CAPADE Van","S-CAPADE Bus","S-CAPADE Bus","S-CAPADE Bus","S-CAPADE Bus"],
    "Fuel":        ["Gasoil 50"] * 5,
    "Distance_km": [22.7, 53.2, 22.7, 14.6, 11.3],
})
bus_raw["tCO2e"] = bus_raw["Distance_km"] * ef_bus_km / 1000

elec_df = pd.DataFrame({
    "Month":     MONTHS,
    "Month_num": np.arange(1, 13),
    "kWh":       elec_kwh,
    "Meters":    np.full(12, 15),
})
elec_df["MWh"]   = elec_df["kWh"] / 1000
elec_df["tCO2e"] = elec_df["kWh"] * ef_grid / 1000

# ── Aggregates ─────────────────────────────────────────────────────────────────
total_s2  = elec_df["tCO2e"].sum()
total_s1v = vehicle_raw["tCO2e"].sum()
total_s1b = bus_raw["tCO2e"].sum()
total_s1  = total_s1v + total_s1b
total_all = total_s1 + total_s2
total_kwh = int(elec_kwh.sum())

# Monthly Scope 1 series
s1_monthly = np.zeros(12)
for _, row in vehicle_raw.iterrows():
    s1_monthly[int(row["Month_num"]) - 1] += row["tCO2e"]
for _, row in bus_raw.iterrows():
    s1_monthly[int(row["Month_num"]) - 1] += row["tCO2e"]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("## 🌿 Carbon Accounting Dashboard — 2025")
st.caption("GHG Protocol Corporate Standard · Scope 1 (Mobile Combustion) + Scope 2 (Purchased Electricity)")

# ── KPI strip ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("🌍 Total emissions",     f"{total_all:.2f} tCO₂e",   "Scope 1 + Scope 2")
k2.metric("🚗 Scope 1 — Direct",   f"{total_s1:.4f} tCO₂e",    "Mobile combustion")
k3.metric("⚡ Scope 2 — Indirect",  f"{total_s2:.2f} tCO₂e",   "Purchased electricity")
k4.metric("💡 Electricity used",    f"{total_kwh/1000:.1f} MWh", "15 meters · 12 months")

st.divider()

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🚗 Scope 1 — Mobile Combustion",
    "⚡ Scope 2 — Electricity",
    "📈 Monthly Trend",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("#### Emissions by scope")
        donut_df = pd.DataFrame({
            "Scope":  ["Scope 1 — Mobile Combustion", "Scope 2 — Electricity"],
            "tCO2e":  [round(total_s1, 4), round(total_s2, 4)],
        })
        donut_df["Pct"] = (donut_df["tCO2e"] / donut_df["tCO2e"].sum() * 100).round(1)

        arc = alt.Chart(donut_df).mark_arc(innerRadius=70, outerRadius=130).encode(
            theta=alt.Theta("tCO2e:Q"),
            color=alt.Color("Scope:N",
                scale=alt.Scale(
                    domain=["Scope 1 — Mobile Combustion", "Scope 2 — Electricity"],
                    range=["#378ADD", "#1D9E75"]
                ),
                legend=alt.Legend(orient="bottom", labelLimit=400)),
            tooltip=[
                alt.Tooltip("Scope:N"),
                alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e"),
                alt.Tooltip("Pct:Q",   format=".1f",  title="%"),
            ],
        ).properties(height=300)
        st.altair_chart(arc, use_container_width=True)

    with col_r:
        st.markdown("#### Scope 1 breakdown by source")
        src_df = pd.DataFrame({
            "Source": ["Diesel (fleet)", "Gasoline (Feb)", "Gasoline (Dec)", "Bus / Van trips"],
            "tCO2e":  [
                vehicle_raw.loc[vehicle_raw["Fuel_type"] == "Diesel", "tCO2e"].sum(),
                vehicle_raw.iloc[1]["tCO2e"],
                vehicle_raw.iloc[2]["tCO2e"],
                bus_raw["tCO2e"].sum(),
            ],
            "Category": ["Vehicle fuel", "Vehicle fuel", "Vehicle fuel", "Distance-based"],
        })

        bar_src = alt.Chart(src_df).mark_bar(
            cornerRadiusTopRight=4, cornerRadiusBottomRight=4
        ).encode(
            x=alt.X("tCO2e:Q", title="tCO₂e", axis=alt.Axis(format=".4f")),
            y=alt.Y("Source:N", sort="-x", title=None),
            color=alt.Color("Category:N",
                scale=alt.Scale(
                    domain=["Vehicle fuel", "Distance-based"],
                    range=["#378ADD", "#5DCAA5"]
                ),
                legend=alt.Legend(orient="bottom")),
            tooltip=[
                alt.Tooltip("Source:N"),
                alt.Tooltip("tCO2e:Q", format=".5f", title="tCO₂e"),
            ],
        ).properties(height=240)

        text_src = bar_src.mark_text(align="left", dx=4, fontSize=11, color="#333").encode(
            text=alt.Text("tCO2e:Q", format=".4f")
        )
        st.altair_chart(bar_src + text_src, use_container_width=True)

    st.markdown("#### Key insights")
    ia, ib, ic = st.columns(3)
    with ia:
        st.markdown(f"""<div class="insight-box">
            <b>🚗 Diesel fleet</b><br>
            Largest single Scope 1 source —
            <b>{vehicle_raw.iloc[0]['tCO2e']:.3f} tCO₂e</b>
            from 1,741 L in February.
        </div>""", unsafe_allow_html=True)
    with ib:
        st.markdown(f"""<div class="insight-box">
            <b>⚡ Peak month — July</b><br>
            48,569 kWh across 15 meters →
            <b>{elec_df.iloc[6]['tCO2e']:.2f} tCO₂e</b>.
        </div>""", unsafe_allow_html=True)
    with ic:
        st.markdown(f"""<div class="insight-box">
            <b>📊 Scope 2 dominates</b><br>
            Electricity accounts for
            <b>{total_s2/total_all*100:.1f}%</b>
            of total emissions.
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SCOPE 1
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<span class="badge-s1">Scope 1</span>&nbsp; Mobile Combustion', unsafe_allow_html=True)
    st.markdown(" ")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Scope 1",      f"{total_s1:.5f} tCO₂e")
    m2.metric("From fuel vouchers", f"{total_s1v:.4f} tCO₂e", "3 transactions")
    m3.metric("From bus/van trips", f"{total_s1b:.5f} tCO₂e", "5 trips")
    m4.metric("Total distance",     "124.5 km", "bus routes")

    st.markdown("#### Vehicle fuel transactions")
    disp_v = vehicle_raw[["Date","Source","Fuel_type","Vouchers","Total_DT","Liters","tCO2e"]].copy()
    disp_v.columns = ["Date","Emission source","Fuel type","Vouchers","Total (DT)","Activity data (L)","tCO₂e"]
    disp_v["Activity data (L)"] = disp_v["Activity data (L)"].map("{:,.1f}".format)
    disp_v["tCO₂e"]             = disp_v["tCO₂e"].map("{:.5f}".format)
    st.dataframe(disp_v, use_container_width=True, hide_index=True)

    st.markdown("#### Bus & van trips — distance-based")
    disp_b = bus_raw[["Date","Destination","Source","Fuel","Distance_km","tCO2e"]].copy()
    disp_b.columns = ["Date","Destination","Vehicle","Fuel","Distance (km)","tCO₂e"]
    disp_b["tCO₂e"] = disp_b["tCO₂e"].map("{:.6f}".format)
    st.dataframe(disp_b, use_container_width=True, hide_index=True)

    st.markdown("#### Monthly Scope 1 profile")
    fuel_monthly = np.zeros(12)
    for _, row in vehicle_raw.iterrows():
        fuel_monthly[int(row["Month_num"]) - 1] += row["tCO2e"]
    bus_monthly = np.zeros(12)
    for _, row in bus_raw.iterrows():
        bus_monthly[int(row["Month_num"]) - 1] += row["tCO2e"]

    s1_month_long = pd.DataFrame({
        "Month":    MONTHS * 2,
        "Type":     ["Fuel vouchers"] * 12 + ["Bus/Van trips"] * 12,
        "tCO2e":    list(fuel_monthly) + list(bus_monthly),
    })
    s1_month_long["Month"] = pd.Categorical(s1_month_long["Month"], categories=MONTHS, ordered=True)

    bar_s1m = alt.Chart(s1_month_long).mark_bar(
        cornerRadiusTopLeft=3, cornerRadiusTopRight=3
    ).encode(
        x=alt.X("Month:N", sort=MONTHS, title=None),
        y=alt.Y("tCO2e:Q", title="tCO₂e", stack="zero"),
        color=alt.Color("Type:N",
            scale=alt.Scale(
                domain=["Fuel vouchers", "Bus/Van trips"],
                range=["#378ADD", "#5DCAA5"]
            ),
            legend=alt.Legend(orient="top", title=None)),
        tooltip=[
            alt.Tooltip("Month:N"),
            alt.Tooltip("Type:N"),
            alt.Tooltip("tCO2e:Q", format=".5f", title="tCO₂e"),
        ],
    ).properties(height=280)
    st.altair_chart(bar_s1m, use_container_width=True)

    st.markdown("#### Emission factors applied")
    st.markdown(f"""
| Source | Method | Emission factor |
|--------|--------|-----------------|
| Diesel vehicles | Activity (L) × EF | **{ef_diesel:.3f}** kgCO₂e / litre |
| Gasoline vehicles | Activity (L) × EF | **{ef_gasoline:.3f}** kgCO₂e / litre |
| Bus / Van (Gasoil 50) | Distance (km) × EF | **{ef_bus_km:.4f}** kgCO₂e / km |
    """)
    st.caption("Source: GHG Protocol Mobile Combustion Tool v2.6  ·  Formula: Activity × EF / 1000 = tCO₂e")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SCOPE 2
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<span class="badge-s2">Scope 2</span>&nbsp; Purchased Electricity — location-based method', unsafe_allow_html=True)
    st.markdown(" ")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Scope 2",     f"{total_s2:.3f} tCO₂e")
    m2.metric("Total consumption", f"{total_kwh/1000:.1f} MWh")
    m3.metric("Avg monthly",       f"{int(total_kwh/12):,} kWh")
    m4.metric("Grid factor",       f"{ef_grid:.3f} kgCO₂e/kWh")

    st.markdown("#### Monthly consumption & emissions")
    elec_plot = elec_df.copy()
    elec_plot["Month"] = pd.Categorical(elec_plot["Month"], categories=MONTHS, ordered=True)

    bar_kwh = alt.Chart(elec_plot).mark_bar(
        color="#9FE1CB", cornerRadiusTopLeft=3, cornerRadiusTopRight=3
    ).encode(
        x=alt.X("Month:N", sort=MONTHS, title=None),
        y=alt.Y("kWh:Q", title="kWh", axis=alt.Axis(titleColor="#1D9E75")),
        tooltip=[
            alt.Tooltip("Month:N"),
            alt.Tooltip("kWh:Q",   format=",.0f", title="kWh"),
            alt.Tooltip("tCO2e:Q", format=".3f",  title="tCO₂e"),
        ],
    )

    line_co2 = alt.Chart(elec_plot).mark_line(
        color="#0F6E56", strokeWidth=2
    ).encode(
        x=alt.X("Month:N", sort=MONTHS),
        y=alt.Y("tCO2e:Q", title="tCO₂e",
                axis=alt.Axis(titleColor="#0F6E56")),
        tooltip=[
            alt.Tooltip("Month:N"),
            alt.Tooltip("tCO2e:Q", format=".3f", title="tCO₂e"),
        ],
    )

    pts_co2 = alt.Chart(elec_plot).mark_point(
        color="#0F6E56", filled=True, size=50
    ).encode(
        x=alt.X("Month:N", sort=MONTHS),
        y=alt.Y("tCO2e:Q"),
    )

    elec_chart = alt.layer(bar_kwh, line_co2 + pts_co2).resolve_scale(
        y="independent"
    ).properties(height=300)
    st.altair_chart(elec_chart, use_container_width=True)

    st.markdown("#### Monthly breakdown table")
    disp_e = elec_df[["Month","kWh","MWh","tCO2e","Meters"]].copy()
    disp_e.columns = ["Month","kWh","MWh","tCO₂e","Meters"]
    disp_e["kWh"]   = disp_e["kWh"].map("{:,.0f}".format)
    disp_e["MWh"]   = disp_e["MWh"].map("{:.2f}".format)
    disp_e["tCO₂e"] = disp_e["tCO₂e"].map("{:.3f}".format)
    st.dataframe(disp_e, use_container_width=True, hide_index=True)
    st.caption(f"🟢 Peak: July (48,569 kWh)  ·  🟡 Lowest: April (19,625 kWh)")

    st.markdown(f"""
#### Emission factor note
| Parameter | Value |
|-----------|-------|
| Emission factor | **{ef_grid:.3f}** kgCO₂e / kWh |
| Method | Location-based (grid average) |
| Grid | Tunisia — STEG national mix |
| Formula | kWh × {ef_grid:.3f} / 1000 = tCO₂e |
    """)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — MONTHLY TREND
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("#### Monthly GHG emissions — all scopes (tCO₂e)")

    trend_df = pd.DataFrame({
        "Month":   MONTHS,
        "Scope 1": s1_monthly,
        "Scope 2": elec_df["tCO2e"].values,
    })
    trend_df["Total"] = trend_df["Scope 1"] + trend_df["Scope 2"]
    trend_df["Month"] = pd.Categorical(trend_df["Month"], categories=MONTHS, ordered=True)

    trend_long = trend_df.melt(
        id_vars=["Month"],
        value_vars=["Scope 1", "Scope 2", "Total"],
        var_name="Series", value_name="tCO2e"
    )

    color_scale = alt.Scale(
        domain=["Scope 1", "Scope 2", "Total"],
        range=["#378ADD", "#1D9E75", "#D4537E"]
    )
    dash_scale = alt.Scale(
        domain=["Scope 1", "Scope 2", "Total"],
        range=[[1, 0], [1, 0], [6, 3]]
    )

    lines = alt.Chart(trend_long).mark_line(strokeWidth=2).encode(
        x=alt.X("Month:N", sort=MONTHS, title=None),
        y=alt.Y("tCO2e:Q", title="tCO₂e"),
        color=alt.Color("Series:N", scale=color_scale,
                        legend=alt.Legend(orient="top", title=None)),
        strokeDash=alt.StrokeDash("Series:N", scale=dash_scale),
        tooltip=[
            alt.Tooltip("Month:N"),
            alt.Tooltip("Series:N"),
            alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e"),
        ],
    )
    points = alt.Chart(trend_long).mark_point(filled=True, size=55).encode(
        x=alt.X("Month:N", sort=MONTHS),
        y=alt.Y("tCO2e:Q"),
        color=alt.Color("Series:N", scale=color_scale),
        tooltip=[
            alt.Tooltip("Month:N"),
            alt.Tooltip("Series:N"),
            alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e"),
        ],
    )
    st.altair_chart((lines + points).properties(height=340), use_container_width=True)

    st.markdown("#### Monthly stacked contribution")
    stack_long = trend_df.melt(
        id_vars=["Month"],
        value_vars=["Scope 1", "Scope 2"],
        var_name="Scope", value_name="tCO2e"
    )
    stack_long["Month"] = pd.Categorical(stack_long["Month"], categories=MONTHS, ordered=True)

    stacked = alt.Chart(stack_long).mark_bar(
        cornerRadiusTopLeft=3, cornerRadiusTopRight=3
    ).encode(
        x=alt.X("Month:N", sort=MONTHS, title=None),
        y=alt.Y("tCO2e:Q", stack="zero", title="tCO₂e"),
        color=alt.Color("Scope:N",
            scale=alt.Scale(
                domain=["Scope 1", "Scope 2"],
                range=["#378ADD", "#1D9E75"]
            ),
            legend=alt.Legend(orient="top", title=None)),
        tooltip=[
            alt.Tooltip("Month:N"),
            alt.Tooltip("Scope:N"),
            alt.Tooltip("tCO2e:Q", format=".4f", title="tCO₂e"),
        ],
    ).properties(height=260)
    st.altair_chart(stacked, use_container_width=True)

    st.markdown("#### Annual summary")
    summary = pd.DataFrame({
        "Metric": [
            "Total Scope 1 (tCO₂e)",
            "Total Scope 2 (tCO₂e)",
            "Grand total (tCO₂e)",
            "Scope 1 share (%)",
            "Scope 2 share (%)",
            "Peak electricity month",
            "Total electricity (MWh)",
        ],
        "Value": [
            f"{total_s1:.5f}",
            f"{total_s2:.3f}",
            f"{total_all:.3f}",
            f"{total_s1/total_all*100:.2f}%",
            f"{total_s2/total_all*100:.2f}%",
            f"July 2025 ({elec_df.iloc[6]['kWh']:,} kWh)",
            f"{total_kwh/1000:.1f}",
        ],
    })
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.caption("Adjust emission factors in the sidebar — all charts and tables update in real time.")
