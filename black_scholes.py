from scipy.stats import norm
import math

def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float):
    d1 = (math.log(S/K) + (r + sigma**2 / 2)*T)/(sigma*math.sqrt(T))

    d2 = d1 - sigma*math.sqrt(T)

    print(f"C = {S*norm.cdf(d1) - K*math.exp(-r*T)*norm.cdf(d2):.3f}") # call price

    print(f"Delta = {norm.cdf(d1):.4f}")

    print(f"Gamma = {norm.pdf(d1)/(S*sigma*math.sqrt(T)):.4f}")

    Theta = - (S*norm.pdf(d1)*sigma)/(2*math.sqrt(T)) - r*K*math.exp(-r*T)*norm.cdf(d2)
    print(f"Theta = {Theta:.4f}")

    print(f"Vega = {S*math.sqrt(T)*norm.pdf(d1):.4f}")

#test
black_scholes_call(100,105,1,.05,.2)

