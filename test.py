import unittest
from financial_instruments import europeanOption, barrierOption
from MCPricer import MCPricer

class MyTestCase(unittest.TestCase):

    # european option test
    def test_european_option(self):

        optionEU = europeanOption()
        optionEU.sigma = .3
        optionEU.K = 40
        optionEU.T = 7/365
        optionEU.r = .01
        optionEU.q = 0

        drift = .1
        N = 10 #simulation steps

        # MC pricer
        optionEU.S = 38
        optionEU.type = "call"
        [price, delta, gamma, vega] = MCPricer(optionEU, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 7.4155541306977835)
        self.assertTrue(0 <= delta <= 1)
        self.assertTrue(vega >= 0)
        optionEU.type = "put"
        [price, delta, gamma, vega] = MCPricer(optionEU, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 4.94932879566411)
        self.assertTrue(-1 <= delta <= 0)
        self.assertTrue(vega >= 0)

        optionEU.S = 42
        optionEU.type = "call"
        [price, delta, gamma, vega] = MCPricer(optionEU, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 10.040123830350968)
        self.assertTrue(0 <= delta <= 1)
        self.assertTrue(vega >= 0)
        optionEU.type = "put"
        [price, delta, gamma, vega] = MCPricer(optionEU, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 3.1045729234458883)
        self.assertTrue(-1 <= delta <= 0)
        self.assertTrue(vega >= 0)

        # Black Scholes Model
        optionEU.S = 38
        optionEU.type = "call"
        [price, delta, gamma, vega] = optionEU.get_BS_price_greeks()
        self.assertAlmostEqual(price, 0.08539668795131128)
        self.assertTrue(0 <= delta <= 1)
        self.assertTrue(vega >= 0)
        optionEU.type = "put"
        [price, delta, gamma, vega] = optionEU.get_BS_price_greeks()
        self.assertAlmostEqual(price, 2.077726190625249)
        self.assertTrue(-1 <= delta <= 0)
        self.assertTrue(vega >= 0)

        optionEU.S = 42
        optionEU.type = "call"
        [price, delta, gamma, vega] = optionEU.get_BS_price_greeks()
        self.assertAlmostEqual(price, 2.107370356043525)
        self.assertTrue(0 <= delta <= 1)
        self.assertTrue(vega >= 0)
        optionEU.type = "put"
        [price, delta, gamma, vega] = optionEU.get_BS_price_greeks()
        self.assertAlmostEqual(price, 0.09969985871746534)
        self.assertTrue(-1 <= delta <= 0)
        self.assertTrue(vega >= 0)


    # # barrier option test
    def test_barrier_option(self):

        #parameters
        optionBA = barrierOption(42, "up-in")
        optionBA.S = 38
        optionBA.sigma = .3
        optionBA.K = 40
        optionBA.T = 7 / 365
        optionBA.r = .01
        optionBA.q = 0
        optionBA.type = "call"
        # optionBA.get_d1_d2()

        drift = .1
        N = 10 #simulation steps

        [price, delta, gamma, vega] = MCPricer(optionBA, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 7.4155541306977835)
        self.assertTrue(0 <= delta <= 1)
        self.assertTrue(vega >= 0)
        optionBA.type = "put"
        [price, delta, gamma, vega] = MCPricer(optionBA, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 0.6626594883295722)
        self.assertTrue(-1 <= delta <= 0)
        self.assertTrue(vega >= 0)

        optionBA.barrier_type = "up-out"
        optionBA.type = "call" # only profit if st between [40,42]
        [price, delta, gamma, vega] = MCPricer(optionBA, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 0.0)
        self.assertTrue(0 <= delta <= 1)
        self.assertTrue(vega >= 0)
        optionBA.type = "put"
        [price, delta, gamma, vega] = MCPricer(optionBA, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 4.286669307334537)
        self.assertTrue(-1 <= delta <= 0)
        self.assertTrue(vega >= 0)

        optionBA.S = 42
        optionBA.barrier = 38
        optionBA.barrier_type = "down-in"
        optionBA.type = "call"
        [price, delta, gamma, vega] = MCPricer(optionBA, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, .0)
        self.assertTrue(0 <= delta <= 1)
        self.assertTrue(vega >= 0)
        optionBA.type = "put"
        [price, delta, gamma, vega] = MCPricer(optionBA, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 3.054008493464713)
        self.assertTrue(-1 <= delta <= 0)
        self.assertTrue(vega >= 0)

        optionBA.barrier_type = "down-out"
        optionBA.type = "call"
        [price, delta, gamma, vega] = MCPricer(optionBA, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 10.040123830350968)
        self.assertTrue(0 <= delta <= 1)
        self.assertTrue(vega >= 0)
        optionBA.type = "put"
        [price, delta, gamma, vega] = MCPricer(optionBA, drift, N).get_price_greeks()
        self.assertAlmostEqual(price, 0.050564429981175496)
        self.assertTrue(-1 <= delta <= 0)
        self.assertTrue(vega >= 0)



if __name__ == '__main__':
    unittest.main()
