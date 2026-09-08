import math
import numpy as np
import yfinance as yf
from scipy.stats import norm

def get_risk_free_rate() -> float:
    # Fetch the 10-Year Treasury Yield index
    treasury = yf.Ticker("^TNX")
    df = treasury.history(period="5d")
    
    if df.empty:
        #default value if all else fails
        return 0.045 
    
    # ^TNX returns e.g. 4.78 for 4.78%, so divide by 100
    latest_yield = df['Close'].iloc[-1]
    return latest_yield / 100.0

def analyze_option_live(ticker_symbol: str, K: float, T: float):
    ticker_symbol = ticker_symbol.upper().strip()

    # pull risk-free rate
    r = get_risk_free_rate()

    #get 1 year of histoical data for the ticker
    print(f"Fetching live market data for {ticker_symbol}")
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period="1y")

    if df.empty:
        raise ValueError(f"ur ticker symbol ({ticker_symbol}) sucks")

    #current stock price
    S = df['Close'].iloc[-1]

    #annualized historical volatility from daily log returns
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
    daily_vol = df['Log_Return'].std()
    sigma = daily_vol * math.sqrt(252) #252 trading days/yr

    #black-scholes
    d1 = (math.log(S/K) + (r + sigma**2 / 2)*T)/(sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)

    call_price = S*norm.cdf(d1) - K*math.exp(-r*T)*norm.cdf(d2)
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1)/(S*sigma*math.sqrt(T))
    theta = - (S*norm.pdf(d1)*sigma)/(2*math.sqrt(T)) - r*K*math.exp(-r*T)*norm.cdf(d2)
    vega = S*math.sqrt(T)*norm.pdf(d1)

    #print stuff
    print(f" Current Stock Price (S)     : ${S:.2f}")
    print(f" Strike Price (K)            : ${K:.2f}")
    print(f" Annualized Volatility (σ)   : {sigma * 100:.2f}%")
    print(f" Time to Expiration (T)      : {T} years")
    print(f" Risk-Free Rate (r)          : {r * 100:.2f}%")

    print(f" Theoretical Call Price (C)  : ${call_price:.2f}")
    print(f" Delta                       : {delta:.4f}")
    print(f" Gamma                       : {gamma:.4f}")
    print(f" Theta (Annualized)          : {theta:.2f}")
    print(f" Vega                        : {vega:.4f}")

#test
analyze_option_live("brk-b", K=510, T=0.5)
