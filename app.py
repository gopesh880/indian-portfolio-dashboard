from pathlib import Path

import numpy as np
import yfinance as yf
import pandas as pd
import streamlit as st
from utils.market_data import get_price_data
from utils.tickers import (
    ETF_MAPPING,
    MF_MAPPING, BENCHMARK_MAPPING
)


from charts.portfolio_charts import (
    create_allocation_chart,
    create_growth_chart,
    create_monte_carlo_chart,
    create_returns_chart,
)
from utils.calculations import (
    calculate_diversification_score,
    calculate_future_value,
    calculate_inflation_adjusted_value,
    calculate_risk_score,
    calculate_sip_future_value,
    calculate_weighted_return, calculate_sharpe_ratio,
)
from utils.insights import calculate_health_score, generate_portfolio_insights
from utils.simulations import monte_carlo_simulation
from utils.recommendations import (
    get_investment_suggestions,
    get_asset_allocation, get_rebalancing_suggestions,
)


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sample_portfolio.csv"
REQUIRED_COLUMNS = {
    "Investment",
    "Category",
    "Allocation (%)",
    "Expected Return (%)",
    "Risk",
}


st.set_page_config(
    page_title="Mutual Fund & Portfolio Analytics Dashboard",
    layout="wide",
)


@st.cache_data
def load_portfolio(path: Path) -> pd.DataFrame:
    portfolio = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS.difference(portfolio.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")
    return portfolio


def format_inr(value: float) -> str:
    return f"Rs. {value:,.0f}"


def metric_card(label: str, value: str, note: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <p>{label}</p>
            <h3>{value}</h3>
            <span>{note}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
    :root {
        --bg: #F8FAFC;
        --panel: #FFFFFF;
        --ink: #0F172A;
        --muted: #64748B;
        --line: #E2E8F0;
        --blue: #2563EB;
        --green: #059669;
        --amber: #B45309;
        --red: #DC2626;
    }

    .stApp {
        background: var(--bg);
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(248, 250, 252, 0.92);
        border-bottom: 1px solid var(--line);
    }

    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: var(--ink);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1280px;
    }

    .hero {
        background: linear-gradient(135deg, #0F172A 0%, #1D4ED8 58%, #14B8A6 100%);
        border-radius: 8px;
        color: #FFFFFF;
        padding: 34px;
        margin-bottom: 22px;
        overflow: hidden;
    }

    .hero-eyebrow {
        color: #BFDBFE;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0;
        margin: 0 0 10px 0;
        text-transform: uppercase;
    }

    .hero h1 {
        color: #FFFFFF;
        font-size: 38px;
        line-height: 1.1;
        margin: 0;
        max-width: 760px;
    }

    .hero p {
        color: #DBEAFE;
        font-size: 16px;
        line-height: 1.6;
        margin: 14px 0 0 0;
        max-width: 760px;
    }

    .metric-card,
    .content-panel,
    .idea-card,
    .concept-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
    }

    .metric-card {
        min-height: 118px;
        padding: 18px;
    }

    .metric-card p {
        color: var(--muted);
        font-size: 13px;
        font-weight: 700;
        margin: 0 0 10px 0;
        text-transform: uppercase;
    }

    .metric-card h3 {
        color: var(--ink);
        font-size: 26px;
        line-height: 1.12;
        margin: 0 0 12px 0;
    }

    .metric-card span {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.4;
    }

    .content-panel {
        padding: 20px;
        margin-bottom: 18px;
    }

    .section-title {
        color: var(--ink);
        font-size: 24px;
        font-weight: 800;
        margin: 8px 0 16px 0;
    }

    .insight-box {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-left: 4px solid var(--blue);
        border-radius: 8px;
        color: #1E3A8A;
        margin-bottom: 12px;
        padding: 14px 16px;
    }

    .idea-card {
        min-height: 178px;
        padding: 18px;
    }

    .idea-card h4 {
        color: var(--ink);
        font-size: 18px;
        margin: 0 0 10px 0;
    }

    .idea-card p {
        color: var(--muted);
        font-size: 14px;
        line-height: 1.45;
        margin: 6px 0;
    }

    .concept-card {
        border-left: 4px solid #14B8A6;
        color: #164E63;
        min-height: 116px;
        padding: 16px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 8px;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 8px;
        color: var(--ink);
        height: 42px;
        padding: 0 16px;
    }

    .stTabs [aria-selected="true"] {
        background: #DBEAFE;
        border-color: #93C5FD;
        color: #1D4ED8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <p class="hero-eyebrow">Fund Management Analytics</p>
        <h1>Mutual Fund & Portfolio Analytics Dashboard</h1>
        <p>
            Analyze portfolio allocation, diversification, risk,
            expected returns, inflation impact and long-term
            wealth creation using data-driven investment analytics.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)
st.sidebar.title("Investor Profile")
st.sidebar.caption("Adjust assumptions to refresh projections instantly.")

investment_amount = st.sidebar.number_input(
    "Investment Amount",
    min_value=1000,
    value=500000,
    step=25000,
    format="%d",
)
sip_amount = st.sidebar.number_input(
    "Monthly SIP Amount",
    min_value=0,
    value=10000,
    step=1000,
    format="%d",
)
investment_duration = st.sidebar.slider(
    "Investment Duration",
    1,
    40,
    15,
)

investor_profile = st.sidebar.selectbox(
    "Investor Profile",
    ["Conservative", "Moderate", "Aggressive"],
    index=1,
)
goal = st.sidebar.selectbox(
    "Investment Goal",
    [
        "Wealth Creation",
        "Retirement",
        "Child Education",
        "House Purchase"
    ]
)
recommended_allocation = get_asset_allocation(
    investor_profile
)

st.sidebar.subheader("Recommended Allocation")

col1, col2 = st.sidebar.columns(2)

with col1:
    st.metric(
        "Equity",
        f"{recommended_allocation['Equity']}%"
    )

    st.metric(
        "Gold",
        f"{recommended_allocation['Gold']}%"
    )

with col2:
    st.metric(
        "Debt",
        f"{recommended_allocation['Debt']}%"
    )

inflation_rate = st.sidebar.slider(
    "Inflation Assumption",
    3.0,
    9.0,
    6.0,
    0.5,
)

volatility = st.sidebar.slider(
    "Simulation Volatility",
    8,
    30,
    18,
)
try:
    portfolio_df = load_portfolio(DATA_PATH)
except Exception as exc:
    st.error(f"Could not load portfolio data from {DATA_PATH}: {exc}")
    st.stop()

weighted_return = calculate_weighted_return(portfolio_df)
risk_free_rate = 7

sharpe_ratio = calculate_sharpe_ratio(
    weighted_return,
    risk_free_rate,
    volatility
)
risk_score = calculate_risk_score(portfolio_df)
future_value = calculate_future_value(
    investment_amount, weighted_return, investment_duration
)
sip_future_value = calculate_sip_future_value(
    sip_amount, weighted_return, investment_duration
)
inflation_adjusted_value = calculate_inflation_adjusted_value(
    future_value, inflation_rate, investment_duration
)
diversification_score = calculate_diversification_score(portfolio_df)
health_score = calculate_health_score(portfolio_df, risk_score)
simulation_df = monte_carlo_simulation(
    investment_amount,
    weighted_return,
    volatility,
    investment_duration,
)

metric_cols = st.columns(5)
with metric_cols[0]:
    metric_card("Expected return", f"{weighted_return:.2f}%", "Weighted by portfolio allocation")
with metric_cols[1]:
    metric_card("Risk score", f"{risk_score}/100", "Lower is steadier, higher is more volatile")
with metric_cols[2]:
    metric_card("Health score", f"{health_score}/100", "Blend of risk balance and diversification")
with metric_cols[3]:
    metric_card("Projected value", format_inr(future_value), f"After {investment_duration} years")
with metric_cols[4]:
    metric_card(
        "Sharpe Ratio",
        str(sharpe_ratio),
        "Risk-adjusted return"
    )

second_metric_cols = st.columns(3)
with second_metric_cols[0]:
    metric_card("SIP future value", format_inr(sip_future_value), f"{format_inr(sip_amount)} monthly")
with second_metric_cols[1]:
    metric_card("Inflation adjusted", format_inr(inflation_adjusted_value), f"At {inflation_rate:.1f}% inflation")
with second_metric_cols[2]:
    metric_card("Diversification", f"{diversification_score}/100", "Higher means less concentrated")

analytics_tab, simulation_tab, education_tab, amc_tab, mf_tab, backtest_tab = st.tabs(
    [
        "Portfolio Analytics",
        "Simulation & Insights",
        "Learn Investing",
        "AMC Analytics",
        "Mutual Fund Analytics",
        "Quant Backtesting"
    ]
)
with analytics_tab:
    st.markdown('<div class="section-title">Portfolio Analytics</div>', unsafe_allow_html=True)

    allocation_chart = create_allocation_chart(portfolio_df)
    returns_chart = create_returns_chart(portfolio_df)

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.plotly_chart(allocation_chart, width="stretch")
    with col_chart2:
        st.plotly_chart(returns_chart, width="stretch")

    growth_chart = create_growth_chart(
        investment_amount,
        weighted_return,
        investment_duration,
    )
    st.plotly_chart(growth_chart, width="stretch")

    st.markdown('<div class="section-title">Current Allocation</div>', unsafe_allow_html=True)
    st.dataframe(
        portfolio_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Allocation (%)": st.column_config.ProgressColumn(
                "Allocation (%)",
                min_value=0,
                max_value=100,
                format="%.0f%%",
            ),
            "Expected Return (%)": st.column_config.NumberColumn(
                "Expected Return (%)",
                format="%.1f%%",
            ),
        },
    )

