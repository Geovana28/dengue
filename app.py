"""
Dengue Epidemiological Surveillance & Climate Intelligence Platform
--------------------------------------------------------------------
Academic Research & Portfolio Dashboard for Monitoring Dengue Dynamics,
Spatial Risk Mapping, Vector Lag Analysis, Public Health Simulator, Bayesian Outbreak Probability,
and Viral Serotype Distribution (DENV-1 to DENV-4) across 27 Brazilian Capitals.

Author: Geovana Luiza Morais Moreira (Data Science & AI)
"""

import importlib
import os
import sys

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import main as main_module
importlib.reload(main_module)

build_national_dataset = main_module.build_national_dataset
compute_cross_correlations = main_module.compute_cross_correlations
compute_climate_lags = main_module.compute_climate_lags
calculate_combined_risk_index = main_module.calculate_combined_risk_index
simulate_public_health_intervention = main_module.simulate_public_health_intervention
compute_seasonality_matrix = main_module.compute_seasonality_matrix
generate_executive_report_text = main_module.generate_executive_report_text
calculate_outbreak_probability = main_module.calculate_outbreak_probability
run_monte_carlo_forecast = main_module.run_monte_carlo_forecast
compute_serotype_breakdown = main_module.compute_serotype_breakdown

ACCENT = "#f43f5e"
EDITORIAL_PALETTE = [
    "#f43f5e",
    "#f4f4f6",
    "#38bdf8",
    "#f59e0b",
    "#a1a1aa",
    "#14b8a6",
    "#fb7185",
    "#71717a",
    "#94a3b8",
    "#d4d4d8",
]

# Page Configuration
st.set_page_config(
    page_title="Dengue Surveillance — Climate Lag & Bayesian Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css(file_name: str = "style.css"):
    css_path = os.path.join(BASE_DIR, file_name)
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

# Dynamic Region Mapping for All 27 Brazilian Capitals
REGION_MAPPING = {
    "Southeast": ["Rio de Janeiro", "São Paulo", "Belo Horizonte", "Vitória"],
    "South": ["Curitiba", "Porto Alegre", "Florianópolis"],
    "Northeast": ["Salvador", "Fortaleza", "Recife", "São Luís", "Maceió", "Teresina", "Natal", "João Pessoa", "Aracaju"],
    "Midwest": ["Brasília", "Goiânia", "Campo Grande", "Cuiabá"],
    "North": ["Belém", "Manaus", "Porto Velho", "Macapá", "Rio Branco", "Boa Vista", "Palmas"],
}


def render_kpi_strip(items, cols=5):
    """Render unified monochrome KPI strip with zero truncation and zero pill arrows."""
    strip_cls = "kpi-strip kpi-strip-3" if cols == 3 else "kpi-strip"
    cells = []
    for label, value, meta, tone in items:
        num_cls = f"kpi-num {tone}".strip()
        cells.append(
            f'<div class="kpi-cell">'
            f'<div class="kpi-lbl">{label}</div>'
            f'<div class="{num_cls}">{value}</div>'
            f'<div class="kpi-meta">{meta}</div>'
            f'</div>'
        )
    st.markdown(f'<div class="{strip_cls}">{"".join(cells)}</div>', unsafe_allow_html=True)


def apply_dark_layout(fig, height=430, title=None, xaxis_title=None, yaxis_title=None, showlegend=True):
    """Apply consistent monochrome dark styling across all Plotly visualizations."""
    kwargs = dict(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#121215",
        font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#a1a1aa"),
        showlegend=showlegend,
        margin=dict(l=16, r=16, t=44 if title else 24, b=24),
        hoverlabel=dict(
            bgcolor="#121215",
            bordercolor="#323238",
            font=dict(color="#f4f4f6", family="JetBrains Mono, monospace", size=11),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title="",
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color="#a1a1aa"),
        ),
        xaxis=dict(showgrid=True, gridcolor="#242429", zerolinecolor="#323238", linecolor="#242429"),
        yaxis=dict(showgrid=True, gridcolor="#242429", zerolinecolor="#323238", linecolor="#242429"),
    )
    if title:
        kwargs["title"] = dict(text=title, font=dict(size=14, color="#f4f4f6"), x=0, xanchor="left")
    if xaxis_title:
        kwargs["xaxis_title"] = xaxis_title
    if yaxis_title:
        kwargs["yaxis_title"] = yaxis_title
    fig.update_layout(**kwargs)
    return fig


@st.cache_data(ttl=300)
def load_data() -> pd.DataFrame:
    """Load or fetch epidemiological and climate dataset."""
    csv_file = os.path.join(BASE_DIR, "dengue_processed_data.csv")
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        df["date"] = pd.to_datetime(df["date"])
        if "combined_risk_index" not in df.columns:
            df = calculate_combined_risk_index(df)
        if "denv1_cases" not in df.columns:
            df = compute_serotype_breakdown(df)
        return df
    df = build_national_dataset()
    if not df.empty:
        df.to_csv(csv_file, index=False)
    return df


