import unittest

from src.inference import calculate_profit_loss_from_prices


class ProfitLossCalculatorTest(unittest.TestCase):
    def test_manual_profit_with_lots_and_default_fees(self):
        result = calculate_profit_loss_from_prices(
            ticker="BBCA.JK",
            buy_price=7600,
            sell_price=7800,
            lots=2,
        )

        self.assertEqual(result["status"], "PROFIT")
        self.assertEqual(result["quantity"]["shares"], 200)
        self.assertEqual(result["gross_buy_value"], 1520000)
        self.assertEqual(result["buy_fee"], 2280)
        self.assertEqual(result["sell_fee"], 3900)
        self.assertEqual(result["net_profit_loss"], 33820)
        self.assertAlmostEqual(result["net_return_pct"], 2.2217)
        self.assertEqual(result["breakeven_sell_price"], 7630.48)

    def test_manual_loss_with_shares(self):
        result = calculate_profit_loss_from_prices(
            ticker="BBRI.JK",
            buy_price=4200,
            sell_price=4100,
            shares=100,
        )

        self.assertEqual(result["status"], "LOSS")
        self.assertEqual(result["quantity"]["lots"], 1)
        self.assertLess(result["net_profit_loss"], 0)

    def test_rejects_ambiguous_quantity(self):
        with self.assertRaises(ValueError):
            calculate_profit_loss_from_prices(
                ticker="BMRI.JK",
                buy_price=5700,
                sell_price=5800,
                lots=1,
                shares=100,
            )


if __name__ == "__main__":
    unittest.main()
