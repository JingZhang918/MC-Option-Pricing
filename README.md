# Monte Carlo Option Pricing Engine

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li> <a href="#ABOUT THE PROJECT">About This Project</a>
    <li> <a href="#Set up environment">Set up environment</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#Logic">Logic</a></li>
        <li><a href="#Assumptions">Assumptions</a></li>
        <li><a href="#Limitations">Limitations</a></li>
        <li><a href="#Future Improvements">Future Improvements</a></li>
      </ul>
    </li>
    <li><a href="#Backend algorithm logic">Backend algorithm logic !!!</a></li>
      <ul>
        <li><a href="#Shortcomings and future improvements">Shortcomings and Future Improvements</a></li>
      </ul>
    <li><a href="#Guide on adding more options">Guide on adding more options</a></li>
    <li><a href="#Future Application">Future Application !!!!</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About this project

This project is used for pricing options through **Monte Carlo Simulation**. Current 
supported option types are **European option** and **Barrier option**. 

Two applications are provided: web app and exe app. Currently, both user interfaces only accepts
European option. 

The following are web app GUI and exe app GUI respectively.

<img src="./images/web_app.png" alt="Web App GUI" width="50%" height="50%"/>

<img src="./images/exe_app.png" alt="Exe App GUI" width="50%" height="50%"/>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Set up environment -->
## Set up environment

To set up environment for both apps, you can run the following code in your terminal.
```
# create environment
conda create -n ope python=3.9
conda activate ope

# install necessary packages (dependencies)
pip install flask yfinance yahoo_fin scipy
# conda install -c conda-forge scipy -y # for apple M1 user

## To use Web APP
python app.py 
# open http://127.0.0.1:5000/ in your browser

## To use EXE APP
python gui.py
```
Note: the web app is not responsive, please report bug if something abnormal happened.

You can also convert .py file into .exe file by:
```
pip install auto-py-to-exe
auto-py-to-exe
```
with the following configuration:

<img src="./images/auto_py_to_exe.png" alt="Auto py to Exe configuration" width="50%" height="50%"/>

Then there is no need to set up environment for this Exe App. 


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- usage -->
## Usage

To run exe app, you can simply double-click
the exe file under directory ```output```
![Exe app directory](./images/output.png)

or if you didn't convert .py to .exe, you can simply run:
```
python gui.py
```

Then the GUI will pop up.

<img src="./images/exe_app.png" alt="Exe App GUI" width="50%" height="50%"/>

To use Web App, in the terminal, run:
```
python app.py
```
and open http://127.0.0.1:5000/ in your browser, you will see:

<img src="./images/web_app.png" alt="Web App GUI" width="50%" height="50%"/>

To price both European and Barrier Options, please run
```
python run.py
```
Then change the parameters here:
```
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
    volatility = 2
    drift = .1
    continuous_yield = 0
    MC_simulation = 1000
# =================================================================================
```


<!-- Logic -->
### Logic

**The option you want to price can be found here: https://finance.yahoo.com/.** Input ticker AAPL is
the same as input ticker AAPL in the search bar of this website. Under the option tag, you can see
call (in/out of money) and put (in/out of money) European Options with features such as contract
name, last trade date, strike and so on. The default setting is to price the **first** option (the 
option with the smallest contract name)

The following graph shows the screenshot of the current Apple Inc.'s options.

<img src="./images/aapl_options.png" alt="AAPL Options" width="50%" height="50%"/>

<!-- Assumptions -->
### Assumptions:

* The underlying follows a statistical process called geometric Brownian motion, which implies 
that the continuously compounded return is normally distributed.
* Geometric Brownian motion implies continuous prices, meaning that the price of underlying 
instrument does not jump from one value to another; rather, it moves smoothly from value to value.
* The underlying instrument is liquid, meaning that it can be easily bought and sold.
* Continuous trading is available, meaning that in the strictest sense one must be able to trade 
at every instant.
* There are no market frictions, such as transaction costs, regulatory constraints, or taxes.
* No arbitrage opportunities are available in the marketplace.
* The continuously compounded risk-free interest rate is known and constant; borrowing and lending
is allowed at the risk-free rate.
* The volatility of the return on the underlying is known and constant.
* If the underlying instrument pays a yield, it is expressed as a continuous known and constant 
yield at an annualized rate.
*Intraday underlying values are not considered, but only the close value


<!-- Limitations -->
### Limitations:

- Both portal only support European option pricing (Barrier Option is **not** supported)
- No data integrity check, meaning wrong type or wrong format can easily break the application
- only one option under call/put tag is valued.

<!-- Future Improvements -->
### Future Improvements:

- Add data integrity checking, e.g. only integer is allowed for Monte Carlo Simulation steps. 
- Use selection box for some inputs, e.g. Option Type can only be chosen as either call or put.
- Add Barrier Option pricing function
- Allow more kinds of options, such as Bermuda, Asian, Rainbow
- Value more options once, e.g. all in-the-money call options.
- better looking GUI
- Make Web APP GUI responsive.


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Backend algorithm logic -->
## Backend Algorithm Logic (IMPORTANT‼️‼️‼️‼️‼️‼️‼ )

<!-- Shortcomings and future improvements -->
### Shortcomings and Future Improvements:

- Calculating Greeks through Monte Carlo Simulation is by definition. 
  - By definition, delta is the amount an option price is expected to move based on a $1 move up in the underlying given everything else stays
  the same. As a result, delta = price(s+1, mu, sigma, n, m) - price(s, mu, sigma, n, m)
  - Gamma is the rate of change in delta based on $1 change in the price of the underlying. Hence,
  gamma = price(s+2, mu, sigma, n, m) - price(s, mu, sigma, n, m) - 2*delta
  - Vega is the amount call & put prices will change for every 1% change in implied volatility. As a
  result, vega = price(s, mu, sigma+.01, n, m) - price(s, mu, sigma, n, m)
- **The unittest is not necessarily right.** For the lack of confidence, I used my own output as the
standard to pass all the unittest. (But I've read every entry. It seems great.) I tried the standard library ```option-price```, the results are
different, but I think mine is right. I also want to try library ```QuantLib``` and ```p4f``` to
get a second opinion. But due to the unfortunate fact that my M1 Mac has no access to those via
pip. As a result, after 4 hours of trying to install via wheel, I failed and gave up.
- **Add unittest logic**: the premium of European option should be larger than that of Barrier Option

<!-- Guide on adding more options -->
## Guide on adding more options 

I have left interfaces to add more options in the file ```financial_instruments.py``` and 
```MCPricer.py```. Just locate the example code, change the class name and the corresponding 
transaction regulations. 

The interface in the file ```financial_instruments.py```:
```
class rainbowOption(baseOption):
    def __init__(self):
        super(baseOption, self).__init__()
```

The interface in the file ```MCPricer.py```:
```
    elif self.option_class == "rainbow":
        pass
```

<!-- Future Application -->
## Future Application ‼️‼️‼️‼️‼️‼️‼️‼️

- Study option trading strategies, such as Covered Call, Married Put, Bull Call Spread, Bear Put Spread,
Protective Collar, Long Straddle, Long Strangle, Long Call Butterfly Spread, Iron Condor, and Iron Butterfly
- create an automated stock and option trading strategies. Combining my current stock trading algorithm along with 
different option trading strategies such as Protective Collar, Iron Condor and so on.

<!-- Contact -->
## Contact

Any ideas you wanna share with me, just send me an email: jingzhang6057@gmail.com :D

<p align="right">(<a href="#top">back to top</a>)</p>