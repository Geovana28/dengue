# 📖 Data Dictionary & API Schema Definition

This document outlines the data schema, variable types, transformations, and definitions used in the **Dengue Epidemiological & Climate Surveillance Platform**.

---

## 📊 Dataset Fields (`dengue_processed_data.csv`)

| Field Name | Type | Description | Source / Formula |
| :--- | :--- | :--- | :--- |
| `date` | `Datetime` | Start date of the Epidemiological Week (SE) | Converted from `data_iniSE` timestamp (ms) |
| `year` | `Integer` | Year of notification | Extracted from `date` |
| `month` | `Integer` | Month of notification (1-12) | Extracted from `date` |
| `epidemiological_week` | `Integer` | Standard Epidemiological Week (1-52) | InfoDengue API (`SE`) |
| `city_name` | `String` | Name of the state capital | IBGE Metadata mapping |
| `uf` | `String` | Brazilian Federation Unit (State code) | IBGE Metadata mapping |
| `population` | `Integer` | IBGE estimated city population | IBGE 2022 Census Metrics |
| `lat` | `Float` | Latitude coordinate of the capital | WGS84 GIS |
| `lon` | `Float` | Longitude coordinate of the capital | WGS84 GIS |
| `notified_cases` | `Integer` | Total cases reported to SINAN | InfoDengue API (`casos`) |
| `estimated_cases` | `Integer` | Nowcasted estimated total cases | InfoDengue API (`casos_est`) |
| `incidence_rate_per_100k` | `Float` | **Incidence Rate per 100k inhabitants** | `(estimated_cases / population) * 100,000` |
| `combined_risk_index` | `Float` | **Epidemiological Combined Risk Index (0-100)** | `0.5*Incidence + 0.3*EWMA + 0.2*RainLag2` |
| `avg_temp_c` | `Float` | Weekly mean 2m air temperature (°C) | Open-Meteo Archive API |
| `total_precipitation_mm` | `Float` | Weekly total precipitation sum (mm) | Open-Meteo Archive API |
| `precipitation_lag_1w..6w` | `Float` | Precipitation lagged by 1 to 6 weeks | Time-series shift per city |
| `temp_lag_1w..6w` | `Float` | Temperature lagged by 1 to 6 weeks | Time-series shift per city |
| `alert_level` | `Integer` | Numeric risk level (1 to 4) | InfoDengue API (`nivel`) |
| `alert_status` | `String` | Human-readable alert label | Categorical mapping |

---

## 🚦 Alert Level Mapping

- **Level 1 (`Low Risk (Green)`)**: Normal transmission rates within historical confidence intervals.
- **Level 2 (`Attention (Yellow)`)**: Favorable climate conditions (temperature/humidity) for Aedes aegypti breeding.
- **Level 3 (`Alert (Orange)`)**: Statistically significant rise in dengue cases.
- **Level 4 (`Epidemic (Red)`)**: Outbreak threshold crossed; emergency public health response required.
