import numpy as np
from scipy import stats

class baseOption():
    def __init__(self, underlying_price, volatility, strike_price, time_to_expiration, risk_free_rate, continuous_yield, type="call"):
        '''
        :param underlying_price: S
        :param volatility: sigma
        :param strike_price: X
        :param time_to_expiration: T (days)
        :param risk_free_rate: r
        :param continuous_yield: q
        :param barrier: b (barrier option)
        :param type:  call/put
        '''
        self.S = underlying_price
        self.sigma = volatility
        self.K = strike_price
        self.T = time_to_expiration/365 # to percentage of year
        self.r = risk_free_rate
        self.q = continuous_yield
        self.type = type

    def get_d1_d2(self):
        self.d1 = (np.log(self.S/self.K)+(self.r-self.q+np.power(self.sigma,2)/2)*self.T)/(self.sigma*np.sqrt(self.T))
        self.d2 = self.d1 - self.sigma*np.sqrt(self.T)

    def BSPricer(self):

        if self.type == "call":
            self.price = self.S*np.exp(-self.q*self.T)*stats.norm.cdf(self.d1) - self.K*np.exp(-self.r*self.T)*stats.norm.cdf(self.d2)
        elif self.type == "put":
            self.price = self.K*np.exp(-self.r*self.T)*stats.norm.cdf(-self.d2) - self.S*np.exp(-self.q*self.T)*stats.norm.cdf(-self.d1)
        else:
            raise ValueError("invalid option type, please try 'call' or 'put'. ")
        return self.price

    def get_delta(self):
        if self.type == "call":
            self.Delta = np.exp(-self.q*self.T)*stats.norm.cdf(self.d1)
        elif self.type == "put":
            self.Delta = -np.exp(-self.q*self.T)*stats.norm.cdf(-self.d1)
        else:
            raise ValueError("invalid option type, please try 'call' or 'put'. ")
        return self.Delta

    def get_gamma(self):
        self.Gamma = np.exp(-self.q*self.T)*stats.norm.pdf(self.d1)/(self.S*self.sigma*np.sqrt(self.T))
        return self.Gamma

    def get_vega(self):
        self.Vega = np.exp(-self.q*self.T)*self.S*np.sqrt(self.T)*stats.norm.pdf(self.d1)
        return self.Vega

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

    # def get_delta(self):
    #     return 1
    #
    # def get_vega(self):
    #     return 1
    #
    # def get_gamma(self):
    #     return 1

class rainbowOption(baseOption):
    def __init__(self):
        super(baseOption, self).__init__()
    # def get_vega(self):
    #     pass
    # def get_gamma(self):
    #     pass
    # def get_delta(self):
    #     pass