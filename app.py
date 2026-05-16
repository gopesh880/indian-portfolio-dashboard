import streamlit as st
import pandas as pd

from utils.calculations import (
    calculate_weighted_return,
    calculate_risk_score,
    calculate_future_value,
    calculate_sip_future_value,
    calculate_inflation_adjusted_value,
    calculate_diversification_score
)

from utils.insights import (
    generate_portfolio_insights,
    calculate_health_score
)

from utils.simulations import monte_carlo_simulation

from utils.recommendations import get_investment_suggestions

from charts.portfolio_charts import (
    create_allocation_chart,
    create_returns_chart,
    create_growth_chart,
    create_monte_carlo_chart
)

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Portfolio Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
        color: white;
    }

    .hero-box {
        background: linear-gradient(135deg, #1f2937, #111827);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid #374151;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 700;
        color: white;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #9CA3AF;
        margin-top: 10px;
    }

    .metric-card {
        background-color: #1F2937;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #374151;
        text-align: center;
    }

    .metric-title {
        font-size: 15px;
        color: #9CA3AF;
    }

    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: white;
    }

    .section-title {
        font-size: 28px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 20px;
        color: white;
    }

    .insight-box {
        background-color: #111827;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# HERO SECTION
# -------------------------------------------------

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">
            Indian Portfolio & Risk Intelligence Dashboard
        </div>

        <div class="hero-subtitle">
            Analyze portfolio diversification, risk exposure, SIP growth,
            and long-term investment projections.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("Investor Profile")

investment_amount = st.sidebar.number_input(
    "Investment Amount (₹)",
    min_value=1000,
    value=500000
)

sip_amount = st.sidebar.number_input(
    "Monthly SIP Amount (₹)",
    min_value=0,
    value=10000
)

investment_duration = st.sidebar.slider(
    "Investment Duration (Years)",
    1,
    40,
    15
)

investor_profile = st.sidebar.selectbox(
    "Investor Profile",
    ["Conservative", "Moderate", "Aggressive"]
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

portfolio_df = pd.read_csv("data/sample_portfolio.csv")

# -------------------------------------------------
# CALCULATIONS
# -------------------------------------------------

weighted_return = calculate_weighted_return(portfolio_df)

risk_score = calculate_risk_score(portfolio_df)

future_value = calculate_future_value(
    investment_amount,
    weighted_return,
    investment_duration
)

sip_future_value = calculate_sip_future_value(
    sip_amount,
    weighted_return,
    investment_duration
)

inflation_adjusted_value = calculate_inflation_adjusted_value(
    future_value,
    6,
    investment_duration
)

diversification_score = calculate_diversification_score(
    portfolio_df
)

health_score = calculate_health_score(
    portfolio_df,
    risk_score
)

simulation_df = monte_carlo_simulation(
    investment_amount,
    weighted_return,
    18,
    investment_duration
)

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Expected Return</div>
            <div class="metric-value">{weighted_return:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Risk Score</div>
            <div class="metric-value">{risk_score}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Portfolio Health</div>
            <div class="metric-value">{health_score}/100</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Projected Value</div>
            <div class="metric-value">₹{future_value:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")
st.write("")

# -------------------------------------------------
# TABS
# -------------------------------------------------

analytics_tab, simulation_tab, education_tab = st.tabs([
    "Portfolio Analytics",
    "Simulation & Insights",
    "Learn Investing"
])

# -------------------------------------------------
# ANALYTICS TAB
# -------------------------------------------------

with analytics_tab:

    st.markdown(
        '<div class="section-title">Portfolio Analytics</div>',
        unsafe_allow_html=True
    )

    allocation_chart = create_allocation_chart(portfolio_df)
    returns_chart = create_returns_chart(portfolio_df)

    chart_col1, chart_col2 = st.columns(2)

    chart_col1.plotly_chart(
        allocation_chart,
        use_container_width=True
    )

    chart_col2.plotly_chart(
        returns_chart,
        use_container_width=True
    )

    growth_chart = create_growth_chart(
        investment_amount,
        weighted_return,
        investment_duration
    )

    st.plotly_chart(
        growth_chart,
        use_container_width=True
    )

    st.subheader("Current Portfolio Allocation")

    st.dataframe(
        portfolio_df,
        use_container_width=True
    )

# -------------------------------------------------
# SIMULATION TAB
# -------------------------------------------------

with simulation_tab:

    st.markdown(
        '<div class="section-title">Monte Carlo Simulation</div>',
        unsafe_allow_html=True
    )

    monte_carlo_chart = create_monte_carlo_chart(
        simulation_df
    )

    st.plotly_chart(
        monte_carlo_chart,
        use_container_width=True
    )

    st.subheader("Investor Insights")

    insights = generate_portfolio_insights(
        portfolio_df,
        weighted_return,
        risk_score
    )

    for insight in insights:

        st.markdown(
            f"""
            <div class="insight-box">
                {insight}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Suggested Investment Ideas")

    recommendation_df = get_investment_suggestions(
        investor_profile
    )

    st.dataframe(
        recommendation_df,
        use_container_width=True
    )

# -------------------------------------------------
# EDUCATION TAB
# -------------------------------------------------

with education_tab:

    st.markdown(
        '<div class="section-title">Finance Concepts Explained</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Diversification means spreading investments across multiple asset categories to reduce risk."
    )

    st.info(
        "SIP investing helps investors build wealth consistently over long periods through compounding."
    )

    st.info(
        "Small-cap investments may provide higher growth potential but also carry higher volatility."
    )

    st.info(
        "Inflation reduces purchasing power over time, which is why inflation-adjusted returns matter."
    )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.write("")
st.write("")

st.caption(
    "Built using Python, Streamlit, Pandas, NumPy, and Plotly"
)
