import numpy as np
# np.random.seed(0)

class MCPricer:
    def __init__(self, option, drift, M):
        self.mu = drift
        self.n = option.T * 365  # number of steps (days)
        self.T = 1
        self.M = M  # num of sims
        self.S0 = option.S
        self.sigma = option.sigma
        self.r = option.r
        self.option_class = option.option_class
        self.option = option
        self.discount_factor = 1 / np.power((1 + self.r),self.n/365)
        self.sum = 0

    def get_paths(self, S0, mu, sigma, n, M):
        np.random.seed(0)
        dt = 1 / n
        St = np.exp(
            (mu - sigma ** 2 / 2) * dt + sigma * np.random.normal(0, np.sqrt(dt), size=(int(M), int(n))).T
        )
        St = np.vstack([np.ones(M), St])
        St = S0 * St.cumprod(axis=0)
        return St

    def get_price_greeks(self):
        self.sum = 0
        simulation_paths = self.get_paths(self.S0, self.mu, self.sigma, self.n, self.M)
        simulation_paths_delta = self.get_paths(self.S0+1, self.mu, self.sigma, self.n, self.M)
        simulation_paths_gamma = self.get_paths(self.S0+2, self.mu, self.sigma, self.n, self.M)
        simulation_paths_vega = self.get_paths(self.S0, self.mu, self.sigma+.01, self.n, self.M)

        if self.option_class == "european":
            price = np.average(self.option.get_payoff(simulation_paths[-1]) * self.discount_factor )
            price_delta = np.average(self.option.get_payoff(simulation_paths_delta[-1]) * self.discount_factor)
            price_gamma = np.average(self.option.get_payoff(simulation_paths_gamma[-1]) * self.discount_factor )
            price_vega = np.average(self.option.get_payoff(simulation_paths_vega[-1]) * self.discount_factor )

            delta = price_delta - price
            gamma = price_gamma - price - 2 * delta
            vega = price_vega - price

            return [price, delta, gamma, vega]

        elif self.option_class == "barrier":
            barrier = self.option.barrier
            barrier_type = self.option.barrier_type

            if barrier_type == "up-in":
                price = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths.T
                                if np.sum(path > barrier) > 0]) / self.M
                price_delta = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_delta.T
                                if np.sum(path > barrier) > 0]) / self.M
                price_gamma = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_gamma.T
                     if np.sum(path > barrier) > 0]) / self.M
                price_vega = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_vega.T
                     if np.sum(path > barrier) > 0]) / self.M

                delta = price_delta - price
                gamma = price_gamma - price - 2*delta
                vega = price_vega - price

                return [price, delta, gamma, vega]

            elif barrier_type == "up-out":
                price = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths.T
                                if np.sum(path > barrier) == 0]) / self.M
                price_delta = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_delta.T
                                if np.sum(path > barrier) == 0]) / self.M
                price_gamma = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_gamma.T
                                if np.sum(path > barrier) == 0]) / self.M
                price_vega = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_vega.T
                                if np.sum(path > barrier) == 0]) / self.M

                delta = price_delta - price
                gamma = price_gamma - price - 2*delta
                vega = price_vega - price

                return [price, delta, gamma, vega]


            elif barrier_type == "down-in":
                price = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths.T
                                if np.sum(path < barrier) > 0]) / self.M
                price_delta = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_delta.T
                                if np.sum(path < barrier) > 0]) / self.M
                price_gamma = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_gamma.T
                                if np.sum(path < barrier) > 0]) / self.M
                price_vega = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_vega.T
                                if np.sum(path < barrier) > 0]) / self.M

                delta = price_delta - price
                gamma = price_gamma - price - 2*delta
                vega = price_vega - price

                return [price, delta, gamma, vega]

            elif barrier_type == "down-out":
                price = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths.T
                                if np.sum(path < barrier) == 0]) / self.M
                price_delta = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_delta.T
                                if np.sum(path < barrier) == 0]) / self.M
                price_gamma = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_gamma.T
                                if np.sum(path < barrier) == 0]) / self.M
                price_vega = np.sum(
                    [self.option.get_payoff(path[-1]) * self.discount_factor for path in simulation_paths_vega.T
                                if np.sum(path < barrier) == 0]) / self.M

                delta = price_delta - price
                gamma = price_gamma - price - 2*delta
                vega = price_vega - price

                return [price, delta, gamma, vega]



            elif self.option_class == "asian":
                pass

            elif self.option_class == "american":
                pass

            elif self.option_class == "binary":
                pass

            elif self.option_class == "rainbow":
                pass




