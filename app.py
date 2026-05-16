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

from utils.simulations import (
    monte_carlo_simulation
)

from utils.recommendations import (
    get_investment_suggestions
)

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
    page_title="Indian Portfolio Dashboard",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #0B1120;
        color: white;
    }

    .hero-box {
        background: linear-gradient(
            135deg,
            #172554,
            #0F172A
        );

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
            Analyze diversification, risk exposure, SIP growth,
            and long-term wealth projections.
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

portfolio_df = pd.read_csv(
    "data/sample_portfolio.csv"
)

# -------------------------------------------------
# CALCULATIONS
# -------------------------------------------------

weighted_return = calculate_weighted_return(
    portfolio_df
)

risk_score = calculate_risk_score(
    portfolio_df
)

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
# KPI CARDS
# -------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                Expected Return
            </div>

            <div class="metric-value">
                {weighted_return:.2f}%
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                Risk Score
            </div>

            <div class="metric-value">
                {risk_score}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                Portfolio Health
            </div>

            <div class="metric-value">
                {health_score}/100
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                Projected Value
            </div>

            <div class="metric-value">
                ₹{future_value:,.0f}
            </div>

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

    allocation_chart = create_allocation_chart(
        portfolio_df
    )

    returns_chart = create_returns_chart(
        portfolio_df
    )

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:

        st.plotly_chart(
            allocation_chart,
            use_container_width=True
        )

    with col_chart2:

        st.plotly_chart(
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
        '<div class="section-title">Simulation & Investor Insights</div>',
        unsafe_allow_html=True
    )

    monte_carlo_chart = create_monte_carlo_chart(
        simulation_df
    )

    st.plotly_chart(
        monte_carlo_chart,
        use_container_width=True
    )

    st.subheader("Portfolio Insights")

    insights = generate_portfolio_insights(
        portfolio_df,
        weighted_return,
        risk_score
    )

    for insight in insights:

        st.markdown(
            f"""
            <div class="insight-box">

                <p style="color:white;">
                    {insight}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------------------------
    # INVESTMENT IDEAS
    # -------------------------------------------------

    st.subheader("Explore Investment Ideas")

    recommendation_df = get_investment_suggestions(
        investor_profile
    )

    for _, row in recommendation_df.iterrows():

        st.markdown(
            f"""
            <div class="insight-box">

                <h4 style="color:white;">
                    {row['Investment']}
                </h4>

                <p style="color:#CBD5E1;">
                    <b>Category:</b> {row['Category']}
                </p>

                <p style="color:#CBD5E1;">
                    <b>Risk:</b> {row['Risk']}
                </p>

                <p style="color:#CBD5E1;">
                    {row['Why']}
                </p>

            </div>
            """,
            unsafe_allow_html=True
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
        "Diversification means spreading investments across multiple asset categories to reduce overall portfolio risk."
    )

    st.info(
        "SIP investing helps investors build wealth consistently through long-term compounding."
    )

    st.info(
        "Small-cap investments may offer higher growth potential but also carry higher volatility."
    )

    st.info(
        "Inflation reduces purchasing power over time, which is why inflation-adjusted returns matter."
    )

    st.info(
        "Monte Carlo simulation estimates multiple possible future investment outcomes using probability-based scenarios."
    )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.write("")
st.write("")

st.caption(
    "Built using Python, Streamlit, Pandas, NumPy, and Plotly"
)
