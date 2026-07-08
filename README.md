# index_ticker

Independent ArkenLabs satellite that publishes major index levels (S&P 500, Nasdaq, Dow,
Russell 2000, VIX, FTSE, DAX, Nikkei) from free Yahoo Finance data — for the site's marquee
ticker banner.

## Produces `out/index_ticker.json`

`data.indices`: `[{symbol, label, price, change_pct}]`, plus `as_of`, `count`.

## Freshness

Delayed market data, refreshed ~every 15 minutes during US market hours via GitHub Actions
(scheduled crons are best-effort and can be delayed a few minutes). The site marquee re-polls
the feed every ~30s but only ever shows the last published values — this is near-live, not a
real-time quote stream.

## Run locally

```bash
pip install -r requirements.txt
python src/build_feed.py
```

## Publish

GitHub Actions publishes `out/` to `gh-pages`. No secrets.

## Not investment advice

Informational, delayed index data.