with simulation_tab:
    st.markdown(
        '<div class="section-title">Simulation & Investor Insights</div>',
        unsafe_allow_html=True,
    )

    monte_carlo_chart = create_monte_carlo_chart(simulation_df)
    st.plotly_chart(monte_carlo_chart, width="stretch")

    st.markdown('<div class="section-title">Portfolio Insights</div>', unsafe_allow_html=True)
    insights = generate_portfolio_insights(portfolio_df, weighted_return, risk_score)

    for insight in insights:
        st.markdown(
            f'<div class="insight-box">{insight}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Explore Investment Ideas</div>', unsafe_allow_html=True)
    recommendation_df = get_investment_suggestions(
    investor_profile,goal )
    idea_cols = st.columns(3)

    for index, row in recommendation_df.iterrows():
        with idea_cols[index % 3]:
            st.markdown(
                f"""
                <div class="idea-card">
                    <h4>{row['Investment']}</h4>
                    <p><strong>Category:</strong> {row['Category']}</p>
                    <p><strong>Risk:</strong> {row['Risk']}</p>
                    <p>{row['Why']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
with education_tab:
    st.markdown(
        '<div class="section-title">Finance Concepts Explained</div>',
        unsafe_allow_html=True,
    )

    concepts = [
        "Diversification spreads investments across categories to reduce portfolio-level risk.",
        "SIP investing builds wealth steadily by investing fixed amounts through market cycles.",
        "Small-cap funds can grow faster, but they usually bring sharper volatility.",
        "Inflation reduces purchasing power, so real returns matter more than headline returns.",
        "Monte Carlo simulation estimates many future paths instead of assuming one perfect outcome.",
        "Portfolio health improves when return potential, risk, and concentration are in balance.",
    ]

    concept_cols = st.columns(3)
    for index, concept in enumerate(concepts):
        with concept_cols[index % 3]:
            st.markdown(f'<div class="concept-card">{concept}</div>', unsafe_allow_html=True)

st.caption("Educational dashboard only. This is not financial advice.")
current_allocation = {
    "Equity": 75,
    "Debt": 10,
    "Gold": 10
}
target_allocation = {
    "Equity": recommended_allocation["Equity"],
    "Debt": recommended_allocation["Debt"],
    "Gold": recommended_allocation["Gold"]
}
rebalancing_suggestions = get_rebalancing_suggestions(
    current_allocation,
    target_allocation
)
st.subheader("Portfolio Rebalancing")

for suggestion in rebalancing_suggestions:
    st.write(suggestion)
with amc_tab:

    st.markdown(
        '<div class="section-title">AMC Analytics</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total AUM", "₹8.5 Trillion")

    with col2:
        st.metric("ETF Count", "22")

    with col3:
        st.metric("Index Funds", "14")

    with col4:
        st.metric("Active Funds", "37")

    st.markdown("---")

    amc_df = pd.DataFrame({
        "Fund": [
            "HDFC Flexi Cap Fund",
            "HDFC Mid Cap Opportunities Fund",
            "HDFC Balanced Advantage Fund",
            "HDFC Small Cap Fund",
            "HDFC Nifty 50 Index Fund"
        ],
        "Category": [
            "Flexi Cap",
            "Mid Cap",
            "Hybrid",
            "Small Cap",
            "Index"
        ],
        "Return (%)": [
            18.5,
            21.2,
            13.1,
            24.8,
            14.6
        ]
    })

    st.dataframe(amc_df, use_container_width=True)
with mf_tab:

    st.header("Mutual Fund Analytics")

    fund = st.selectbox(
        "Select Fund",
        list(MF_MAPPING.keys())
    )

    selected_ticker = MF_MAPPING[fund]

    mf_data = get_price_data(
        selected_ticker
    )

    if mf_data.empty:

        st.error(
            "Unable to fetch mutual fund data."
        )

    else:

        close = mf_data["Close"]

        if isinstance(
            close,
            pd.DataFrame
        ):
            close = close.iloc[:, 0]

        close = close.dropna()

        returns = (
            close
            .pct_change()
            .dropna()
        )

        total_return = round(
            (
                close.iloc[-1]
                /
                close.iloc[0]
                - 1
            ) * 100,
            2
        )

        volatility = round(
            returns.std()
            *
            (252 ** 0.5)
            *
            100,
            2
        )

        sharpe = round(
            (
                returns.mean()
                * 252
            )
            /
            (
                returns.std()
                *
                (252 ** 0.5)
            ),
            2
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Return",
                f"{total_return}%"
            )

        with col2:
            st.metric(
                "Volatility",
                f"{volatility}%"
            )

        with col3:
            st.metric(
                "Sharpe Ratio",
                f"{sharpe}"
            )

        st.markdown("---")

        st.subheader(
            "NAV History"
        )

        st.line_chart(
            close
        )

        st.subheader(
            "Recent NAV Data"
        )

        st.dataframe(
            mf_data.tail(),
            use_container_width=True
        )
with backtest_tab:

    st.header("Quant Strategy Backtesting")

    ticker = st.selectbox(
        "Select Asset",
        list(ETF_MAPPING.keys())
    )

    strategy = st.selectbox(
        "Strategy",
        [
            "Buy & Hold",
            "EMA Crossover",
            "Momentum"
        ]
    )

    selected_ticker = ETF_MAPPING[ticker]

    price_data = get_price_data(
        selected_ticker
    )

    benchmark_data = get_price_data(
        "^NSEI"
    )

    if (
        price_data.empty
        or benchmark_data.empty
    ):

        st.error(
            "Unable to fetch market data."
        )

    else:

        # ==========================
        # CLEAN PRICE DATA
        # ==========================

        close = price_data["Close"]

        if isinstance(
            close,
            pd.DataFrame
        ):
            close = close.iloc[:, 0]

        benchmark_close = benchmark_data["Close"]

        if isinstance(
            benchmark_close,
            pd.DataFrame
        ):
            benchmark_close = benchmark_close.iloc[:, 0]

        close = close.dropna()

        benchmark_close = (
            benchmark_close.dropna()
        )

        # ==========================
        # RETURNS
        # ==========================

        returns = (
            close
            .pct_change()
            .dropna()
        )

        benchmark_returns = (
            benchmark_close
            .pct_change()
            .dropna()
        )

        # ==========================
        # STRATEGY LOGIC
        # ==========================

        if strategy == "EMA Crossover":

            ema20 = (
                close
                .ewm(span=20)
                .mean()
            )

            ema50 = (
                close
                .ewm(span=50)
                .mean()
            )

            signal = (
                ema20 > ema50
            ).astype(int)

            strategy_returns = (
                returns
                *
                signal.shift(1)
                .fillna(0)
            )

        elif strategy == "Momentum":

            momentum = (
                close
                /
                close.shift(126)
                - 1
            )

            signal = (
                momentum > 0
            ).astype(int)

            strategy_returns = (
                returns
                *
                signal.shift(1)
                .fillna(0)
            )

        else:

            strategy_returns = (
                returns
            )

        # ==========================
        # EQUITY CURVES
        # ==========================

        equity_curve = (
            1 +
            strategy_returns
        ).cumprod()

        benchmark_curve = (
            1 +
            benchmark_returns
        ).cumprod()

        # ==========================
        # METRICS
        # ==========================

        total_return = round(
            (
                equity_curve.iloc[-1]
                - 1
            ) * 100,
            2
        )

        benchmark_return = round(
            (
                benchmark_curve.iloc[-1]
                - 1
            ) * 100,
            2
        )

        alpha = round(
            total_return
            - benchmark_return,
            2
        )

        volatility_bt = round(
            strategy_returns.std()
            *
            np.sqrt(252)
            *
            100,
            2
        )

        sharpe_bt = round(
            (
                strategy_returns.mean()
                *
                252
            )
            /
            (
                strategy_returns.std()
                *
                np.sqrt(252)
            ),
            2
        )

        rolling_max = (
            equity_curve
            .cummax()
        )

        drawdown = (
            equity_curve
            -
            rolling_max
        ) / rolling_max

        max_drawdown = round(
            drawdown.min()
            * 100,
            2
        )

        # ==========================
        # DASHBOARD METRICS
        # ==========================

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "Strategy Return",
                f"{total_return}%"
            )

        with col2:
            st.metric(
                "Benchmark Return",
                f"{benchmark_return}%"
            )

        with col3:
            st.metric(
                "Alpha",
                f"{alpha}%"
            )

        with col4:
            st.metric(
                "Sharpe Ratio",
                f"{sharpe_bt}"
            )

        with col5:
            st.metric(
                "Max Drawdown",
                f"{max_drawdown}%"
            )

        st.markdown("---")

        # ==========================
        # STRATEGY VS NIFTY
        # ==========================

        st.subheader(
            "Strategy vs Nifty"
        )

        comparison_df = pd.DataFrame(
            {
                "Strategy":
                equity_curve * 100,

                "Nifty":
                benchmark_curve * 100
            }
        )

        st.line_chart(
            comparison_df
        )

        # ==========================
        # PRICE HISTORY
        # ==========================

        st.subheader(
            f"{ticker} Price History"
        )

        st.line_chart(
            close
        )

        # ==========================
        # DRAWDOWN
        # ==========================

        st.subheader(
            "Drawdown Analysis"
        )

        st.line_chart(
            drawdown
        )

        # ==========================
        # RECENT DATA
        # ==========================

        st.subheader(
            "Recent Market Data"
        )

        st.dataframe(
            price_data.tail(),
            use_container_width=True
        )
