"""Ingest: major index quotes from Yahoo Finance (free, no key). Defensive."""

from __future__ import annotations

import datetime as dt
import logging
import math
from typing import Any, Dict, List


def gather(cfg: Dict[str, Any]) -> Dict[str, Any]:
    indices = cfg.get("indices", []) or []
    symbols = [str(i["symbol"]) for i in indices if i.get("symbol")]
    label_by_symbol = {str(i["symbol"]): str(i.get("label") or i["symbol"]) for i in indices}
    quotes: List[Dict[str, Any]] = []
    if not symbols:
        return {"quotes": quotes}
    try:
        import yfinance as yf

        data = yf.download(
            tickers=symbols,
            period="5d",
            interval="1d",
            group_by="ticker",
            auto_adjust=False,
            progress=False,
            threads=False,
        )
    except Exception as exc:
        logging.getLogger(__name__).warning("Yahoo index batch failed: %s", type(exc).__name__)
        return {"quotes": quotes}

    for sym in symbols:
        try:
            frame = data if len(symbols) == 1 else data[sym]
            observed = frame["Close"].dropna()
            closes = [float(v) for v in observed.tolist()]
            observation_date = observed.index[-1].date()
            if not 2000 <= observation_date.year or observation_date > dt.datetime.now(dt.timezone.utc).date():
                continue
        except Exception:
            continue
        if len(closes) < 2 or any(not math.isfinite(v) or v <= 0 for v in closes[-2:]):
            continue
        last = closes[-1]
        prev = closes[-2]
        change_pct = (last - prev) / prev * 100.0
        quotes.append(
            {
                "symbol": sym,
                "label": label_by_symbol.get(sym, sym),
                "price": round(last, 2),
                "change_pct": round(change_pct, 2),
                "price_observation_date": observation_date.isoformat(),
            }
        )
    return {"quotes": quotes}
