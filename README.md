# 📈 Options Greeks Calculator

This web app calculates **option Greeks** and **option prices** using the **Black-Scholes model**.  
It allows users to:
- Compute **Call & Put prices** using the Black-Scholes formula.
- Analyze **option Greeks** (Delta, Gamma, Vega, Theta, Rho).
- Fetch **live stock prices** from Yahoo Finance.
- Visualize **Greek sensitivities** and **option price changes** with different parameters.

---

## 📖 **Black-Scholes Model**
The **Black-Scholes model** is used to price European call and put options:

### **📌 Call & Put Option Price Formulas**
\[
C = S N(d_1) - K e^{-rT} N(d_2)
\]

\[
P = K e^{-rT} N(-d_2) - S N(-d_1)
\]

where:

\[
d_1 = \frac{\ln(S/K) + (r + \sigma^2 / 2)T}{\sigma \sqrt{T}}
\]

\[
d_2 = d_1 - \sigma \sqrt{T}
\]

### **📌 Parameters**
- **S** = Stock price  
- **K** = Strike price  
- **T** = Time to expiration  
- **r** = Risk-free interest rate  
- **σ** = Volatility  
- **N(d)** = Cumulative standard normal distribution  

---

## 📊 **Option Greeks**
### **Greeks Explained**
| Greek | Meaning |
|--------|----------|
| **Delta (Δ)** | Sensitivity to stock price changes |
| **Gamma (Γ)** | Sensitivity of Delta to stock price changes |
| **Vega (ν)** | Sensitivity to volatility changes |
| **Theta (Θ)** | Sensitivity to time decay |
| **Rho (ρ)** | Sensitivity to interest rate changes |

---


## ⚠️ Disclaimer

**The Black-Scholes model assumes no dividends, constant volatility, and risk-free rates, which may not reflect real-world conditions.**

---

## 🚀 **Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/Options-Greeks-Calculator.git
cd Options-Greeks-Calculator
