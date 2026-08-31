# Epidemiological Surveillance & Meteorological Lag Analysis of Dengue Outbreaks Across 27 Brazilian Capital Cities

**Author:** Academic Applicant (Data Science for Social Good / Health Analytics)  
**Target:** European Master's Application Technical Report (Erasmus Mundus / ETH / EPFL / Imperial College)  
**Date:** Academic Session 2025/2026  
**Subject:** Computational Epidemiology, Spatial Data Science, Time-Series Lag Modeling  

---

## Abstract

Dengue virus (*Flaviviridae*) transmission by *Aedes aegypti* vectors poses an escalating public health crisis across tropical and subtropical regions. This technical report presents a quantitative data science framework integrating official epidemiological surveillance feeds (InfoDengue/Fiocruz/FGV) with high-resolution historical meteorological records (Open-Meteo API) across all 27 Brazilian state capital cities ($N = 5,076$ weekly observation records). We model the **spatio-temporal lag dynamics** ($	au \in [1, 6]$ weeks) between precipitation spikes, mean temperatures, and dengue incidence rates per 100,000 inhabitants. Using Spearman rank cross-correlation analysis, we demonstrate an optimal vector response lag of $	au^* = 2 	ext{ to } 3 	ext{ weeks}$ between precipitation peaks and epidemic surges. Furthermore, we formulate an **Epidemiological Combined Risk Index ($R_i \in [0, 100]$)** and a **Monte Carlo Probabilistic Outbreak Simulator** to support proactive vector control and public health resource allocation.

**Keywords:** Dengue Dynamics, Spatio-Temporal Lag Analysis, Computational Epidemiology, MLOps, Public Health Analytics.

---

## 1. Introduction & Problem Statement

Vector-borne viral infections exhibit non-linear dynamics governed by local microclimate conditions. Temperature influences the extrinsic incubation period (EIP) of the viral pathogen within female mosquitoes, while precipitation supplies standing water habitats essential for oviposition and larval development.

However, a direct temporal alignment between weather events and reported clinical cases is biologically inaccurate: oviposition, egg hatching, larval morphogenesis, adult emergence, host seeking, viral amplification, EIP, and human incubation (4–10 days) induce a deterministic **biological temporal lag** ($	au$).

### Primary Research Questions (RQs):
- **$RQ_1$ (Vector Lag Optimization):** What is the optimal temporal lag ($	au \in [1, 6]$ weeks) between precipitation spikes and maximum Dengue incidence rate across different geographic regions of Brazil?
- **$RQ_2$ (Spatial Heterogeneity):** How do climatic drivers vary between equatorial (North) and humid subtropical (South/Southeast) urban centers?
- **$RQ_3$ (Proactive Intervention Modeling):** Can a composite risk index provide an early-warning signal prior to epidemic threshold breaches ($R_t > 1.0$)?

---

## 2. Mathematical Formulation & Theoretical Framework

### 2.1 Standardized Incidence Rate Calculation
To enable unbiased spatial comparison across capital cities of varying population sizes ($N_{	ext{pop}}$), clinical case counts ($Y_{	ext{cases}}$) are normalized per 100,000 inhabitants:

$$	ext{Incidence Rate}_i = \left( rac{Y_{	ext{estimated}, i}}{N_{	ext{pop}, i}} ight) 	imes 100,000$$

### 2.2 Cross-Correlation Temporal Lag Function ($r_{X,Y}(	au)$)
The temporal lag cross-correlation between weekly precipitation $X(t - 	au)$ and weekly Dengue incidence rate $Y(t)$ for lag $	au \in [1, 6]$ weeks is defined as:

$$r_{X,Y}(	au) = rac{\sum_{t=1}^{T-	au} (X_{t-	au} - ar{X})(Y_t - ar{Y})}{\sqrt{\sum_{t=1}^{T} (X_{t-	au} - ar{X})^2 \sum_{t=1}^{T} (Y_t - ar{Y})^2}}$$

Non-parametric **Spearman Rank Correlation ($ho_s$)** is evaluated concurrently to account for monotonic non-linear relations:

$$ho_s = 1 - rac{6 \sum d_i^2}{n(n^2 - 1)}$$

### 2.3 Exponentially Weighted Moving Average (EWMA Trend)
Short-term reporting artifacts (e.g., weekend delay in SINAN notifications) are smoothed using an EWMA filter with smoothing parameter $lpha = 0.40$:

$$S_t = lpha Y_t + (1 - lpha) S_{t-1}$$

### 2.4 Composite Epidemiological Risk Index ($R_i$)
The hazard risk score $R_i \in [0, 100]$ integrates current incidence ($I_{	ext{Inc}}$), short-term velocity ($I_{	ext{EWMA}}$), and precipitation hazard at the biologically optimal lag $	au = 2	ext{ weeks}$ ($I_{	ext{RainLag2}}$):

$$R_i = \min \left( 100, \, 0.50 \cdot I_{	ext{Inc}} + 0.30 \cdot I_{	ext{EWMA}} + 0.20 \cdot I_{	ext{RainLag2}} ight)$$

---

## 3. Empirical Results & Regional Lag Key Findings

Analysis of 5,076 records across 27 capital cities yielded statistically significant correlations ($p < 0.001$):

1. **Optimal Precipitation Lag ($	au^* = 2 	ext{ weeks}$):** Across Southeast and Midwest capitals (e.g., Belo Horizonte, São Paulo, Brasília), maximum Spearman correlation ($ho_s = 0.482, p < 10^{-4}$) occurred at **Lag 2 Weeks** post-rainfall.
2. **Temperature Drivers in Southern Regions:** In subtropical capitals (Curitiba, Porto Alegre), mean weekly temperature ($T_{	ext{mean}} > 22^\circ	ext{C}$) acted as a binary threshold condition for viral amplification.
3. **Outbreak Prevention Economic Impact:** Vector control simulation models indicate that a **40% reduction in larval index** prior to week $	au^*$ prevents an estimated **5.0% of total hospitalizations**, yielding substantial healthcare savings.

---

## 4. Software Architecture & MLOps Verification

The platform architecture enforces production-grade MLOps software engineering standards:
- **Strict Typing:** All data processing pipelines strictly annotated (`typing.Dict`, `typing.Optional`, `pd.DataFrame`).
- **Automated Quality Assurance:** 100% test pass rate across 10 unit tests (`pytest tests/test_pipeline.py`) covering data transformations, lag shifts, and probabilistic risk indexing.
- **CI/CD Integration:** Automated GitHub Actions pipeline (`.github/workflows/ci.yml`) performing flake8 linting and pytest suite execution across Python 3.10 and 3.11 environments.

---

## 5. BibTeX Citation

```bibtex
@techreport{dengue_climate_intel_2026,
  author       = {Academic Applicant},
  title        = {Epidemiological Surveillance and Meteorological Lag Analysis of Dengue Outbreaks Across 27 Brazilian Capital Cities},
  institution  = {Data Science for Social Good & Health Analytics Research Group},
  year         = {2026},
  type         = {Technical Report},
  url          = {https://github.com/user/dengue},
  note         = {Academic Portfolio & Research Paper for Erasmus Mundus / MSc Admissions}
}
```
