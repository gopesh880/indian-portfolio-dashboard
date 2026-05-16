import streamlit as st
import pandas as pd

from utils.calculations import (
    calculate_weighted_return,
    calculate_risk_score,
    calculate_future_value,
    calculate_sip_future_value,
    calculate_inflation_adjusted_value,
    calculate_diversification_score,
)
from utils.insights import generate_portfolio_insights, calculate_health_score
from utils.simulations import monte_carlo_simulation
from utils.recommendations import get_investment_suggestions
from charts.portfolio_charts import (
    create_allocation_chart,
    create_returns_chart,
    create_growth_chart,
    create_monte_carlo_chart,
)

st.set_page_config(page_title="Indian Portfolio Dashboard", layout="wide")

st.markdown(
    """
    <style>
    .main {
        background-color: #0B1120;
        color: white;
    }

    .hero-box {
        background: linear-gradient(135deg, #172554, #0F172A);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #334155;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #CBD5E1;
    }

    .metric-card {
        background-color: #111827;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #334155;
        text-align: center;
    }

    .metric-title {
        color: #94A3B8;
        font-size: 15px;
        margin-bottom: 10px;
    }

    .metric-value {
        color: white;
        font-size: 34px;
        font-weight: bold;
    }

    .section-title {
        font-size: 32px;
        font-weight: 700;
        color: white;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .insight-box {
        background-color: #111827;
        border-left: 5px solid #2563EB;
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">Indian Portfolio & Risk Intelligence Dashboard</div>
        <div class="hero-subtitle">
            Analyze diversification, risk exposure, SIP growth,
            and long-term wealth projections.
        </div>
    </div>
