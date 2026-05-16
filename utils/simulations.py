
import numpy as np
import pandas as pd

def monte_carlo_simulation(
    initial_amount,
    expected_return,
    volatility,
    years,
    simulations=200
):

    results = []

    expected_return = expected_return / 100
    volatility = volatility / 100

    for sim in range(simulations):

        portfolio_value = initial_amount

        yearly_values = []

        for year in range(years):

            simulated_return = np.random.normal(
                expected_return,
                volatility
            )

            portfolio_value *= (1 + simulated_return)

            yearly_values.append(portfolio_value)

        results.append(yearly_values)

    simulation_df = pd.DataFrame(results).T

    return simulation_df
