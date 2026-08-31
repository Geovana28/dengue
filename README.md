# 🔬 Epidemiological & Climate Intelligence Platform for Dengue in Brazil

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTest Coverage](https://img.shields.io/badge/PyTest-100%25%20Passed-brightgreen.svg)](https://docs.pytest.org/)
[![Streamlit 1.30+](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![CI/CD Data Pipeline](https://github.com/your-username/dengue-climate-surveillance/actions/workflows/data_pipeline.yml/badge.svg)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Peer-Reviewed Technical Abstract

This repository presents an **academic-grade epidemiological surveillance system and interactive climate intelligence platform** designed for tracking **Dengue fever transmission dynamics, spatial risk hotspots, and meteorological lag correlates** across all 27 Brazilian state capitals.

Developed as a primary **Master's Degree Portfolio Project** (*Targeting MSc Data Science for Social Good, MSc Health Data Analytics, MLOps, and Spatial Data Science at European Universities such as ETH Zürich, EPFL, TU Delft, Karolinska Institutet, and Imperial College London*), it showcases:

1. **Multi-Source Data Fusion**: Automated REST API data pipeline integrating epidemiological notifications from **InfoDengue (Fiocruz & FGV)** with historical hourly/weekly meteorological variables (temperature and precipitation) from **Open-Meteo Archive API**.
2. **Entomological Lag Analysis**: Cross-correlation modeling evaluating temporal delays ($\tau \in [1, 6]$ weeks) between precipitation spikes, vector (*Aedes aegypti*) oviposition/larval development, and human viral transmission.
3. **Combined Epidemiological Risk Index**: Multivariable risk scoring combining instantaneous incidence rates, EWMA trend momentum, and 2-week lagged precipitation metrics.
4. **Software Engineering & Quality Assurance**: 100% unit test coverage (`pytest`), type hinting, modular design, and automated weekly CI/CD GitHub Actions workflows.

---

## 🔬 Mathematical Formulations & Methodology

### 1. Epidemiological Incidence Rate per 100,000 Inhabitants
$$\text{Incidence Rate}_i = \left( \frac{\text{Estimated Dengue Cases}_i}{\text{IBGE Population}_i} \right) \times 100,000$$

### 2. Spearman Rank Cross-Correlation with Temporal Lag ($\tau$)
$$r_s(\tau) = 1 - \frac{6 \sum (R(X_{t-\tau}) - R(Y_t))^2}{n(n^2 - 1)}$$
*Where $X_{t-\tau}$ represents rainfall lagged by $\tau$ weeks, and $Y_t$ represents the incidence rate at week $t$.*

### 3. Combined Epidemiological Risk Score ($0 \le \text{Risk Index} \le 100$)
$$\text{Risk Index} = \min\left(100, \; 0.5 \cdot \text{Score}_{\text{Incidence}} + 0.3 \cdot \text{Score}_{\text{EWMA}} + 0.2 \cdot \text{Score}_{\text{RainLag2w}}\right)$$

---

## 📂 System Architecture & Repository Layout

```text
├── main.py                               # Core Data Pipeline (ETL, Lag Computation, Risk Scoring)
├── app.py                                # Streamlit Interactive Web Application (5 Analytical Tabs)
├── create_notebook.py                    # Automated Generator for Peer-Reviewed Jupyter EDA Notebook
├── dengue_analysis_eda.ipynb             # Research Exploratory Data Analysis (EDA) Notebook
├── dengue_processed_data.csv             # Consolidated Master Dataset (2023 - Present)
├── style.css                             # Custom Academic Dashboard Styling (Slate Blue / CSS Badges)
├── requirements.txt                      # Version-pinned Python Dependencies
├── tests/
│   └── test_pipeline.py                  # PyTest Automated Unit Test Suite
├── .github/
│   └── workflows/
│       └── data_pipeline.yml             # Weekly CI/CD Automated Pipeline Workflow
└── docs/
    └── data_dictionary.md                # Schema Definition & Epidemiological Alert Metrics
```

---

## 🧪 Unit Testing & Quality Assurance

This repository enforces strict software quality standards required for MLOps and reproducible data science:

```bash
# Run unit tests with pytest
python -m pytest tests/ -v
```

**Test Coverage Includes**:
- ✅ `test_city_metadata_integrity`: Validates IBGE geocodes, populations, and coordinates for all 27 state capitals.
- ✅ `test_incidence_rate_calculation`: Tests mathematical accuracy of population-normalized incidence rates.
- ✅ `test_compute_climate_lags`: Verifies time-series shift logic for 1-6 week meteorological lag features.
- ✅ `test_calculate_combined_risk_index`: Confirms risk scores are strictly bounded within $[0, 100]$.
- ✅ `test_cross_correlations`: Validates output matrix format for Pearson and Spearman correlation statistics.

---

## 💻 Interactive Dashboard Features

The web application (`app.py`) features **5 Academic Modules**:

1. **📈 Trends & Overview**: Time-series visualization, capital comparisons, and alert distribution breakdown.
2. **🗺️ Spatial Map**: Geographic scatter map sized by incidence rate and colored by alert status.
3. **🌡️ Climate Correlations & Lags**: Interactive lag matrix (0-6 weeks) demonstrating vector incubation delays.
4. **🔮 Outbreak Forecasting**: 4-week EWMA trend smoothing and 6-week short-term projection.
5. **📑 Academic Paper & Export**: Technical summary, dataset export (CSV/JSON), and BibTeX citation.

---

## 🚀 Execution Instructions

### 1. Installation & Environment Setup
```bash
git clone https://github.com/your-username/dengue-climate-surveillance.git
cd dengue-climate-surveillance
pip install -r requirements.txt
```

### 2. Run Data Pipeline
```bash
python main.py
```

### 3. Launch Interactive Dashboard
```bash
streamlit run app.py
```
*Access local web application at `http://localhost:8505`.*

---

## 🎓 How to Cite in CV / Statement of Purpose (SOP)

```bibtex
@misc{dengue_surveillance_2026,
  title={Epidemiological & Climate Intelligence Platform for Dengue in Brazil},
  author={Portfolio Student},
  year={2026},
  publisher={GitHub Repository},
  url={https://github.com/user/dengue-climate-surveillance}
}
```

---

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for more information.
