import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from streamlit_echarts import st_echarts

st.set_page_config(
    page_title="Scenario Trend Viewer",
    layout="wide"
)

def app():
    csv_file_names = ["Optimistic.csv", "Middle.csv", "Pessimistic.csv"]
    scenario_dfs = {}
    for file_name in csv_file_names:
        try:
            df_csv = pd.read_csv(file_name)
            df_csv = df_csv[df_csv["Year"] <= 2050]
            scenario_dfs[file_name.replace('.csv', '')] = df_csv
        except FileNotFoundError:
            st.warning(f"⚠️ Could not find `{file_name}`. Skipped.")

    tab1, tab2 = st.tabs(["📈 Scenario Trend Analysis", "📊 Multi-Fuel Grid View"])

    # -----------------------
    # Tab 1: ECharts
    # -----------------------
    with tab1:
        dataset_names = list(scenario_dfs.keys())
        selected_datasets = st.multiselect("Select datasets to visualize", dataset_names, default=dataset_names)

        if selected_datasets:
            first_df = scenario_dfs[selected_datasets[0]]
            columns = first_df.columns[1:]
            selected_columns = st.multiselect("Select columns to visualize", columns, default=[columns[0]])

            if selected_columns:
                series = []
                color_mapping = {"Optimistic": "green", "Middle": "black", "Pessimistic": "red"}
                for dataset_name in selected_datasets:
                    df = scenario_dfs[dataset_name]
                    for col in selected_columns:
                        series.append({
                            "name": f"{dataset_name} - {col}",
                            "type": "line",
                            "data": df[col].tolist(),
                            "lineStyle": {"color": color_mapping.get(dataset_name, "blue")},
                            "itemStyle": {"color": color_mapping.get(dataset_name, "blue")},
                            "markLine": {
                                "data": [
                                    {
                                        "yAxis": 1.238,
                                        "lineStyle": {"type": "dash", "color": "#444"},
                                        "label": {"formatter": "RED III Target (1.238)", "position": "end"}
                                    },
                                    {
                                        "yAxis": 4.127,
                                        "lineStyle": {"type": "solid", "color": "#222"},
                                        "label": {"formatter": "Jet Fuel Baseline (4.127)", "position": "end"}
                                    }
                                ]
                            }
                        })

                options = {
                    "title": {"text": "Yearly Trends Across Scenarios"},
                    "tooltip": {"trigger": "axis"},
                    "legend": {
                        "type": "scroll",
                        "orient": "horizontal",
                        "top": "bottom",
                        "data": [s["name"] for s in series]
                    },
                    "xAxis": {
                        "type": "category",
                        "data": first_df["Year"].tolist(),
                        "name": "Year"
                    },
                    "yAxis": {
                        "type": "value",
                        "name": "kg CO₂-eq/kg fuel"
                    },
                    "series": series,
                }

                st_echarts(options=options, height="600px")

    # -----------------------
    # Tab 2: Matplotlib Grid
    # -----------------------
    with tab2:
        st.subheader("16 Fuel Types - 3 Scenarios (Up to 2050)")

        if scenario_dfs:
            all_fuels = [col for col in scenario_dfs["Optimistic"].columns if col != "Year"]

            def fuel_sort_key(fuel):
                if "STL" in fuel:
                    return (0, fuel)
                elif "PTL" in fuel:
                    return (1, fuel)
                elif "PBTL" in fuel:
                    return (2, fuel)
                elif "BTL" in fuel:
                    return (3, fuel)
                elif "HEFA" in fuel:
                    return (4, fuel)
                else:
                    return (5, fuel)

            fuel_columns = sorted(all_fuels, key=fuel_sort_key)

            def get_label_style(fuel_name):
                if "STL" in fuel_name:
                    return {"color": "red", "label": fuel_name}
                elif "PTL" in fuel_name:
                    return {"color": "blue", "label": fuel_name}
                elif "PBTL" in fuel_name:
                    return {"color": "limegreen", "label": fuel_name}
                elif "BTL" in fuel_name:
                    return {"color": "green", "label": fuel_name}
                elif "HEFA" in fuel_name:
                    return {"color": "darkorange", "label": fuel_name}
                else:
                    return {"color": "black", "label": fuel_name}

            all_values = []
            for df in scenario_dfs.values():
                all_values.extend(df[fuel_columns].values.flatten())
            ymin, ymax = min(all_values), max(all_values)

            fig = plt.figure(figsize=(30, 15))
            gs = gridspec.GridSpec(4, 4, wspace=0.3, hspace=0.4)

            for i, fuel in enumerate(fuel_columns):
                row, col = divmod(i, 4)
                ax = fig.add_subplot(gs[row, col])
                for scenario, df in scenario_dfs.items():
                    ax.plot(
                        df["Year"], df[fuel],
                        label=scenario,
                        color={"Optimistic": "green", "Middle": "black", "Pessimistic": "red"}[scenario],
                        linestyle={"Optimistic": "solid", "Middle": "dashed", "Pessimistic": "dotted"}[scenario]
                    )
                style = get_label_style(fuel)
                ax.axhline(y=4.127, color="gray", linestyle="solid", linewidth=1)
                ax.axhline(y=1.238, color="black", linestyle="dashdot", linewidth=1)
                ax.text(2021, 4.25, "Jet Fuel Baseline", fontsize=10, color="gray")
                ax.text(2021, 1.45, "RED III Target", fontsize=10, color="black")
                ax.set_title(style["label"], fontsize=14, color=style["color"])
                ax.set_ylim(ymin, ymax)
                ax.set_xlabel("Year", fontsize=14)
                ax.set_ylabel("kg CO₂-eq/kg fuel", fontsize=14)
                ax.tick_params(axis='both', labelsize=8)
                ax.grid(True)

            fig.legend(["Optimistic", "Middle", "Pessimistic"], loc="upper center", ncol=3)
            st.pyplot(fig)
app()