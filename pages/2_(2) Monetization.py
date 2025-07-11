import streamlit as st
import pandas as pd
import plotly.express as px
from difflib import get_close_matches

st.set_page_config(
    page_title="LCA Monetization Dashboard",
    layout="wide"
)

def app():
    st.title("💰 LCA Fuel Variant Monetization Dashboard")

    # 📂 Load master.xlsx
    df = pd.read_excel("master.xlsx", sheet_name=0)

    # 📶 Monetization Factor Selection
    tabs = ["Low", "Central", "High"]
    scenario_level = st.sidebar.selectbox("Select Monetization Scenario", tabs, index=1)
    scenario_index = {"Low": 0, "Central": 1, "High": 2}[scenario_level]

    # 📦 Monetization Factors
    monetization_factors_all = {
        "Climate change (kg CO₂ eq.)": [0.0615, 0.1025, 0.1936],
        "Ozone Depletion Potential (kg CFC-11 eq.)": [22.8, 31.4, 127.2],
        "Ionising Radiation – Human Health (kBq U-235 eq.)": [0.0008, 0.00120, 0.0461],
        "Photochemical Ozone Creation Potential (kg NMVOC eq.)": [0.87, 1.19, 1.90],
        "Particulate Matter Formation (Disease incidence)": [661974, 784126, 1204600],
        "Human Toxicity – Non-Carcinogenic (CTUh)": [30211, 163447, 755270],
        "Human Toxicity – Carcinogenic (CTUh)": [174324, 902616, 2789181],
        "Acidification (mol H⁺ eq.)": [0.176, 0.344, 1.617],
        "Eutrophication Potential – Freshwater (kg P eq.)": [0.26, 1.92, 2.18],
        "Eutrophication Potential – Marine (kg N eq.)": [3.21, 3.21, 3.21],
        "Ecotoxicity – Freshwater (CTUe)": [2.39e-24, 3.82e-05, 1.89e-04],
        "Land Use (Pt)": [0.000087, 0.000175, 0.000349],
        "Water Use (m³ world eq.)": [0.00419, 0.00499, 0.2359],
        "Resource Use – Fossils (MJ)": [0, 0.0013, 0.0068],
        "Material resources: metals/minerals (kg Sb eq.)": [0, 1.64, 6.53]
    }

    color_presets = {
        "Climate change (kg CO₂ eq.)": "#ff4d4d",
        "Ozone Depletion Potential (kg CFC-11 eq.)": "#800000",
        "Particulate Matter Formation (Disease incidence)": "#808000",
        "Photochemical Ozone Creation Potential (kg NMVOC eq.)": "#ffa500",
        "Ionising Radiation – Human Health (kBq U-235 eq.)": "#800080",
        "Acidification (mol H⁺ eq.)": "#ff69b4",
        "Eutrophication Potential – Freshwater (kg P eq.)": "#32cd32",
        "Water Use (m³ world eq.)": "#1e90ff",
        "Human Toxicity – Carcinogenic (CTUh)": "#a52a2a",
        "Human Toxicity – Non-Carcinogenic (CTUh)": "#8b4513",
        "Land Use (Pt)": "#deb887",
        "Resource Use – Fossils (MJ)": "#20b2aa",
        "Material resources: metals/minerals (kg Sb eq.)": "#4682b4"
    }

    column_manual_overrides = {
        "Resource Use – Fossils (MJ)": "Energy resources: non-renewable (MJ)"
    }

    user_monetization_factors = {}
    custom_color_dict = {}
    for category, values in monetization_factors_all.items():
        factor = values[scenario_index]
        color = color_presets.get(category, "#000000")
        user_monetization_factors[category] = factor
        custom_color_dict[category] = color

    st.sidebar.markdown(f"🔧 Factors from **{scenario_level}** scenario")

    monetization_df = pd.DataFrame([
        {"Category": cat, "Factor (€/unit)": val, "Color": custom_color_dict[cat]}
        for cat, val in user_monetization_factors.items()
    ])

    fig = px.bar(
        monetization_df,
        x="Category",
        y="Factor (€/unit)",
        color="Category",
        title=f"💶 Monetization Factors - {scenario_level} Scenario",
        color_discrete_map=custom_color_dict
    )
    fig.update_layout(showlegend=False, xaxis_tickangle=-45, height=600)
    st.plotly_chart(fig, use_container_width=True)

    column_mapping = {}
    for key in user_monetization_factors:
        if key in column_manual_overrides:
            column_mapping[key] = column_manual_overrides[key]
        else:
            match = get_close_matches(key, df.columns, n=1, cutoff=0.6)
            if match:
                column_mapping[key] = match[0]

    matched_columns = list(column_mapping.values())

    apply_adjustment = st.sidebar.checkbox("✅ Apply CO₂ correction (-7.4kg for STL, -6.34kg for PTL)")

    st.subheader("📊 Total Monetized Cost per Fuel Variant")

    variant_map = {
        'STL1': {'Fuel': 'STL', 'Scenario': [0, 1]},
        'STL2': {'Fuel': 'STL', 'Scenario': [0, 2]},
        'STL3': {'Fuel': 'STL', 'Scenario': [0, 3]},
        'HEFA1': {'Fuel': 'HEFA', 'Scenario': [0, 1]},
        'HEFA2': {'Fuel': 'HEFA', 'Scenario': [0, 2]},
        'HEFA3': {'Fuel': 'HEFA', 'Scenario': [0, 3]},
        'HEFA4': {'Fuel': 'HEFA', 'Scenario': [0, 4]},
        'PBTL1': {'Fuel': 'PBTL', 'Scenario': [0, 1]},
        'PBTL2': {'Fuel': 'PBTL', 'Scenario': [0, 2]},
        'PBTL3': {'Fuel': 'PBTL', 'Scenario': [0, 3]},
        'PBTL4': {'Fuel': 'PBTL', 'Scenario': [0, 4]},
        'BTL': {'Fuel': 'BTL', 'Scenario': [0]},
        'PTL1': {'Fuel': 'PTL', 'Scenario': [0, 1]},
        'PTL2': {'Fuel': 'PTL', 'Scenario': [0, 2]},
        'PTL3': {'Fuel': 'PTL', 'Scenario': [0, 3]},
        'PTL4': {'Fuel': 'PTL', 'Scenario': [0, 4]}
    }

    monetized_data = []
    for variant, rule in variant_map.items():
        subset = df[(df['Fuel'] == rule['Fuel']) & (df['Scenario'].isin(rule['Scenario']))].copy()
        co2_col = column_mapping.get("Climate change (kg CO₂ eq.)")
        if apply_adjustment and co2_col in subset.columns:
            if rule['Fuel'] == 'STL':
                subset[co2_col] -= 7.4
            elif rule['Fuel'] == 'PTL':
                subset[co2_col] -= 6.34

        impact_sum = subset[matched_columns].sum()
        total_cost = 0.0
        for key in column_mapping:
            col = column_mapping[key]
            if col in impact_sum:
                val = float(impact_sum[col])
                total_cost += val * user_monetization_factors[key]

        monetized_data.append({
            "Variant": variant,
            "Fuel": rule['Fuel'],
            "Monetized Cost (€)": "❌" if rule['Fuel'] in ['STL', 'PTL'] and apply_adjustment else round(total_cost, 2)
        })

    result_df = pd.DataFrame(monetized_data)
    st.dataframe(result_df.style.format({"Monetized Cost (€)": lambda v: v if v == "❌" else f"€{v:.2f}"}))

    # -----------------------
    # 📊 Cost Breakdown Chart
    # -----------------------
    st.subheader("📊 Cost Breakdown by Impact Category")

    def strip_unit(name):
        return name.split(" (")[0]

    category_cost_records = []
    for variant, rule in variant_map.items():
        subset = df[(df['Fuel'] == rule['Fuel']) & (df['Scenario'].isin(rule['Scenario']))].copy()
        if apply_adjustment and co2_col in subset.columns:
            if rule['Fuel'] == 'STL':
                subset[co2_col] -= 7.4
            elif rule['Fuel'] == 'PTL':
                subset[co2_col] -= 6.34

        impact_sum = subset[matched_columns].sum()
        for category in user_monetization_factors:
            if category in column_mapping:
                column_name = column_mapping[category]
                val = float(impact_sum[column_name])
                cost = val * user_monetization_factors[category]
                category_cost_records.append({
                    "Variant": variant,
                    "Fuel": rule['Fuel'],
                    "Impact Category": category,
                    "Cost (€)": cost,
                    "Mark": "❌" if rule['Fuel'] in ['STL', 'PTL'] and apply_adjustment else ""
                })

    stacked_df = pd.DataFrame(category_cost_records)
    stacked_df["Label"] = stacked_df["Variant"] + stacked_df["Mark"]

    preferred_order = [
        "STL1", "STL2", "STL3",
        "PTL1", "PTL2", "PTL3", "PTL4",
        "PBTL1", "PBTL2", "PBTL3", "PBTL4",
        "BTL",
        "HEFA1", "HEFA2", "HEFA3", "HEFA4"
    ]
    if apply_adjustment:
        preferred_order = [v + "❌" if any([v.startswith('STL'), v.startswith('PTL')]) else v for v in preferred_order]

    stacked_df["Label"] = pd.Categorical(stacked_df["Label"], categories=preferred_order, ordered=True)
    stacked_df = stacked_df.sort_values("Label")
    stacked_df["Impact Category Clean"] = stacked_df["Impact Category"].apply(strip_unit)
    clean_color_dict = {strip_unit(k): v for k, v in custom_color_dict.items()}

    fig = px.bar(
        stacked_df,
        x="Label",
        y="Cost (€)",
        color="Impact Category Clean",
        title="📊 Variant-wise Monetized Cost Breakdown by Impact Category",
        color_discrete_map=clean_color_dict,
        height=700
    )
    fig.update_layout(
        xaxis_title="Fuel Variant",
        yaxis_title="External Cost (€/kg fuel)",
        xaxis_tickfont=dict(size=14),
        yaxis_tickfont=dict(size=14),
        legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        label="📅 Download Result as CSV",
        data=result_df.to_csv(index=False).encode('utf-8'),
        file_name="fuel_variant_monetization.csv",
        mime="text/csv"
    )
app()