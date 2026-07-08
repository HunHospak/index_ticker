"""Ingest: major index quotes from Yahoo Finance (free, no key). Defensive."""
from __future__ import annotations

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
            tickers=symbols, period="5d", interval="1d",
            group_by="ticker", auto_adjust=False, progress=False, threads=True,
        )
    except Exception:
        return {"quotes": quotes}

    for sym in symbols:
        try:
            frame = data if len(symbols) == 1 else data[sym]
            closes = [float(v) for v in frame["Close"].dropna().tolist()]
        except Exception:
            continue
        if not closes:
            continue
        last = closes[-1]
        prev = closes[-2] if len(closes) >= 2 else last
        change_pct = ((last - prev) / prev * 100.0) if prev else 0.0
        quotes.append({
            "symbol": sym,
            "label": label_by_symbol.get(sym, sym),
            "price": round(last, 2),
            "change_pct": round(change_pct, 2),
        })
    return {"quotes": quotes}
