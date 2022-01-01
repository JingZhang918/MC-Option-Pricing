from flask import Flask, request, jsonify, render_template
from MCPricer import MCPricer
from financial_instruments import europeanOption, barrierOption
import numpy as np
np.random.seed(0)
from yahoo_fin import options
import yfinance as yf
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    values = list(request.form.values())

    ticker = values[0]
    expiration_date = values[1]
    option_class = values[2]
    option_type = values[3]
    risk_free_rate = float(values[4])
    volatility = float(values[5])
    drift = float(values[6])
    continuous_yield = float(values[7])
    MC_simulation = int(values[8])

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

    # output
    return render_template('index.html', prediction_text=prediction_text)

#
# @app.route('/predict_api',methods=['POST'])
# def predict_api():
#     '''
#     For direct API calls through request
#     '''
#     data = request.get_json(force=True)
#     # prediction = model.predict([np.array(list(data.values()))])
#     prediction = [0, 1]
#     output = prediction[0]
#     return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)


