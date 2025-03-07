import numpy as np
from scipy.stats import norm

def black_scholes_greeks(S, K, T, r, sigma, option_type="call"):
    """
    Compute the Greeks and Black-Scholes price for European Call/Put options.

    Parameters:
    S - Stock price
    K - Strike price
    T - Time to expiration (in years)
    r - Risk-free interest rate (decimal)
    sigma - Volatility (decimal)
    option_type - "call" or "put"

    Returns:
    Dictionary containing Call Price, Put Price, Delta, Gamma, Vega, Theta, Rho
    """
    
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Black-Scholes option prices
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    # Greeks calculations
    delta = norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))) - (r * K * np.exp(-r * T) * norm.cdf(d2) if option_type == "call" else -r * K * np.exp(-r * T) * norm.cdf(-d2))
    rho = K * T * np.exp(-r * T) * norm.cdf(d2) if option_type == "call" else -K * T * np.exp(-r * T) * norm.cdf(-d2)

    return {
        "Call Price": call_price,
        "Put Price": put_price,
        "Delta": delta,
        "Gamma": gamma,
        "Vega": vega / 100,
        "Theta": theta / 365,
        "Rho": rho / 100
    }
