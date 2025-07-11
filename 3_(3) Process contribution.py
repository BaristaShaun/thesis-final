import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.colors import hex_to_rgb

st.set_page_config(
    page_title="Process Group Contribution",
    layout="wide"
)

def app():
    # -----------------------
    # 🔧 Functions
    # -----------------------
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
    # 📂 Load master.xlsx
    # -----------------------
    try:
        df = pd.read_excel("master.xlsx", sheet_name=0)
        df['Scenario'] = pd.to_numeric(df['Scenario'], errors='coerce')
        impact_categories = df.columns[4:]
        df[impact_categories] = df[impact_categories].apply(pd.to_numeric, errors='coerce')
        df['Group'] = df['System'].apply(get_process_group_from_system)
    except FileNotFoundError:
        st.error("Could not find **master.xlsx** file.")
        return

    # -----------------------
    # 📍 Sidebar 선택
    # -----------------------
    view = st.sidebar.radio("Select View", ["Process Group Contribution"])
    selected_impact = st.sidebar.selectbox("Select Impact Category", impact_categories)

    # -----------------------
    # 🚀 Variant Mapping
    # -----------------------
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
        'HEFA4': {'Fuel': 'HEFA', 'Scenario': [0, 4]}
    }

    preferred_order = list(variant_map.keys())
    group_order = ["construction", "rawmaterial", "pretreatment", "conversion", "transportation"]
    group_name_map = {
        "construction": "1. Construction",
        "rawmaterial": "2. Raw material acquisition",
        "pretreatment": "3. Pretreatment",
        "conversion": "4. Conversion",
        "transportation": "5. Transportation"
    }
    color_order = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]

    # -----------------------
    # 🌍 Process Group Contribution View
    # -----------------------
    if view == "Process Group Contribution":
        st.subheader(f"📊 {selected_impact} Contribution by System Group per Fuel Variant")

        records = []
        for variant, rule in variant_map.items():
            variant_df = df[(df['Fuel'] == rule['Fuel']) & (df['Scenario'].isin(rule['Scenario']))].copy()
            if variant_df.empty:
                continue
            group_sum = variant_df.groupby("Group")[selected_impact].sum()
            total = group_sum.sum()
            for group, val in group_sum.items():
                percent = (val / total) * 100 if total > 0 else 0
                records.append({
                    "Variant": variant,
                    "Group": group_name_map.get(group, group),
                    "Contribution (%)": percent
                })

        impact_df = pd.DataFrame(records)
        impact_df["Variant"] = pd.Categorical(impact_df["Variant"], categories=preferred_order, ordered=True)
        impact_df = impact_df.sort_values("Variant")

        fig = px.bar(
            impact_df,
            x="Variant",
            y="Contribution (%)",
            color="Group",
            title=f"📊 {selected_impact} Contribution by System Group per Fuel Variant",
            barmode="stack",
            height=600,
            category_orders={"Group": [group_name_map[g] for g in group_order]},
            color_discrete_sequence=color_order
        )
        fig.update_xaxes(title_font=dict(color="black", size=16), tickfont=dict(color="black", size=14))
        fig.update_yaxes(title_font=dict(color="black", size=16), tickfont=dict(color="black", size=14))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(impact_df.style.format({"Contribution (%)": "{:.2f}%"}))
app()