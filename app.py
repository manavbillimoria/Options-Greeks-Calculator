import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from greeks import black_scholes_greeks

st.set_page_config(page_title="Option Greeks Calculator")

st.title("📈 Options Greeks Calculator")

#Calculator Description for User
with st.expander("ℹ️ **What is this calculator?**"):
    st.write("""
    This tool calculates **option Greeks** using the **Black-Scholes model**.  
    The **Black-Scholes model** is a mathematical formula used to price **European call and put options**.

    ### **📌 Black-Scholes Formula for Call and Put Options**
    The Black-Scholes price for a **call option** is given by:

    $$
    C = S N(d_1) - K e^{-rT} N(d_2)
    $$

    The Black-Scholes price for a **put option** is:

    $$
    P = K e^{-rT} N(-d_2) - S N(-d_1)
    $$

    where:

    $$
    d_1 = \\frac{\\ln(S/K) + (r + \\sigma^2 / 2)T}{\\sigma \\sqrt{T}}
    $$

    $$
    d_2 = d_1 - \\sigma \\sqrt{T}
    $$

    - **S** = Stock price  
    - **K** = Strike price  
    - **T** = Time to expiration  
    - **r** = Risk-free interest rate  
    - **σ** = Volatility  
    - **N(d)** = Cumulative standard normal distribution  

    The Greeks describe how the option price changes with **stock price, volatility, time decay, and interest rates**.
    """)


st.sidebar.header("Input Parameters")

#Parameter Descriptions for User
with st.sidebar.expander("📌 **Parameter Descriptions**"):
    st.write("""
    - **Stock Price (S)**: Current market price of the stock.
    - **Strike Price (K)**: Price at which the option can be exercised.
    - **Time to Expiration (T)**: Time left until the option expires (in years).
    - **Risk-Free Rate (r)**: Theoretical return on a risk-free investment.
    - **Volatility (σ)**: The expected fluctuation in the stock price (higher = riskier).
    - **Option Type**: Choose between a **Call** (buy) or **Put** (sell) option.
    """)


if "live_price" not in st.session_state:
    st.session_state.live_price = None

# Market price switch 
use_live_price = st.sidebar.checkbox("Use Live Market Price", value=True)

#Stock Ticker Selector
ticker = None
if use_live_price:
    ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")
    if st.sidebar.button("Use Live Data"):
        try:
            stock = yf.Ticker(ticker)
            st.session_state.live_price = stock.history(period="1d")["Close"].iloc[-1]
            st.sidebar.success(f"Live Price: ${st.session_state.live_price:.2f}")
        except Exception:
            st.sidebar.error("Invalid Ticker Symbol")

# Manual stock price input selector
S = None  # Default to None
if not use_live_price:
    S = st.sidebar.number_input("Stock Price (S)", min_value=1.0, value=100.0, step=0.1)

K = st.sidebar.number_input("Strike Price (K)", min_value=1.0, value=100.0, step=0.1)
T = st.sidebar.number_input("Time to Expiration (Years)", min_value=0.01, value=1.0, step=0.01)
r = st.sidebar.number_input("Risk-Free Rate (as decimal)", min_value=0.0, value=0.05, step=0.001)
sigma = st.sidebar.number_input("Volatility (as decimal)", min_value=0.01, value=0.2, step=0.01)
option_type = st.sidebar.radio("Option Type", ("call", "put"))


if st.sidebar.button("Generate Greeks"):
    S_final = st.session_state.live_price if use_live_price and st.session_state.live_price is not None else (S if S is not None else 100.0)

    if S_final is None:
        st.error("Please enter a stock price or fetch live data before calculating Greeks.")
    else:
        
        greeks = black_scholes_greeks(S_final, K, T, r, sigma, option_type)
        
        st.subheader("📊 Option Greeks")
        with st.expander("📌 **What Do the Greeks Mean?**"):
            st.write("""
            - **Delta (Δ)**: Measures how much the option price changes when the stock price moves **by $1**.
            - **Gamma (Γ)**: Measures how fast **Delta** changes as the stock price moves.
            - **Vega (ν)**: Sensitivity of the option price to a **1% change in volatility**.
            - **Theta (Θ)**: Measures **time decay** – how much the option loses value per day.
            - **Rho (ρ)**: Sensitivity of the option price to **interest rate changes**.
            """)
        
        st.write(f"**(Using {'Live' if use_live_price else 'Manual'} Price: ${S_final:.2f})**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            for key, value in greeks.items():
                if key not in ["Call Price", "Put Price"]:
                    st.write(f"**{key}**: {value:.4f}")
        with col2:
            st.write(f"**Call Option Price:** ${greeks['Call Price']:.4f}")
            st.write(f"**Put Option Price:** ${greeks['Put Price']:.4f}")

        
    
        # Visualization Section
        st.subheader("📈 Visualizing Option Greeks")

        # Generate stock prices from 80% to 120% of the selected price for the graph
        S_range = np.linspace(0.8 * S_final, 1.2 * S_final, 50)

        # Calculate Greeks for different stock prices
        delta_vals, gamma_vals, vega_vals, theta_vals, rho_vals = [], [], [], [], []

        
        for S_val in S_range:
            greeks = black_scholes_greeks(S_val, K, T, r, sigma, option_type)
            delta_vals.append(greeks["Delta"])
            gamma_vals.append(greeks["Gamma"])
            vega_vals.append(greeks["Vega"])
            theta_vals.append(greeks["Theta"])
            rho_vals.append(greeks["Rho"])

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.plot(S_range, delta_vals, label="Delta", linestyle="-", marker="o")
        ax.plot(S_range, gamma_vals, label="Gamma", linestyle="--", marker="s")
        ax.plot(S_range, vega_vals, label="Vega", linestyle="-.", marker="^")
        ax.plot(S_range, theta_vals, label="Theta", linestyle=":", marker="v")
        ax.plot(S_range, rho_vals, label="Rho", linestyle="--", marker="d")

        ax.set_xlabel("Stock Price (S)")
        ax.set_ylabel("Greek Values")
        ax.set_title(f"Greek Sensitivities for {option_type.capitalize()} Option")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

# Disclaimer Section for User
with st.expander("⚠️ **Disclaimer**"):
    st.write(""" 
    The Black-Scholes model assumes **no dividends, constant volatility, and risk-free rates**, which may not reflect real-world conditions.  
    """)
