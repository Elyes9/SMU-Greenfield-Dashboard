st.header("🔥 Scope 1 Emissions")

st.write("Direct emissions from fuels and owned sources.")

st.dataframe(scope1_df)

# Detect emission column
emission_column_scope1 = None
for col in scope1_df.columns:
    if "emission" in col or "co2" in col:
        emission_column_scope1 = col
        break

if emission_column_scope1:

    # convert to numeric safely
    scope1_df[emission_column_scope1] = pd.to_numeric(
        scope1_df[emission_column_scope1],
        errors="coerce"
    )

    # replace NaN with 0
    scope1_df[emission_column_scope1] = scope1_df[emission_column_scope1].fillna(0)

    total_scope1 = scope1_df[emission_column_scope1].sum()

    st.metric(
        "Total Scope 1 Emissions",
        str(round(total_scope1,2)) + " kgCO2e"
    )

    st.subheader("Scope 1 Emissions Distribution")

    plot_scope1 = scope1_df.groupby(emission_column_scope1).sum(numeric_only=True)

    st.bar_chart(scope1_df[emission_column_scope1])

else:
    st.warning("Emission column not detected in Scope 1 dataset.")
