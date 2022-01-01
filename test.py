import unittest
from financial_instruments import europeanOption, barrierOption
from MCPricer import MCPricer

class MyTestCase(unittest.TestCase):

    # european option test
    def test_european_option(self):
        #parameters
        r = .01
        S = 30
        K = 40
        T = 240 / 365
        sigma = .3
        drift = .1
        N = 100 #simulation steps

        optionEU = europeanOption()
        optionEU.S = S
        optionEU.sigma = sigma
        optionEU.K = K
        optionEU.T = T
        optionEU.r = r
        optionEU.q = 0
        optionEU.get_d1_d2()
        optionEU.type = "call"

        self.assertAlmostEqual(optionEU.BSPricer(), 0.5132843798399405)
        self.assertAlmostEqual(optionEU.get_vega(), 5.686707929045142)
        self.assertAlmostEqual(optionEU.get_gamma(), 0.03203161102008452)
        self.assertAlmostEqual(optionEU.get_delta(), 0.15058613984880015)
        self.assertGreater(optionEU.get_delta(), 0)
        self.assertAlmostEqual(MCPricer(optionEU, drift, N).get_price(), 0.931311142005521)

        optionEU.type = "put"
        self.assertAlmostEqual(optionEU.BSPricer(), 10.251133491653508)
        self.assertAlmostEqual(optionEU.get_delta(), -0.8494138601511998)
        self.assertLess(optionEU.get_delta(), 0)
        self.assertAlmostEqual(MCPricer(optionEU, drift, N).get_price(), 9.10040511686146)

    # barrier option test
    def test_barrier_option(self):
        #parameters
        r = .01
        S = 30
        K = 40
        T = 240 / 365
        sigma = .3
        drift = .1
        N = 100 #simulation steps

        #barrier type up-in
        barrier = 42
        barrier_type = "up-in"
        optionBA = barrierOption(barrier, barrier_type)
        # initialize parameters
        optionBA.barrier = barrier
        optionBA.barrier_type = barrier_type
        optionBA.S = S
        optionBA.sigma = sigma
        optionBA.K = K
        optionBA.T = T
        optionBA.r = r
        optionBA.q = 0
        optionBA.type = "call"
        optionBA.get_d1_d2()

        self.assertAlmostEqual(MCPricer(optionBA, drift, N).get_price(), 0.0)

        optionBA.type = "put"
        self.assertAlmostEqual(MCPricer(optionBA, drift, N).get_price(), 0.0)


        # barrier type up-out
        barrier = 42
        barrier_type = "up-out"
        optionBA = barrierOption(barrier, barrier_type)
        # initialize parameters
        optionBA.barrier = barrier
        optionBA.barrier_type = barrier_type
        optionBA.S = S
        optionBA.sigma = sigma
        optionBA.K = K
        optionBA.T = T
        optionBA.r = r
        optionBA.q = 0
        optionBA.type = "call"
        optionBA.get_d1_d2()

        self.assertAlmostEqual(MCPricer(optionBA, drift, N).get_price(), 0.3289026040563393)

        optionBA.type = "put"
        self.assertAlmostEqual(MCPricer(optionBA, drift, N).get_price(), 38.22879138380772)

        # barrier type down-in
        barrier = 38
        barrier_type = "down-in"
        optionBA = barrierOption(barrier, barrier_type)
        # initialize parameters
        optionBA.barrier = barrier
        optionBA.barrier_type = barrier_type
        optionBA.S = S
        optionBA.sigma = sigma
        optionBA.K = K
        optionBA.T = T
        optionBA.r = r
        optionBA.q = 0
        optionBA.type = "call"
        optionBA.get_d1_d2()

        self.assertAlmostEqual(MCPricer(optionBA, drift, N).get_price(), 0.0)

        optionBA.type = "put"
        self.assertAlmostEqual(MCPricer(optionBA, drift, N).get_price(), 39.504540358128786)

        # barrier type down-out
        barrier = 38
        barrier_type = "down-out"
        optionBA = barrierOption(barrier, barrier_type)
        # initialize parameters
        optionBA.barrier = barrier
        optionBA.barrier_type = barrier_type
        optionBA.S = S
        optionBA.sigma = sigma
        optionBA.K = K
        optionBA.T = T
        optionBA.r = r
        optionBA.q = 0
        optionBA.type = "call"
        optionBA.get_d1_d2()

        self.assertAlmostEqual(MCPricer(optionBA, drift, N).get_price(), 0.0)

        optionBA.type = "put"
        self.assertAlmostEqual(MCPricer(optionBA, drift, N).get_price(), 0.0)

if __name__ == '__main__':
    unittest.main()
