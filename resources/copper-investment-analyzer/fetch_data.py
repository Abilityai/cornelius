#!/usr/bin/env python3
"""
Fetch current market data for all copper investment universe tickers.
Saves to market_data.json which the analyzer HTML loads on startup.

Usage:
    uv run --with yfinance fetch_data.py
    # or: pip install yfinance && python fetch_data.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    print("yfinance not found. Install with: pip install yfinance")
    print("  or run: uv run --with yfinance fetch_data.py")
    sys.exit(1)

# Map display ticker -> Yahoo Finance ticker
TICKERS = {
    # Major miners
    "FCX":    "FCX",
    "BHP":    "BHP",
    "SCCO":   "SCCO",
    "IVN":    "IVN.TO",
    "KGHM":   "KGH.WA",
    # Mid-cap miners
    "FM":     "FM.TO",
    "TECK.B": "TECK-B.TO",
    "HBM":    "HBM.TO",
    "ERO":    "ERO.TO",
    # ETFs
    "CPER":   "CPER",
    "COPX":   "COPX",
    "JJCTF":  "JJCTF",
    # Royalty/streaming
    "WPM":    "WPM",
    "FNV":    "FNV",
    # Equipment
    "CAT":    "CAT",
    "SAND":   "SAND.ST",
    "EPIR":   "EPIR-B.ST",
    # Recycling
    "Aurubis": "NDA.DE",
    # Hedge
    "AA":     "AA",
    # Copper futures
    "HG=F":   "HG=F",
}


def fmt_num(n):
    if n is None:
        return None
    if abs(n) >= 1e12:
        return f"${n/1e12:.1f}T"
    if abs(n) >= 1e9:
        return f"${n/1e9:.1f}B"
    if abs(n) >= 1e6:
        return f"${n/1e6:.0f}M"
    return f"${n:,.0f}"


def fetch_all():
    output = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "tickers": {},
    }

    print(f"Fetching {len(TICKERS)} tickers...\n")

    for display, yahoo in TICKERS.items():
        try:
            t = yf.Ticker(yahoo)
            info = t.info or {}
            hist = t.history(period="1y")

            price = info.get("currentPrice") or info.get("regularMarketPrice")
            prev_close = info.get("regularMarketPreviousClose")

            # YTD return
            ytd = None
            if not hist.empty:
                try:
                    yr = datetime.now().year
                    year_data = hist[hist.index.year == yr]
                    if not year_data.empty:
                        first = year_data.iloc[0]["Close"]
                        last = hist.iloc[-1]["Close"]
                        ytd = round((last - first) / first * 100, 2)
                except Exception:
                    pass

            # 1-month return
            m1 = None
            if not hist.empty and len(hist) >= 22:
                try:
                    m1_price = hist.iloc[-22]["Close"]
                    last_price = hist.iloc[-1]["Close"]
                    m1 = round((last_price - m1_price) / m1_price * 100, 2)
                except Exception:
                    pass

            record = {
                "price": round(price, 2) if price else None,
                "currency": info.get("currency", "USD"),
                "change_pct": round((price - prev_close) / prev_close * 100, 2) if price and prev_close else None,
                "market_cap": info.get("marketCap"),
                "market_cap_fmt": fmt_num(info.get("marketCap")),
                "pe_ratio": round(info.get("trailingPE"), 1) if info.get("trailingPE") else None,
                "forward_pe": round(info.get("forwardPE"), 1) if info.get("forwardPE") else None,
                "dividend_yield": round(info.get("dividendYield", 0) * 100, 2) if info.get("dividendYield") else None,
                "w52_high": info.get("fiftyTwoWeekHigh"),
                "w52_low": info.get("fiftyTwoWeekLow"),
                "ma_50": round(info.get("fiftyDayAverage"), 2) if info.get("fiftyDayAverage") else None,
                "ma_200": round(info.get("twoHundredDayAverage"), 2) if info.get("twoHundredDayAverage") else None,
                "ytd_return": ytd,
                "m1_return": m1,
                "beta": round(info.get("beta"), 2) if info.get("beta") else None,
                "avg_volume": info.get("averageVolume"),
            }

            # Technical signals
            if price and record["ma_50"] and record["ma_200"]:
                record["above_50ma"] = price > record["ma_50"]
                record["above_200ma"] = price > record["ma_200"]
                record["golden_cross"] = record["ma_50"] > record["ma_200"]

            # Distance from 52w high/low
            if price and record["w52_high"]:
                record["pct_from_high"] = round((price - record["w52_high"]) / record["w52_high"] * 100, 1)
            if price and record["w52_low"]:
                record["pct_from_low"] = round((price - record["w52_low"]) / record["w52_low"] * 100, 1)

            output["tickers"][display] = record
            status = f"${price}" if price else "no price"
            print(f"  {display:10s} {status}")

        except Exception as e:
            print(f"  {display:10s} FAILED: {e}")
            output["tickers"][display] = {"error": str(e)}

    # Save
    out_path = Path(__file__).parent / "market_data.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    ok = sum(1 for v in output["tickers"].values() if "error" not in v)
    print(f"\nDone. {ok}/{len(TICKERS)} tickers saved to {out_path}")
    return output


if __name__ == "__main__":
    fetch_all()
