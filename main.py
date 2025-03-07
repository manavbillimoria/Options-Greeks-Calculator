from greeks import black_scholes_greeks

def main():
    print("Welcome to the Options Greeks Calculator!")

    # Get user input
    S = float(input("Enter stock price (S): "))
    K = float(input("Enter strike price (K): "))
    T = float(input("Enter time to expiration (years): "))
    r = float(input("Enter risk-free rate (as decimal, e.g., 0.05 for 5%): "))
    sigma = float(input("Enter volatility (as decimal, e.g., 0.2 for 20%): "))
    option_type = input("Enter option type (call/put): ").strip().lower()

    # Calculate Greeks
    greeks = black_scholes_greeks(S, K, T, r, sigma, option_type)

    # Display results
    print("\nOption Greeks:")
    for key, value in greeks.items():
        print(f"{key}: {value:.4f}")

if __name__ == "__main__":
    main()
