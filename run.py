from MCPricer import MCPricer
from financial_instruments import europeanOption, barrierOption
import numpy as np
np.random.seed(0)
from yahoo_fin import options
import yfinance as yf
from datetime import datetime

if __name__ == "__main__":

# =================================================================================
# parameters input area
# =================================================================================
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
    volatility = 1.5
    drift = .1
    continuous_yield = 0
    MC_simulation = 1000
# =================================================================================


    # start with one option
    if option_type == "call":
        option_lists = options.get_calls(ticker, expiration_date)
    else:
        option_lists = options.get_puts(ticker, expiration_date)
    option = option_lists.iloc[0]

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

        # calculate Greeks and prices under BSM and MC
        [price_bs, delta_bs, gamma_bs, vega_bs] = optionEU.get_BS_price_greeks()
        [price_mc, delta_mc, gamma_mc, vega_mc] = MCPricer(optionEU, drift, MC_simulation).get_price_greeks()

        print(f"under the input assumptions, \n"
              f"the MC simulation price is {price_mc},\n"
              f"delta is {delta_mc},\n"
              f"gamma is {gamma_mc},\n"
              f"Vega is {vega_mc},\n")

        print(f"under the input assumptions, \n"
              f"the BS price is {price_bs},\n"
              f"delta is {delta_bs},\n"
              f"gamma is {gamma_bs},\n"
              f"Vega is {vega_bs},\n")

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

        [price_mc, delta_mc, gamma_mc, vega_mc] = MCPricer(optionBA, drift, MC_simulation).get_price_greeks()

        print(f"under the input assumptions, \n"
              f"the MC simulation price is {price_mc},\n"
              f"delta is {delta_mc},\n"
              f"gamma is {gamma_mc},\n"
              f"Vega is {vega_mc},\n")

    elif option_class == "american":
        pass

























