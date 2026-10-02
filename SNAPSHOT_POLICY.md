# Market snapshot policy (2026-10-02)

Keep the existing US-market-hour and post-close schedules. Additional four-hourly
outside-hours/weekend builds refresh feed availability, NOT quote observation time.
Each quote now carries its actual Yahoo daily-bar `price_observation_date`.
A build on Sunday must not relabel Friday's bar as a Sunday price.

The consumer labels values as a market snapshot, never live quotes. Expired valid
feeds may be displayed only with a fixed delayed-data caption and feed timestamp;
malformed/unavailable feeds show a visible message without prices. The public TTL
is unchanged. Quote dates are displayed separately from feed update time.

Use one non-threaded Yahoo batch. Invalid/nonpositive prices, missing previous
closes and invalid/future observation dates are excluded, not replaced by a fake
zero change. Offline tests cover observation-date preservation and rejection paths.
GitHub scheduled execution can be delayed; the caption remains essential even with
the repaired scheduling coverage.
