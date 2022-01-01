from tkinter import *
from MCPricer import MCPricer
from financial_instruments import baseOption, europeanOption, barrierOption
import numpy as np
np.random.seed(0)
from yahoo_fin import options
import yfinance as yf
from datetime import datetime


def price_option():

    ticker = ticker_var.get()
    expiration_date = expiration_date_var.get()
    option_class = option_class_var.get()
    option_type = option_type_var.get()
    risk_free_rate = float(risk_free_rate_var.get())
    volatility = float(volatility_var.get())
    drift = float(drift_var.get())
    continuous_yield = float(continuous_yield_var.get())
    MC_simulation = int(MC_simulation_var.get())

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
        optionEU.get_d1_d2()

        # calculate Greeks and prices under BSM and MC
        BSM_price = optionEU.BSPricer()
        Delta = optionEU.get_delta()
        Gamma = optionEU.get_gamma()
        Vega = optionEU.get_vega()
        MC_price = MCPricer(optionEU, drift, MC_simulation).get_price()

        # print(f"under the input assumptions, the black-scholes-merton price is {BSM_price},\n"
        #       f"delta is {Delta},\n"
        #       f"gamma is {Gamma},\n"
        #       f"Vega is {Vega},\n"
        #       f"Monte Carlo Simulation price is {MC_price}")

    elif option_class == "barrier":
        pass
        # optionBA = barrierOption(barrier, barrier_type)
        # # initialize parameters
        # optionBA.barrier = barrier
        # optionBA.barrier_type = barrier_type
        # optionBA.S = underlying_price
        # optionBA.sigma = volatility
        # optionBA.K = strike_price
        # optionBA.T = time_to_expiration
        # optionBA.r = risk_free_rate
        # optionBA.q = continuous_yield
        # optionBA.type = option_type
        # optionBA.get_d1_d2()
        #
        # Delta = optionBA.get_delta()
        # Gamma = optionBA.get_gamma()
        # Vega = optionBA.get_vega()
        # MC_price = MCPricer(optionBA, drift, 100).get_price()
        #
        # # output
        # print(f"under the input assumptions,\n"
        #       f"delta is {Delta},\n"
        #       f"gamma is {Gamma},\n"
        #       f"Vega is {Vega},\n"
        #       f"Monte Carlo Simulation price is {MC_price}")

    elif option_class == "american":
        pass

    prediction_text = f"under the input assumptions, \n" + \
                      f"the black-scholes-merton price is {round(BSM_price, 2)},\n" + \
                      f"delta is {round(Delta, 2)},\n" + \
                      f"gamma is {round(Gamma, 2)},\n" + \
                      f"Vega is {round(Vega, 2)},\n" + \
                      f"Monte Carlo Simulation price is {round(MC_price, 2)} \n\n"


    Output.insert(END, prediction_text)

    # ticker_entry.delete(0, END)


screen = Tk()
screen.geometry("500x500")
screen.title("Option Pricing")

ticker_label = Label(text="Ticker * (e.g. AAPL)", )
ticker_label.place(x=10, y=10)
ticker_var = StringVar()
ticker_entry = Entry(textvariable=ticker_var, width="20")
ticker_entry.place(x=280, y=10)

expiration_date_label = Label(text="Expiration Date * (e.g. January 7, 2022) ", )
expiration_date_label.place(x=10, y=40)
expiration_date_var = StringVar()
expiration_date_entry = Entry(textvariable=expiration_date_var, width="20")
expiration_date_entry.place(x=280, y= 40)

option_class_label = Label(text="Option Class * (european or barrier)", )
option_class_label.place(x=10, y=70)
option_class_var = StringVar()
option_class_entry = Entry(textvariable=option_class_var, width="20")
option_class_entry.place(x=280, y= 70)

option_type_label = Label(text="Option Type * (call or put)", )
option_type_label.place(x=10, y=100)
option_type_var = StringVar()
option_type_entry = Entry(textvariable=option_type_var, width="20")
option_type_entry.place(x=280, y= 100)

risk_free_rate_label = Label(text="Risk Free Rate *", )
risk_free_rate_label.place(x=10, y=130)
risk_free_rate_var = StringVar()
risk_free_rate_entry = Entry(textvariable=risk_free_rate_var, width="20")
risk_free_rate_entry.place(x=280, y= 130)

volatility_label = Label(text="Volatility *", )
volatility_label.place(x=10, y=160)
volatility_var = StringVar()
volatility_entry = Entry(textvariable=volatility_var, width="20")
volatility_entry.place(x=280, y= 160)

drift_label = Label(text="Drift *", )
drift_label.place(x=10, y=190)
drift_var = StringVar()
drift_entry = Entry(textvariable=drift_var, width="20")
drift_entry.place(x=280, y= 190)

continuous_yield_label = Label(text="Continuous Yield *", )
continuous_yield_label.place(x=10, y=220)
continuous_yield_var = StringVar()
continuous_yield_entry = Entry(textvariable=continuous_yield_var, width="20")
continuous_yield_entry.place(x=280, y= 220)

MC_simulation_label = Label(text="MC Simulation *", )
MC_simulation_label.place(x=10, y=250)
MC_simulation_var = StringVar()
MC_simulation_entry = Entry(textvariable=MC_simulation_var, width="20")
MC_simulation_entry.place(x=280, y= 250)

btn = Button(screen, text="Price Option", width="30", height="2", command=lambda: price_option(), bg="grey")
btn.place(x=100, y=290)

Output = Text(screen, height = 8, width = 65, bg = "light cyan")
Output.place(x=20, y = 350)

screen.mainloop()

