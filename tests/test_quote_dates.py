import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from providers import gather


class QuoteDateTests(unittest.TestCase):
    def test_actual_observation_date_survives_refresh(self):
        frame = pd.DataFrame({"Close": [100.0, 110.0]}, index=pd.to_datetime(["2026-09-29", "2026-09-30"]))
        fake = SimpleNamespace(download=lambda **kwargs: frame)
        with patch.dict(sys.modules, {"yfinance": fake}):
            quote = gather({"indices": [{"symbol": "TEST", "label": "Test"}]})["quotes"][0]
        self.assertEqual(quote["price_observation_date"], "2026-09-30")
        self.assertEqual(quote["change_pct"], 10.0)

    def test_nonfinite_zero_price_or_no_previous_close_is_not_faked(self):
        for closes in [[100.0, float("inf")], [100.0, 0.0], [100.0]]:
            frame = pd.DataFrame({"Close": closes}, index=pd.date_range("2026-09-29", periods=len(closes)))
            with patch.dict(sys.modules, {"yfinance": SimpleNamespace(download=lambda frame=frame, **kwargs: frame)}):
                self.assertEqual(gather({"indices": [{"symbol": "TEST"}]})["quotes"], [])

    def test_future_observation_is_rejected(self):
        frame = pd.DataFrame({"Close": [100.0, 110.0]}, index=pd.to_datetime(["2099-01-01", "2099-01-02"]))
        with patch.dict(sys.modules, {"yfinance": SimpleNamespace(download=lambda **kwargs: frame)}):
            self.assertEqual(gather({"indices": [{"symbol": "TEST"}]})["quotes"], [])


if __name__ == "__main__":
    unittest.main()
