import numpy as np
np.random.seed(0)
import math
# from financial_instruments import
# from scipy import stats

class MCPricer:
    def __init__(self, option, drift, M):
        self.mu = drift
        self.n = int(option.T * 365)  # number of steps (days)
        self.T = 1
        self.M = M  # num of sims
        self.S0 = option.S
        self.sigma = option.sigma
        self.r = option.r
        self.option_class = option.option_class
        self.option = option

    def GBM(self):
        dt = self.T / self.n
        St = np.exp(
            (self.mu - self.sigma ** 2 / 2) * dt + self.sigma * np.random.normal(0, np.sqrt(dt), size=(self.M, self.n)).T
        )
        St = np.vstack([np.ones(self.M), St])
        St = self.S0 * St.cumprod(axis=0)
        return St

    def get_price(self):
        simulation_paths = self.GBM()

        if self.option_class == "european":
            return np.average(self.option.get_payoff(simulation_paths[-1]) / (1 + self.r))

        elif self.option_class == "barrier":
            barrier = self.option.barrier
            barrier_type = self.option.barrier_type
            sum = 0
            if barrier_type == "up-in":
                for path in simulation_paths:
                    if path.any() > barrier: #knock in
                        sum += self.option.get_payoff(path[-1]) / (1 + self.r)
                return sum/self.M
            elif barrier_type == "up-out":
                for path in simulation_paths:
                    out = False
                    if path.any() > barrier: #knock out
                        out = True
                    if not out:
                        sum += self.option.get_payoff(path[-1]) / (1 + self.r)
                return sum/self.M
            elif barrier_type == "down-in":
                for path in simulation_paths:
                    if path.any() < barrier: # knock in
                        sum += self.option.get_payoff(path[-1]) / (1 + self.r)
                return sum/self.M
            elif barrier_type == "down-out":
                for path in simulation_paths:
                    out = False
                    if path.any() < barrier: # knock out
                        out = True
                    if not out:
                        sum += self.option.get_payoff(path[-1]) / (1 + self.r)
                return sum/self.M

            elif self.option_class == "asian":
                pass

            elif self.option_class == "american":
                pass

            elif self.option_class == "binary":
                pass

            elif self.option_class == "rainbow":
                pass









