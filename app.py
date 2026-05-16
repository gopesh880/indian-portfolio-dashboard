import streamlit as st
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



with education_tab:

)
