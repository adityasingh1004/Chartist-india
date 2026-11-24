"""Offline tests: synthetic prices only, no network. Run with:  python -m unittest discover tests"""

import json
import math
import os
import random
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [ROOT, os.path.join(ROOT, "chartist")]

import engine  # noqa: E402
import universe  # noqa: E402


def synthetic_bars(n=700, seed=7, start=1000.0):
    rnd = random.Random(seed)
    import datetime as dt
    d, p, out = dt.date(2023, 1, 2), start, []
    while len(out) < n:
        if d.weekday() < 5:
            q = p * math.exp(rnd.gauss(0.0003, 0.015))
            hi, lo = max(p, q) * (1 + abs(rnd.gauss(0, .004))), min(p, q) * (1 - abs(rnd.gauss(0, .004)))
            out.append({"t": d.isoformat(), "o": round(p, 2), "h": round(hi, 2), "l": round(lo, 2), "c": round(q, 2),
                        "v": float(rnd.randint(100000, 900000))})
            p = q
        d += dt.timedelta(days=1)
    return out


class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bars = synthetic_bars()
        cls.bench = {b["t"]: b["c"] for b in synthetic_bars(seed=11, start=20000.0)}
        cls.r = engine.analyse(cls.bars, cls.bench, "DEMO", "synthetic")

    def test_shape(self):
        for k in ("verdict", "trend", "momentum", "levels", "patterns", "signals", "scorecard", "params"):
            self.assertIn(k, self.r)
        self.assertIn(self.r["verdict"]["bias"], ["Bearish", "Mildly bearish", "Neutral / range", "Mildly bullish", "Bullish"])
        json.dumps(self.r, default=str)                   # serialisable for the web page

    def test_too_short(self):
        with self.assertRaises(ValueError):
            engine.analyse(self.bars[:30])

    def test_params_clamped(self):
        p = engine.clean_params({"ema_fast": 60, "ema_slow": 50, "rsi_n": 9999, "bb_k": "x", "junk": 1})
        self.assertEqual((p["ema_fast"], p["ema_slow"]), (20, 50))   # invalid pair falls back to defaults
        self.assertEqual(p["rsi_n"], 400)
        self.assertEqual(p["bb_k"], 2.0)
        self.assertNotIn("junk", p)

    def test_custom_params_change_output(self):
        r2 = engine.analyse(self.bars, self.bench, "DEMO", params={"ema_fast": 10, "ema_slow": 30})
        self.assertEqual(r2["params"]["ema_fast"], 10)


class UniverseTests(unittest.TestCase):
    def test_parse_nse(self):
        csv_text = "SYMBOL,NAME OF COMPANY, SERIES, DATE OF LISTING, PAID UP VALUE, MARKET LOT, ISIN NUMBER, FACE VALUE\n" \
                   "RELIANCE,Reliance Industries Limited,EQ,29-NOV-1995,10,1,INE002A01018,10\n"
        rows = universe.parse_nse(csv_text)
        self.assertEqual(rows[0]["s"], "RELIANCE")
        self.assertEqual(rows[0]["isin"], "INE002A01018")

    def test_parse_bse_skips_inactive(self):
        doc = json.dumps([{"SCRIP_CD": "1", "Scrip_Name": "A", "Status": "Active", "scrip_id": "AAA", "ISIN_NUMBER": "X1"},
                          {"SCRIP_CD": "2", "Scrip_Name": "B", "Status": "Delisted", "scrip_id": "BBB", "ISIN_NUMBER": "X2"}])
        self.assertEqual([r["sid"] for r in universe.parse_bse(doc)], ["AAA"])

    def test_glb_id_windows_safe(self):
        self.assertEqual(universe.glb_id("BZ=F"), "GLB_BZ_F")
        self.assertEqual(universe.glb_id("^TNX"), "GLB_TNX")


class CalibrationTests(unittest.TestCase):
    def test_group_of(self):
        import calibrate
        tiers = {"Nifty 100": ["TCS"], "Smallcap 250": ["TINY"]}
        g = lambda i: calibrate.group_of(i, tiers, {"MIDX"})
        self.assertEqual(g({"s": "TCS", "x": "NSE"}), "Nifty 100")
        self.assertEqual(g({"s": "TINY", "x": "NSE"}), "Smallcap 250")
        self.assertEqual(g({"s": "MIDX", "x": "NSE"}), "Nifty 500 (tier unknown)")
        self.assertEqual(g({"s": "OTHER", "x": "NSE"}), "NSE outside Nifty 500")
        self.assertEqual(g({"s": "SMEX", "x": "NSE SME"}), "NSE SME")
        self.assertEqual(g({"s": "BSE_ABC", "x": "BSE"}), "BSE-only")
        self.assertEqual(g({"s": "GLB_TNX", "k": "yield"}), "Global yield")

    def test_summarise_too_few_and_gap(self):
        import calibrate
        rows = [("A", "G", "2020-01-%02d" % (i % 28 + 1), "Bullish" if i % 2 else "Bearish", 0, 0, 0, 0,
                 0.05 if i % 2 else 0.0, False) for i in range(40)]
        s = calibrate.summarise(rows)
        self.assertAlmostEqual(s["bull_minus_bear_x60"], 5.0)
        self.assertEqual(s["finding"], "too few")


if __name__ == "__main__":
    unittest.main()
