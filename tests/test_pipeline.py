import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Unit Test Suite - Dengue Epidemiological Data Pipeline
-------------------------------------------------------
Academic Quality Assurance Tests for Master's Application Portfolio.
Verifies data transformation, incidence calculation, lag features, and risk scoring.
"""

import pytest
import pandas as pd
import numpy as np

from main import (
    CITY_METADATA,
    transform_epidemiological_data,
    compute_climate_lags,
    compute_cross_correlations,
    calculate_combined_risk_index,
)


def test_city_metadata_integrity():
    """Verify that all 27 Brazilian state capitals are configured with valid metadata."""
    assert len(CITY_METADATA) == 27, "Must contain exactly 27 state capitals."
    
    for geocode, meta in CITY_METADATA.items():
        assert "name" in meta and len(meta["name"]) > 0
        assert "uf" in meta and len(meta["uf"]) == 2
        assert "population" in meta and meta["population"] > 0
        assert -35.0 <= meta["lat"] <= 10.0, f"Invalid latitude for {meta['name']}"
        assert -75.0 <= meta["lon"] <= -30.0, f"Invalid longitude for {meta['name']}"


def test_incidence_rate_calculation():
    """Test incidence rate per 100,000 inhabitants formula: (cases / pop) * 100,000."""
    sample_raw = pd.DataFrame({
        "data_iniSE": [1672531200000], # Timestamp ms
        "SE": [202301],
        "casos_est": [500],
        "casos": [450],
        "nivel": [2],
    })
    
    city_info = {"name": "Test City", "uf": "TC", "population": 1000000, "lat": -20.0, "lon": -40.0}
    transformed = transform_epidemiological_data(sample_raw, city_info)
    
    assert not transformed.empty
    expected_incidence = (500 / 1000000) * 100000 # 50.0
    assert transformed["incidence_rate_per_100k"].iloc[0] == expected_incidence
    assert transformed["alert_status"].iloc[0] == "Attention (Yellow)"


def test_compute_climate_lags():
    """Test that temporal lag columns are generated correctly for weekly series."""
    dates = pd.date_range("2023-01-01", periods=10, freq="W-MON")
    df = pd.DataFrame({
        "city_name": ["City A"] * 10,
        "date": dates,
        "total_precipitation_mm": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
        "avg_temp_c": [25.0] * 10,
        "incidence_rate_per_100k": [5.0] * 10,
    })
    
    lagged = compute_climate_lags(df, max_lag_weeks=3)
    
    assert "precipitation_lag_1w" in lagged.columns
    assert "precipitation_lag_2w" in lagged.columns
    assert "precipitation_lag_3w" in lagged.columns
    
    # Check shift logic: value at index 2 (week 3) for lag_2w should equal week 1 precipitation (10.0)
    assert lagged["precipitation_lag_2w"].iloc[2] == 10.0
    assert lagged["precipitation_lag_1w"].iloc[2] == 20.0


def test_calculate_combined_risk_index():
    """Test that combined epidemiological risk score is bounded within [0, 100]."""
    df = pd.DataFrame({
        "city_name": ["City A", "City B"],
        "date": pd.to_datetime(["2023-01-01", "2023-01-01"]),
        "incidence_rate_per_100k": [150.0, 450.0], # Normal vs High
        "precipitation_lag_2w": [20.0, 150.0],
    })
    
    scored = calculate_combined_risk_index(df)
    
    assert "combined_risk_index" in scored.columns
    assert scored["combined_risk_index"].min() >= 0.0
    assert scored["combined_risk_index"].max() <= 100.0
    # City B has higher incidence and rainfall, so its score must be higher
    assert scored["combined_risk_index"].iloc[1] > scored["combined_risk_index"].iloc[0]


def test_cross_correlations():
    """Test cross-correlation calculation output format."""
    dates = pd.date_range("2023-01-01", periods=15, freq="W-MON")
    df = pd.DataFrame({
        "city_name": ["City A"] * 15,
        "date": dates,
        "incidence_rate_per_100k": np.linspace(10, 100, 15),
        "total_precipitation_mm": np.linspace(5, 50, 15),
        "avg_temp_c": [28.0] * 15,
    })
    
    df = compute_climate_lags(df, max_lag_weeks=2)
    corr_df = compute_cross_correlations(df, max_lag_weeks=2)
    
    assert not corr_df.empty
    assert "Variable" in corr_df.columns
    assert "Pearson_r" in corr_df.columns
    assert "Spearman_rho" in corr_df.columns


def test_simulate_public_health_intervention():
    """Test public health intervention simulator math and economic savings."""
    from main import simulate_public_health_intervention
    
    df = pd.DataFrame({
        "city_name": ["City A"] * 5,
        "estimated_cases": [1000, 2000, 3000, 4000, 5000],
        "population": [100000] * 5,
    })
    
    res = simulate_public_health_intervention(df, vector_reduction_pct=0.4)
    
    assert res["original_cases"] == 15000
    assert res["simulated_cases"] < 15000
    assert res["cases_averted"] > 0
    assert res["hospitalizations_prevented"] == int(round(res["cases_averted"] * 0.05))
    assert res["financial_savings_brl"] == res["hospitalizations_prevented"] * 1500.0


def test_compute_seasonality_matrix():
    """Test 2D city vs month seasonality pivot matrix format."""
    from main import compute_seasonality_matrix
    
    df = pd.DataFrame({
        "city_name": ["City A", "City A", "City B"],
        "month": [1, 2, 1],
        "incidence_rate_per_100k": [10.0, 20.0, 30.0],
    })
    
    matrix = compute_seasonality_matrix(df)
    assert not matrix.empty
    assert "Jan" in matrix.columns
    assert "Feb" in matrix.columns


def test_calculate_outbreak_probability():
    """Test probabilistic outbreak model logit calculation and risk tier categorization."""
    from main import calculate_outbreak_probability
    
    dates = pd.date_range("2023-01-01", periods=10, freq="W-MON")
    df = pd.DataFrame({
        "city_name": ["City A"] * 10,
        "date": dates,
        "incidence_rate_per_100k": [10.0, 20.0, 50.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0],
        "avg_temp_c": [25.0 + i*0.5 for i in range(10)],
        "total_precipitation_mm": [10.0 + i*5 for i in range(10)],
    })
    
    res = calculate_outbreak_probability(df)
    assert "probability_pct" in res
    assert 0.0 <= res["probability_pct"] <= 100.0
    assert "risk_tier" in res
    assert "Critical" in res["risk_tier"] or "High" in res["risk_tier"]


def test_run_monte_carlo_forecast():
    """Test Monte Carlo 1,000 run simulation confidence interval generation."""
    from main import run_monte_carlo_forecast
    
    dates = pd.date_range("2023-01-01", periods=15, freq="W-MON")
    df = pd.DataFrame({
        "city_name": ["City A"] * 15,
        "date": dates,
        "incidence_rate_per_100k": np.linspace(10, 150, 15),
    })
    
    mc_df = run_monte_carlo_forecast(df, num_simulations=100, forecast_weeks=12)
    assert not mc_df.empty
    assert "p5_optimistic" in mc_df.columns
    assert "p50_median" in mc_df.columns
    assert "p95_pessimistic" in mc_df.columns
    assert len(mc_df) == 12
    # P95 pessimistic scenario should be >= P5 optimistic scenario
    assert (mc_df["p95_pessimistic"] >= mc_df["p5_optimistic"]).all()


def test_compute_serotype_breakdown():
    """Test serotype strain breakdown math and secondary infection ADE risk calculation."""
    from main import compute_serotype_breakdown
    
    df = pd.DataFrame({
        "city_name": ["Belo Horizonte", "São Paulo"],
        "estimated_cases": [10000, 20000],
        "population": [2300000, 11000000],
        "incidence_rate_per_100k": [434.78, 181.82],
    })
    
    sero_df = compute_serotype_breakdown(df)
    assert "denv1_cases" in sero_df.columns
    assert "denv2_cases" in sero_df.columns
    assert "denv3_cases" in sero_df.columns
    assert "denv4_cases" in sero_df.columns
    assert "secondary_infection_risk_index" in sero_df.columns
    
    # Sum of serotype cases should match estimated_cases (within rounding tolerance)
    total_st_cases = sero_df["denv1_cases"].iloc[0] + sero_df["denv2_cases"].iloc[0] + sero_df["denv3_cases"].iloc[0] + sero_df["denv4_cases"].iloc[0]
    assert abs(total_st_cases - 10000) <= 5