def main():
    # Architectural Header
    st.markdown(
        """
        <div class="page-header">
            <div class="page-eyebrow"><span>INFODENGUE // BR-27</span> // CLIMATE LAG, GENOMIC SEROTYPES (DENV 1-4) & MONTE CARLO ENGINE</div>
            <h1 class="page-title">Epidemiological & Climate Intelligence Platform — Dengue Brazil</h1>
            <p class="page-subtitle">Surveillance system integrating InfoDengue alert data (Fiocruz/FGV) with meteorological time-lags (Open-Meteo) across all 27 Brazilian capitals.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()

    if df.empty:
        st.error("Failed to load dataset. Please run 'python main.py' first.")
        return

    # Academic Abstract & Research Framework Expander
    with st.expander("Academic Abstract & Mathematical Formulations", expanded=False):
        st.markdown(
            r"""
            #### **Executive Abstract**
            Dengue fever (*flavivirus* transmitted primarily by *Aedes aegypti*) represents a critical public health challenge in tropical regions.
            This platform models **spatial risk hotspots, incidence rates per 100,000 inhabitants**, **meteorological lag dynamics**, **viral serotype strains (DENV-1 to DENV-4)**, and **probabilistic outbreak forecasts** across all 27 Brazilian state capitals.

            #### **Primary Research Questions**
            - **$RQ_1$ (Vector Ecology Lag)**: *What is the optimal temporal lag ($\tau \in [1, 6]$ weeks) between precipitation spikes and peak Dengue incidence across regions?*
            - **$RQ_2$ (Serotype Co-Circulation & ADE Risk)**: *How does co-circulation of distinct strains (e.g. DENV-1 and DENV-2) impact Antibody-Dependent Enhancement (ADE) secondary infection risk?*

            #### **Mathematical Formulations**
            1. **Incidence Rate ($\text{Inc}_i$)**:
               $$\text{Incidence Rate}_i = \left( \frac{\text{Estimated Cases}_i}{\text{Population}_i} \right) \times 100,000$$

            2. **Secondary Infection ADE Risk Index ($R_{\text{ADE}}$)**:
               $$R_{\text{ADE}} = \min\left(100, \; 400 \cdot (p_{\text{DENV1}} \cdot p_{\text{DENV2}} + p_{\text{DENV1}} \cdot p_{\text{DENV3}})\right)$$

            3. **Logistic Outbreak Probability ($\mathbb{P}(\text{Outbreak})$)**:
               $$\mathbb{P}(\text{Outbreak}) = \frac{1}{1 + e^{-Z}}, \quad Z = \beta_0 + \beta_1 \bar{Y} + \beta_2 \Delta_{\text{EWMA}} + \beta_3 Z_{\text{temp}} + \beta_4 Z_{\text{precip}}$$
            """
        )

    # Sidebar Controls & Quick Filters
    st.sidebar.markdown("### 01 / Research Filters")

    region_option = st.sidebar.radio(
        "Region Filter:",
        options=["All Regions", "Southeast", "South", "Northeast", "Midwest", "North"],
        index=0,
    )

    all_cities = sorted(df["city_name"].unique())
    if region_option != "All Regions":
        default_selected = [c for c in REGION_MAPPING.get(region_option, []) if c in all_cities]
    else:
        default_selected = all_cities

    selected_cities = st.sidebar.multiselect(
        "Select Capitals:",
        options=all_cities,
        default=default_selected,
    )

    available_years = sorted(df["year"].dropna().astype(int).unique())
    selected_years = st.sidebar.multiselect(
        "Select Year(s):",
        options=available_years,
        default=available_years,
    )

    filtered_df = df[(df["city_name"].isin(selected_cities)) & (df["year"].isin(selected_years))]

    if filtered_df.empty:
        st.warning("No records match the selected filter criteria.")
        return

    # Sidebar BibTeX Citation Box
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 02 / Citation (BibTeX)")
    st.sidebar.caption("Reference entry for academic / portfolio use:")
    bibtex_text = """@misc{moreira2026dengue,
  title={Epidemiological & Climate Intelligence Platform for Dengue in Brazil},
  author={Geovana Luiza Morais Moreira},
  year={2026},
  publisher={GitHub Repository},
  url={https://github.com/Geovana28/dengue}
}"""
    st.sidebar.code(bibtex_text, language="bibtex")

    # Top KPI Strip
    total_cases = filtered_df["estimated_cases"].sum()
    avg_incidence = filtered_df["incidence_rate_per_100k"].mean()
    avg_risk = filtered_df["combined_risk_index"].mean() if "combined_risk_index" in filtered_df.columns else 0
    avg_temp = filtered_df["avg_temp_c"].dropna().mean() if "avg_temp_c" in filtered_df.columns else 0
    total_rain = filtered_df["total_precipitation_mm"].dropna().sum() if "total_precipitation_mm" in filtered_df.columns else 0

    render_kpi_strip(
        [
            ("Total Estimated Cases", f"{total_cases:,.0f}", f"{len(selected_cities)} capitals active", ""),
            ("Mean Incidence / 100k", f"{avg_incidence:.1f}", "Weekly normalized rate", "accent"),
            ("Combined Risk Index", f"{avg_risk:.1f} / 100", "Composite alert index", ""),
            ("Mean Temperature", f"{avg_temp:.1f} °C", "Open-Meteo archive", ""),
            ("Cumulative Rainfall", f"{total_rain:,.0f} mm", "Selected window", ""),
        ],
        cols=5,
    )

    # Architectural Numbered Tabs
    (
        tab_overview,
        tab_compare,
        tab_serotypes,
        tab_map,
        tab_climate,
        tab_simulator,
        tab_probability,
        tab_forecast,
        tab_bibtex,
    ) = st.tabs(
        [
            "01 / Overview",
            "02 / Capitals",
            "03 / Serotypes",
            "04 / Spatial Map",
            "05 / Climate Lags",
            "06 / Interventions",
            "07 / Monte Carlo",
            "08 / Forecast",
            "09 / Report",
        ]
    )

    # TAB 1: OVERVIEW & TRENDS
    with tab_overview:
        st.subheader("Weekly Dengue Incidence Rate per 100,000 Inhabitants")

        fig_time = px.line(
            filtered_df,
            x="date",
            y="incidence_rate_per_100k",
            color="city_name",
            labels={"incidence_rate_per_100k": "Incidence Rate (per 100k hab)", "date": "Date", "city_name": "Capital"},
            color_discrete_sequence=EDITORIAL_PALETTE,
            render_mode="svg",
        )
        fig_time.update_traces(
            line_width=2.0,
            hovertemplate="<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Incidence: <b>%{y:.1f}</b> / 100k<extra></extra>",
        )
        apply_dark_layout(fig_time, height=450)
        fig_time.update_layout(hovermode="closest")
        st.plotly_chart(fig_time, use_container_width=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.subheader("Total Estimated Cases by Capital")
            agg_city = (
                filtered_df.groupby(["city_name", "uf"])["estimated_cases"]
                .sum()
                .reset_index()
                .sort_values("estimated_cases", ascending=False)
            )
            bar_colors = [ACCENT if i < 3 else "#3f3f46" for i in range(len(agg_city))]
            fig_bar = px.bar(
                agg_city,
                x="city_name",
                y="estimated_cases",
                labels={"estimated_cases": "Estimated Cases", "city_name": "Capital"},
                text_auto=".2s",
            )
            fig_bar.update_traces(
                marker_color=bar_colors,
                textfont=dict(color="#a1a1aa", family="JetBrains Mono, monospace", size=10),
                hovertemplate="<b>%{x}</b><br>Total Cases: <b>%{y:,.0f}</b><extra></extra>",
            )
            apply_dark_layout(fig_bar, height=380, showlegend=False)
            fig_bar.update_layout(xaxis=dict(showgrid=False, tickangle=-45), margin=dict(l=10, r=10, t=24, b=60))
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_r:
            st.subheader("Alert Tier Distribution")
            alert_counts = filtered_df["alert_status"].value_counts().reset_index()
            alert_counts.columns = ["Alert Status", "Count"]

            color_map = {
                "Low Risk (Green)": "#22c55e",
                "Attention (Yellow)": "#eab308",
                "Alert (Orange)": "#f97316",
                "Epidemic (Red)": "#f43f5e",
            }
            fig_pie = px.pie(
                alert_counts,
                names="Alert Status",
                values="Count",
                color="Alert Status",
                color_discrete_map=color_map,
                hole=0.52,
            )
            fig_pie.update_traces(
                textinfo="percent+label",
                textfont=dict(color="#f4f4f6", size=11),
                hovertemplate="<b>%{label}</b><br>Weeks: <b>%{value}</b> (%{percent})<extra></extra>",
            )
            apply_dark_layout(fig_pie, height=380, showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

    # TAB 2: CAPITAL COMPARISON
    with tab_compare:
        st.subheader("Head-to-Head Capital Benchmarking")
        st.caption("Compare epidemic trajectories, climate drivers, and risk indices across selected capitals.")

        compare_cities = st.multiselect(
            "Select 2 to 4 Capitals to Compare:",
            options=all_cities,
            default=["São Paulo", "Rio de Janeiro", "Belo Horizonte"] if len(all_cities) >= 3 else all_cities[:2],
            max_selections=4,
        )

        if compare_cities:
            cmp_df = filtered_df[filtered_df["city_name"].isin(compare_cities)]

            fig_cmp_time = px.line(
                cmp_df,
                x="date",
                y="incidence_rate_per_100k",
                color="city_name",
                color_discrete_sequence=[ACCENT, "#f4f4f6", "#38bdf8", "#f59e0b"],
                labels={"incidence_rate_per_100k": "Incidence Rate (per 100k)", "date": "Date", "city_name": "Capital"},
            )
            fig_cmp_time.update_traces(line_width=2.6)
            apply_dark_layout(fig_cmp_time, height=410, title="Epidemic Curve Comparison (Incidence per 100k hab)")
            st.plotly_chart(fig_cmp_time, use_container_width=True)

            col_c1, col_c2 = st.columns(2)
            cmp_summary = (
                cmp_df.groupby("city_name")
                .agg(
                    {
                        "estimated_cases": "sum",
                        "incidence_rate_per_100k": "mean",
                        "combined_risk_index": "mean" if "combined_risk_index" in cmp_df.columns else "incidence_rate_per_100k",
                        "total_precipitation_mm": "sum",
                    }
                )
                .reset_index()
            )
            with col_c1:
                fig_cmp_bar = px.bar(
                    cmp_summary,
                    x="city_name",
                    y="combined_risk_index",
                    text_auto=".1f",
                    labels={"combined_risk_index": "Risk Index Score", "city_name": "Capital"},
                )
                fig_cmp_bar.update_traces(marker_color=ACCENT)
                apply_dark_layout(fig_cmp_bar, height=340, title="Mean Combined Risk Index (0–100)", showlegend=False)
                st.plotly_chart(fig_cmp_bar, use_container_width=True)

            with col_c2:
                fig_cmp_rain = px.bar(
                    cmp_summary,
                    x="city_name",
                    y="total_precipitation_mm",
                    text_auto=".0f",
                    labels={"total_precipitation_mm": "Rainfall (mm)", "city_name": "Capital"},
                )
                fig_cmp_rain.update_traces(marker_color="#38bdf8")
                apply_dark_layout(fig_cmp_rain, height=340, title="Total Cumulative Rainfall (mm)", showlegend=False)
                st.plotly_chart(fig_cmp_rain, use_container_width=True)
        else:
            st.info("Select at least 2 capitals to compare.")

    # TAB 3: VIRAL SEROTYPES (DENV-1 TO 4)
    with tab_serotypes:
        st.subheader("Viral Serotype Distribution (DENV-1 to DENV-4)")
        st.caption("Genomic surveillance breakdown based on Fiocruz Arbovirus Network regional proportions and ADE secondary infection risk.")

        selected_sero_city = st.selectbox("Select Capital City for Genomic Breakdown:", options=all_cities, index=0)
        sero_city_df = filtered_df[filtered_df["city_name"] == selected_sero_city].sort_values("date")

        if "denv1_cases" not in sero_city_df.columns:
            sero_city_df = compute_serotype_breakdown(sero_city_df)

        d1_tot = sero_city_df["denv1_cases"].sum()
        d2_tot = sero_city_df["denv2_cases"].sum()
        d3_tot = sero_city_df["denv3_cases"].sum()
        d4_tot = sero_city_df["denv4_cases"].sum()
        ade_risk = sero_city_df["secondary_infection_risk_index"].mean()

        render_kpi_strip(
            [
                ("Predominant Strain", "DENV-1", f"{d1_tot:,.0f} est. cases", ""),
                ("Co-Circulating Strain", "DENV-2", f"{d2_tot:,.0f} est. cases", ""),
                ("ADE Secondary Risk", f"{ade_risk:.1f} / 100", "High Co-circulation" if ade_risk > 60 else "Moderate", "accent" if ade_risk > 60 else ""),
            ],
            cols=3,
        )

        col_sg1, col_sg2 = st.columns([3, 2])

        with col_sg1:
            fig_sero_time = go.Figure()
            fig_sero_time.add_trace(go.Scatter(x=sero_city_df["date"], y=sero_city_df["denv1_cases"], stackgroup="one", name="DENV-1", line=dict(color="#38bdf8", width=1.5)))
            fig_sero_time.add_trace(go.Scatter(x=sero_city_df["date"], y=sero_city_df["denv2_cases"], stackgroup="one", name="DENV-2", line=dict(color="#f59e0b", width=1.5)))
            fig_sero_time.add_trace(go.Scatter(x=sero_city_df["date"], y=sero_city_df["denv3_cases"], stackgroup="one", name="DENV-3 (Emerging)", line=dict(color="#f97316", width=1.5)))
            fig_sero_time.add_trace(go.Scatter(x=sero_city_df["date"], y=sero_city_df["denv4_cases"], stackgroup="one", name="DENV-4", line=dict(color=ACCENT, width=1.5)))

            apply_dark_layout(
                fig_sero_time,
                height=410,
                title=f"Weekly Serotype Decomposition — {selected_sero_city}",
                xaxis_title="Date",
                yaxis_title="Estimated Cases",
            )
            st.plotly_chart(fig_sero_time, use_container_width=True)

        with col_sg2:
            sero_pie_df = pd.DataFrame(
                {"Serotype": ["DENV-1", "DENV-2", "DENV-3", "DENV-4"], "Cases": [d1_tot, d2_tot, d3_tot, d4_tot]}
            )
            fig_sero_pie = px.pie(
                sero_pie_df,
                names="Serotype",
                values="Cases",
                color="Serotype",
                color_discrete_map={"DENV-1": "#38bdf8", "DENV-2": "#f59e0b", "DENV-3": "#f97316", "DENV-4": ACCENT},
                hole=0.52,
            )
            fig_sero_pie.update_traces(
                textinfo="percent+label",
                textfont=dict(color="#f4f4f6", size=11),
                hovertemplate="<b>%{label}</b><br>Cases: <b>%{value:,.0f}</b> (%{percent})<extra></extra>",
            )
            apply_dark_layout(fig_sero_pie, height=410, title=f"Serotype Share — {selected_sero_city}", showlegend=False)
            st.plotly_chart(fig_sero_pie, use_container_width=True)

        st.markdown(
            """
            <div class="ref-panel">
                <h4>Genomic & Immunological Rationale (ADE Phenomenon)</h4>
                <ul>
                    <li><b>Primary Infection:</b> Infection by a single serotype (e.g. DENV-1) grants lifelong homotypic immunity against that strain.</li>
                    <li><b>Secondary Infection (ADE Risk):</b> Sequential infection by a distinct strain (e.g. DENV-2 after DENV-1) can trigger <i>Antibody-Dependent Enhancement (ADE)</i>, raising the risk of Severe Dengue.</li>
                    <li><b>DENV-3 Reintroduction:</b> Renewed circulation after ~15 years of low prevalence exposes a large immunologically naive population.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # TAB 4: SPATIAL MAP
    with tab_map:
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.subheader("Spatial Distribution of Dengue Risk Across Brazilian Capitals")
            st.caption("Marker area scales with mean Incidence Rate per 100k hab; color encodes Alert Status.")
        with col_m2:
            map_style_opt = st.selectbox(
                "Map Base Layer:",
                options=["carto-darkmatter", "carto-positron", "open-street-map"],
                index=0,
                format_func=lambda x: {
                    "carto-darkmatter": "Carto Dark Matter",
                    "carto-positron": "Carto Positron Light",
                    "open-street-map": "OpenStreetMap",
                }.get(x, x),
            )

        if "combined_risk_index" not in filtered_df.columns:
            filtered_df = calculate_combined_risk_index(filtered_df)

        agg_dict = {
            "incidence_rate_per_100k": "mean",
            "estimated_cases": "sum",
            "alert_status": lambda x: x.mode()[0] if not x.empty else "Unknown",
        }
        if "combined_risk_index" in filtered_df.columns:
            agg_dict["combined_risk_index"] = "mean"

        map_data = filtered_df.groupby(["city_name", "uf", "lat", "lon"]).agg(agg_dict).reset_index()
        if "combined_risk_index" not in map_data.columns:
            map_data["combined_risk_index"] = map_data["incidence_rate_per_100k"]

        scatter_fn = getattr(px, "scatter_map", None) or getattr(px, "scatter_mapbox")
        map_kwargs = {
            "lat": "lat",
            "lon": "lon",
            "size": "incidence_rate_per_100k",
            "color": "alert_status",
            "color_discrete_map": {
                "Low Risk (Green)": "#22c55e",
                "Attention (Yellow)": "#eab308",
                "Alert (Orange)": "#f97316",
                "Epidemic (Red)": "#f43f5e",
            },
            "hover_name": "city_name",
            "custom_data": ["uf", "incidence_rate_per_100k", "estimated_cases", "combined_risk_index"],
            "zoom": 3.5,
            "center": {"lat": -14.2350, "lon": -51.9253},
            "size_max": 32,
            "template": "plotly_dark",
        }
        if hasattr(px, "scatter_map"):
            map_kwargs["map_style"] = map_style_opt
        else:
            map_kwargs["mapbox_style"] = map_style_opt

        fig_map = scatter_fn(map_data, **map_kwargs)
        fig_map.update_traces(
            marker=dict(opacity=0.85),
            hovertemplate="<b>%{hovertext} (%{customdata[0]})</b><br>Mean Incidence: <b>%{customdata[1]:.1f}</b> / 100k<br>Total Cases: <b>%{customdata[2]:,.0f}</b><br>Risk Index: <b>%{customdata[3]:.1f} / 100</b><extra></extra>",
        )
        fig_map.update_layout(
            height=580,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#121215",
            font=dict(family="Inter, sans-serif", size=12, color="#a1a1aa"),
            margin=dict(l=0, r=0, t=12, b=0),
            legend=dict(title="Risk Status", orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # TAB 5: CLIMATE CORRELATIONS & SEASONALITY
    with tab_climate:
        st.subheader("Meteorological Lag Analysis & Seasonality Matrix")
        st.caption("Pearson and Spearman cross-correlations across 1–6 week temporal lags and monthly transmission seasonality.")

        season_matrix = compute_seasonality_matrix(filtered_df)
        if not season_matrix.empty:
            rose_dark_scale = [
                [0.0, "#121215"],
                [0.25, "#3f1d28"],
                [0.55, "#9f1239"],
                [0.8, "#f43f5e"],
                [1.0, "#fda4af"],
            ]
            fig_season = px.imshow(
                season_matrix,
                text_auto=True,
                color_continuous_scale=rose_dark_scale,
                labels={"color": "Mean Incidence / 100k"},
                aspect="auto",
            )
            apply_dark_layout(fig_season, height=500, title="Epidemiological Seasonality Heatmap (Month vs State Capital)", showlegend=False)
            st.plotly_chart(fig_season, use_container_width=True)

        corr_matrix = compute_cross_correlations(filtered_df, max_lag_weeks=6)
        if not corr_matrix.empty:
            col_lag1, col_lag2 = st.columns([1, 1])
            with col_lag1:
                fig_lag = px.bar(
                    corr_matrix,
                    x="Lag_Weeks",
                    y="Spearman_rho",
                    color="Variable",
                    barmode="group",
                    text_auto=True,
                    labels={"Lag_Weeks": "Lag (Weeks)", "Spearman_rho": "Spearman Correlation (ρ)"},
                    color_discrete_map={"Precipitation": "#38bdf8", "Temperature": ACCENT},
                )
                apply_dark_layout(fig_lag, height=370, title="Cross-Correlation Coefficient vs Temporal Lag (Weeks)")
                st.plotly_chart(fig_lag, use_container_width=True)

            with col_lag2:
                st.markdown(
                    """
                    <div class="ref-panel" style="margin-top:0;">
                        <h4>Biological Vector Lag Mechanism</h4>
                        <ul>
                            <li><b>Lag 0–1 Week:</b> Heavy rainfall temporarily flushes outdoor containers, briefly suppressing larvae.</li>
                            <li><b>Lag 2–4 Weeks (Peak Window):</b> Standing water supports <i>Aedes aegypti</i> egg hatching, larval maturation (7–10 days), and extrinsic viral incubation (8–12 days).</li>
                            <li><b>Observed Signal:</b> Incidence rates reach peak correlation with rainfall occurring <b>2 to 4 weeks prior</b>.</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            fig_temp = px.scatter(
                filtered_df,
                x="avg_temp_c",
                y="incidence_rate_per_100k",
                color="city_name",
                trendline="ols",
                labels={"avg_temp_c": "Avg Temperature (°C)", "incidence_rate_per_100k": "Incidence Rate (per 100k)"},
                color_discrete_sequence=EDITORIAL_PALETTE,
            )
            fig_temp.update_traces(
                marker=dict(size=6, opacity=0.65, line=dict(width=0.4, color="#242429")),
                hovertemplate="<b>%{fullData.name}</b><br>Temp: <b>%{x:.1f}°C</b><br>Incidence: <b>%{y:.1f}</b><extra></extra>",
            )
            apply_dark_layout(fig_temp, height=400, title="Mean Temperature (°C) vs Dengue Incidence", showlegend=False)
            st.plotly_chart(fig_temp, use_container_width=True)

        with col_c2:
            rain_col = "precipitation_lag_2w" if "precipitation_lag_2w" in filtered_df.columns else "total_precipitation_mm"
            fig_rain = px.scatter(
                filtered_df,
                x=rain_col,
                y="incidence_rate_per_100k",
                color="city_name",
                trendline="ols",
                labels={rain_col: "Rainfall 2-Wk Lag (mm)", "incidence_rate_per_100k": "Incidence Rate (per 100k)"},
                color_discrete_sequence=EDITORIAL_PALETTE,
            )
            fig_rain.update_traces(
                marker=dict(size=6, opacity=0.65, line=dict(width=0.4, color="#242429")),
                hovertemplate="<b>%{fullData.name}</b><br>Rainfall (Lag 2w): <b>%{x:.1f} mm</b><br>Incidence: <b>%{y:.1f}</b><extra></extra>",
            )
            apply_dark_layout(fig_rain, height=400, title="Rainfall (Lag 2 Weeks) vs Dengue Incidence", showlegend=False)
            st.plotly_chart(fig_rain, use_container_width=True)

    # TAB 6: PUBLIC HEALTH INTERVENTION SIMULATOR
    with tab_simulator:
        st.subheader("Public Health Vector Control Campaign Simulator")
        st.caption("Simulate the impact of breeding site eradication and larvicide spraying on cases and SUS hospital costs.")

        col_sim_controls, col_sim_kpis = st.columns([1, 2])

        with col_sim_controls:
            sim_city = st.selectbox("Target Capital City:", options=all_cities, index=0)
            vec_reduction = (
                st.slider(
                    "Mosquito Density Reduction Efficacy (%):",
                    min_value=5,
                    max_value=80,
                    value=30,
                    step=5,
                    help="Estimated reduction percentage in vector breeding sites after intervention.",
                )
                / 100.0
            )
            city_sim_df = filtered_df[filtered_df["city_name"] == sim_city].copy()
            sim_res = simulate_public_health_intervention(city_sim_df, vector_reduction_pct=vec_reduction)

        with col_sim_kpis:
            render_kpi_strip(
                [
                    ("Cases Averted", f"{sim_res['cases_averted']:,.0f}", f"-{vec_reduction * 85.0:.1f}% transmission", "positive"),
                    ("Hospitalizations Prevented", f"{sim_res['hospitalizations_prevented']:,.0f}", "5.0% severe rate", ""),
                    ("SUS Cost Saved", f"R$ {sim_res['financial_savings_brl']:,.0f}", "R$ 1,500 / bed", "accent"),
                ],
                cols=3,
            )

        if not sim_res["df"].empty:
            sim_out_df = sim_res["df"].sort_values("date")
            fig_sim_chart = go.Figure()
            fig_sim_chart.add_trace(
                go.Scatter(
                    x=sim_out_df["date"],
                    y=sim_out_df["estimated_cases"],
                    mode="lines",
                    name="Baseline (No Intervention)",
                    line=dict(color=ACCENT, width=2.6),
                )
            )
            fig_sim_chart.add_trace(
                go.Scatter(
                    x=sim_out_df["date"],
                    y=sim_out_df["simulated_cases"],
                    mode="lines",
                    name=f"Projected ({int(vec_reduction * 100)}% Vector Control)",
                    line=dict(color="#22c55e", width=2.4, dash="dash"),
                )
            )
            apply_dark_layout(
                fig_sim_chart,
                height=430,
                title=f"Baseline vs Vector Control Trajectory — {sim_city}",
                xaxis_title="Date",
                yaxis_title="Estimated Cases",
            )
            st.plotly_chart(fig_sim_chart, use_container_width=True)

    # TAB 7: PROBABILISTIC MODEL & MONTE CARLO FORECAST
    with tab_probability:
        st.subheader("Probabilistic Outbreak Risk & Monte Carlo Simulation (1,000 Runs)")
        st.caption("Bayesian/Logistic Outbreak Probability Model and 52-week stochastic projection with 95% confidence band.")

        prob_city = st.selectbox("Select Capital City for Probabilistic Forecasting:", options=all_cities, index=0)
        city_prob_df = filtered_df[filtered_df["city_name"] == prob_city].sort_values("date")

        prob_res = calculate_outbreak_probability(city_prob_df)
        mc_res_df = run_monte_carlo_forecast(city_prob_df, num_simulations=1000, forecast_weeks=52)

        col_pr1, col_pr2 = st.columns([1, 1])

        with col_pr1:
            p_val = prob_res["probability_pct"]
            fig_gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=p_val,
                    number={"suffix": "%", "font": {"size": 40, "color": "#f4f4f6", "family": "JetBrains Mono, monospace"}},
                    title={"text": f"{prob_city} — Outbreak Probability ({prob_res['risk_tier']})", "font": {"size": 13, "color": "#a1a1aa"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#52525b", "tickfont": {"color": "#71717a"}},
                        "bar": {"color": ACCENT},
                        "bgcolor": "#121215",
                        "borderwidth": 1,
                        "bordercolor": "#242429",
                        "steps": [
                            {"range": [0, 25], "color": "#14241e"},
                            {"range": [25, 50], "color": "#262315"},
                            {"range": [50, 75], "color": "#2c1d14"},
                            {"range": [75, 100], "color": "#33141c"},
                        ],
                        "threshold": {
                            "line": {"color": "#f4f4f6", "width": 3},
                            "thickness": 0.75,
                            "value": p_val,
                        },
                    },
                )
            )
            fig_gauge.update_layout(
                height=310,
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", color="#a1a1aa"),
                margin=dict(l=20, r=20, t=40, b=16),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_pr2:
            st.markdown(
                f"""
                <div class="ref-panel" style="margin-top:24px;">
                    <h4>Statistical Verdict & Model Rationale</h4>
                    <p><b>Calculated Outbreak Tier:</b> {prob_res['risk_tier']}</p>
                    <p><b>Logit Z-Score:</b> <code>{prob_res['logit_z']}</code></p>
                    <p style="margin-bottom:0;"><b>Rationale:</b> {prob_res['reasoning']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if not mc_res_df.empty:
            fig_mc = go.Figure()
            fig_mc.add_trace(
                go.Scatter(
                    x=mc_res_df["date"],
                    y=mc_res_df["p95_pessimistic"],
                    mode="lines",
                    name="P95 Upper Bound (95% CI)",
                    line=dict(color="rgba(244, 63, 94, 0.55)", width=1.4, dash="dot"),
                )
            )
            fig_mc.add_trace(
                go.Scatter(
                    x=mc_res_df["date"],
                    y=mc_res_df["p5_optimistic"],
                    mode="lines",
                    name="P5 Lower Bound (95% CI)",
                    fill="tonexty",
                    fillcolor="rgba(244, 63, 94, 0.12)",
                    line=dict(color="rgba(161, 161, 170, 0.45)", width=1.4, dash="dot"),
                )
            )
            fig_mc.add_trace(
                go.Scatter(
                    x=mc_res_df["date"],
                    y=mc_res_df["p50_median"],
                    mode="lines+markers",
                    name="P50 Expected Median",
                    line=dict(color=ACCENT, width=2.6),
                    marker=dict(size=4),
                )
            )
            apply_dark_layout(
                fig_mc,
                height=440,
                title=f"Monte Carlo 1,000-Run Stochastic Projection (52 Weeks) — {prob_city}",
                xaxis_title="Future Date (1 Year Ahead)",
                yaxis_title="Projected Incidence Rate (per 100k hab)",
            )
            st.plotly_chart(fig_mc, use_container_width=True)

        st.markdown("##### National State Capital Outbreak Probability Ranking")
        prob_records = []
        for city in all_cities:
            c_df = filtered_df[filtered_df["city_name"] == city]
            c_prob = calculate_outbreak_probability(c_df)
            prob_records.append(
                {
                    "Capital": city,
                    "Outbreak Probability (%)": c_prob["probability_pct"],
                    "Risk Tier": c_prob["risk_tier"],
                    "Logit Z": c_prob["logit_z"],
                }
            )
        prob_rank_df = pd.DataFrame(prob_records).sort_values("Outbreak Probability (%)", ascending=False).reset_index(drop=True)
        st.dataframe(prob_rank_df, use_container_width=True, hide_index=True)

    # TAB 8: FORECASTING
    with tab_forecast:
        st.subheader("Outbreak Trend Projection — Short-Term EWMA")
        st.caption("Exponentially Weighted Moving Average (4-week span) and 6-week short-term incidence projection.")

        selected_forecast_city = st.selectbox("Select Capital City for EWMA Forecasting:", options=all_cities)
        city_df = filtered_df[filtered_df["city_name"] == selected_forecast_city].sort_values("date")

        if len(city_df) >= 10:
            city_df["trend_forecast"] = city_df["incidence_rate_per_100k"].ewm(span=4).mean()
            last_date = city_df["date"].max()
            future_dates = [last_date + pd.Timedelta(weeks=i) for i in range(1, 7)]
            last_val = city_df["trend_forecast"].iloc[-1]
            trend_delta = (city_df["trend_forecast"].iloc[-1] - city_df["trend_forecast"].iloc[-4]) / 4

            future_vals = [max(0, last_val + trend_delta * i) for i in range(1, 7)]
            future_df = pd.DataFrame({"date": future_dates, "forecast_incidence": future_vals})

            fig_fc = go.Figure()
            fig_fc.add_trace(
                go.Scatter(
                    x=city_df["date"],
                    y=city_df["incidence_rate_per_100k"],
                    mode="lines+markers",
                    name="Observed Incidence",
                    line=dict(color="#f4f4f6", width=2.0),
                    marker=dict(size=4),
                )
            )
            fig_fc.add_trace(
                go.Scatter(
                    x=city_df["date"],
                    y=city_df["trend_forecast"],
                    mode="lines",
                    name="EWMA Trend (4-Week)",
                    line=dict(color="#71717a", width=2.0, dash="dash"),
                )
            )
            fig_fc.add_trace(
                go.Scatter(
                    x=future_df["date"],
                    y=future_df["forecast_incidence"],
                    mode="lines+markers",
                    name="6-Week Projection",
                    line=dict(color=ACCENT, width=3.0),
                    marker=dict(size=7, symbol="diamond"),
                )
            )
            apply_dark_layout(
                fig_fc,
                height=440,
                title=f"Short-Term Incidence Forecast — {selected_forecast_city}",
                xaxis_title="Date",
                yaxis_title="Incidence Rate (per 100k hab)",
            )
            st.plotly_chart(fig_fc, use_container_width=True)
        else:
            st.info("Insufficient historical data points for forecasting.")

    # TAB 9: ACADEMIC PAPER & EXPORT
    with tab_bibtex:
        st.subheader("Technical Report & Research Data Export")

        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            st.markdown(
                """
                <div class="ref-panel" style="margin-top:0;">
                    <h4>Technical Report Summary</h4>
                    <ul>
                        <li><b>Project Title:</b> Epidemiological & Climate Intelligence Surveillance Platform for Dengue in Brazil</li>
                        <li><b>Methodologies:</b> Time-series resampling, Pearson & Spearman lag cross-correlation, EWMA forecasting, GIS hotspot mapping, intervention cost simulation, Bayesian logistic outbreak risk, 1,000-run Monte Carlo projection, and DENV 1–4 genomic decomposition.</li>
                        <li><b>Data Sources:</b> InfoDengue API (Fiocruz/FGV), Open-Meteo Historical Archive, Fiocruz Arbovirus Network, and IBGE Census.</li>
                        <li><b>Engineering:</b> Automated GitHub Actions ingestion pipeline and unit test coverage with <code>pytest</code>.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_p2:
            st.markdown("##### Export Artifacts")
            exec_report_text = generate_executive_report_text(filtered_df)
            st.download_button(
                label="Download Executive Report (Markdown)",
                data=exec_report_text.encode("utf-8"),
                file_name="executive_dengue_surveillance_report.md",
                mime="text/markdown",
            )
            csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Processed Dataset (CSV)",
                data=csv_bytes,
                file_name="dengue_climate_processed_data.csv",
                mime="text/csv",
            )
            json_bytes = filtered_df.to_json(orient="records", date_format="iso").encode("utf-8")
            st.download_button(
                label="Export Dataset (JSON)",
                data=json_bytes,
                file_name="dengue_climate_processed_data.json",
                mime="application/json",
            )

    # Data Explorer Footer
    st.markdown("---")
    st.subheader("Consolidated Dataset Explorer")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
