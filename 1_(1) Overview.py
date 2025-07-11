# pages/1_Fuel_Overview_Comparison.py

import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.colors import hex_to_rgb

st.set_page_config(page_title="Fuel Overview Comparison", layout="wide")

st.title("💼 Fuel Overview Comparison")

# -----------------------
# 📂 Load master.xlsx
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_excel("master.xlsx", sheet_name=0)
    df['Scenario'] = pd.to_numeric(df['Scenario'], errors='coerce').astype("Int64")
    df[df.columns[4:]] = df[df.columns[4:]].apply(pd.to_numeric, errors='coerce')
    df['Group'] = df['System'].apply(get_process_group_from_system)
    return df

def get_process_group_from_system(system_name):
    if "1." in system_name:
        return 'construction'
    elif "2." in system_name:
        return 'rawmaterial'
    elif "3." in system_name:
        return 'pretreatment'
    elif "4." in system_name:
        return 'conversion'
    elif "5." in system_name:
        return 'transportation'
    else:
        return 'other'

def hex_to_rgb_str(hex_code):
    r, g, b = hex_to_rgb(hex_code)
    return f'rgb({r},{g},{b})'

# -----------------------
# Load & Setup
# -----------------------
df = load_data()
impact_categories = df.columns[4:].tolist()

variant_map = {
    'STL1': {'Fuel': 'STL', 'Scenario': [0, 1]},
    'STL2': {'Fuel': 'STL', 'Scenario': [0, 2]},
    'STL3': {'Fuel': 'STL', 'Scenario': [0, 3]},
    'PTL1': {'Fuel': 'PTL', 'Scenario': [0, 1]},
    'PTL2': {'Fuel': 'PTL', 'Scenario': [0, 2]},
    'PTL3': {'Fuel': 'PTL', 'Scenario': [0, 3]},
    'PTL4': {'Fuel': 'PTL', 'Scenario': [0, 4]},
    'PBTL1': {'Fuel': 'PBTL', 'Scenario': [0, 1]},
    'PBTL2': {'Fuel': 'PBTL', 'Scenario': [0, 2]},
    'PBTL3': {'Fuel': 'PBTL', 'Scenario': [0, 3]},
    'PBTL4': {'Fuel': 'PBTL', 'Scenario': [0, 4]},
    'BTL': {'Fuel': 'BTL', 'Scenario': [0]},
    'HEFA1': {'Fuel': 'HEFA', 'Scenario': [0, 1]},
    'HEFA2': {'Fuel': 'HEFA', 'Scenario': [0, 2]},
    'HEFA3': {'Fuel': 'HEFA', 'Scenario': [0, 3]},
    'HEFA4': {'Fuel': 'HEFA', 'Scenario': [0, 4]},
}

# Sidebar UI
selected_variant = st.sidebar.selectbox("Select Fuel Variant", list(variant_map.keys()))
selected_impact = st.sidebar.selectbox("Select Impact Category", impact_categories)
red_weight = st.sidebar.selectbox("Select RED III Weighting", [2, 3], index=0)

color_order = ["STL", "PTL", "PBTL", "BTL", "HEFA"]
default_colors = {
    'STL': '#FF0000',
    'PTL': '#0000FF',
    'PBTL': '#90EE90',
    'BTL': '#008000',
    'HEFA': '#FFA900'
}
st.sidebar.markdown("### 🎨 Fuel Color Settings")
color_map = {
    fuel: st.sidebar.color_picker(f"{fuel} Color", default_colors[fuel])
    for fuel in color_order
}

# Filter selected variant
rule = variant_map[selected_variant]
filtered_df = df[(df['Fuel'] == rule['Fuel']) & (df['Scenario'].isin(rule['Scenario']))]

# 🔄 Aggregate values by variant
base_records = []
for variant, vrule in variant_map.items():
    sub_df = df[(df['Fuel'] == vrule['Fuel']) & (df['Scenario'].isin(vrule['Scenario']))]
    total = sub_df[selected_impact].sum()
    base_records.append({'Variant': variant, selected_impact: total, 'Fuel type': vrule['Fuel']})

agg_df = pd.DataFrame(base_records)
agg_df['FuelOrder'] = pd.Categorical(agg_df['Fuel type'], categories=color_order, ordered=True)
agg_df = agg_df.sort_values(['FuelOrder', 'Variant'])

# 📈 Main chart
fig = px.bar(
    agg_df,
    x='Variant',
    y=selected_impact,
    color='Fuel type',
    title=f"{selected_impact} by Fuel Variant",
    labels={'Variant': 'Fuel Scenario', selected_impact: selected_impact},
    color_discrete_map=color_map
)

# ⚠️ RED III reference lines
if "climate change" in selected_impact.lower():
    fig.add_hline(
        y=4.127,
        line_dash="solid",
        line_color="black",
        annotation_text="Petroleum Jet Fuel Baseline",
        annotation_position="top right"
    )
    fig.add_hline(
        y=1.238,
        line_dash="dashdot",
        line_color="black",
        annotation_text="RED III 70% Reduction Target",
        annotation_position="top right"
    )

fig.update_yaxes(title_text="kg CO₂-eq / kg fuel")

st.plotly_chart(fig, use_container_width=True)
st.dataframe(
    agg_df[["Variant", selected_impact, "Fuel type"]].style.format(precision=10),
    use_container_width=True
)
