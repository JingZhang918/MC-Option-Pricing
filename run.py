from MCPricer import MCPricer
from financial_instruments import europeanOption, barrierOption
import numpy as np
np.random.seed(0)
from yahoo_fin import options
import yfinance as yf
from datetime import datetime

if __name__ == "__main__":
    # input parameters through keyboard
    ticker = "AAPL"
    expiration_date = "January 7, 2022" # January 7, 2022 or 01/07/2022 or 01/07/22
    # option_class = "barrier"           # european option / barrier option
    option_class = "european"
    option_type = "call"                # call or put
    if option_class == "barrier":
        barrier_type = "up-out"           # up-in / up-out / down-in/ down-out
        barrier = 100
    risk_free_rate = .01
    volatility = .03
    drift = .1
    continuous_yield = 0
    index = 0

    # start with one option
    if option_type == "call":
        option_lists = options.get_calls(ticker, expiration_date)
    else:
        option_lists = options.get_puts(ticker, expiration_date)
    option = option_lists.iloc[index]

    # use yfinance to get current stock price
    underlying_price = yf.Ticker(ticker).history(period="1d").Close.values[0]
    strike_price = option["Strike"]
    time_to_expiration = (datetime.strptime(expiration_date, "%B %d, %Y") - datetime.today()).days # get days to expiration

    if option_class == "european":
        optionEU = europeanOption()
        # initialize parameters
        optionEU.S = underlying_price
        optionEU.sigma = volatility
        optionEU.K = strike_price
        optionEU.T = time_to_expiration
        optionEU.r = risk_free_rate
        optionEU.q = continuous_yield
        optionEU.type = option_type
        optionEU.get_d1_d2()

        # calculate Greeks and prices under BSM and MC
        BSM_price = optionEU.BSPricer()
        Delta = optionEU.get_delta()
        Gamma = optionEU.get_gamma()
        Vega = optionEU.get_vega()
        MC_price = MCPricer(optionEU, drift, 100).get_price()

        print(f"under the input assumptions, the black-scholes-merton price is {BSM_price},\n"
              f"delta is {Delta},\n"
              f"gamma is {Gamma},\n"
              f"Vega is {Vega},\n"
              f"Monte Carlo Simulation price is {MC_price}")

    elif option_class == "barrier":
        optionBA = barrierOption(barrier, barrier_type)
        # initialize parameters
        optionBA.barrier = barrier
        optionBA.barrier_type = barrier_type
        optionBA.S = underlying_price
        optionBA.sigma = volatility
        optionBA.K = strike_price
        optionBA.T = time_to_expiration
        optionBA.r = risk_free_rate
        optionBA.q = continuous_yield
        optionBA.type = option_type
        optionBA.get_d1_d2()

        Delta = optionBA.get_delta()
        Gamma = optionBA.get_gamma()
        Vega = optionBA.get_vega()
        MC_price = MCPricer(optionBA, drift, 100).get_price()

        # output
        print(f"under the input assumptions,\n"
              f"delta is {Delta},\n"
              f"gamma is {Gamma},\n"
              f"Vega is {Vega},\n"
              f"Monte Carlo Simulation price is {MC_price}")

    elif option_class == "american":
        pass

























