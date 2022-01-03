import numpy as np
from scipy import stats

class baseOption():
    def __init__(self, underlying_price, volatility, strike_price, time_to_expiration, risk_free_rate, continuous_yield, type="call"):
        '''
        :param underlying_price: S
        :param volatility: sigma
        :param strike_price: K
        :param time_to_expiration: T (days)
        :param risk_free_rate: r
        :param continuous_yield: q
        :param type:  call/put
        '''
        self.S = underlying_price
        self.sigma = volatility
        self.K = strike_price
        self.T = time_to_expiration/365 # to percentage of year
        self.r = risk_free_rate
        self.q = continuous_yield
        self.type = type

    def get_BS_price_greeks(self):

        d1 = (np.log(self.S/self.K)+(self.r-self.q+np.power(self.sigma,2)/2)*self.T)/(self.sigma*np.sqrt(self.T))
        d2 = d1 - self.sigma*np.sqrt(self.T)
        gamma = np.exp(-self.q*self.T)*stats.norm.pdf(d1)/(self.S*self.sigma*np.sqrt(self.T))
        vega = np.exp(-self.q*self.T)*self.S*np.sqrt(self.T)*stats.norm.pdf(d1)

        if self.type == "call":
            price = self.S*np.exp(-self.q*self.T)*stats.norm.cdf(d1) - self.K*np.exp(-self.r*self.T)*stats.norm.cdf(d2)
            delta = np.exp(-self.q*self.T)*stats.norm.cdf(d1)
        else:
            price = self.K*np.exp(-self.r*self.T)*stats.norm.cdf(-d2) - self.S*np.exp(-self.q*self.T)*stats.norm.cdf(-d1)
            delta = -np.exp(-self.q*self.T)*stats.norm.cdf(-d1)

        return [price, delta, gamma, vega]


    def get_payoff(self, predicted_price):
        if self.type == "call":
            return np.clip(predicted_price - self.K, a_min=0, a_max=np.inf)
        else:
            return np.clip(self.K - predicted_price, a_min=0, a_max=np.inf)


class europeanOption(baseOption):

    def __init__(self, option_class = "european"):
        self.option_class = option_class
        super(baseOption, self).__init__()


class barrierOption(baseOption):

    def __init__(self, barrier, barrier_type, option_class="barrier"):
        '''
        :param barrier: float
        :param barrier_type: UpIn, UpOut, DownIn, DownOut
        '''
        self.option_class = option_class
        self.barrier = barrier
        self.barrier_type = barrier_type
        super(baseOption, self).__init__()


class rainbowOption(baseOption):
    def __init__(self):
        super(baseOption, self).__init__()
