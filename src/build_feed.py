"""Orchestration: ingest -> compute -> validate(schema) -> write out/."""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from providers import gather  # noqa: E402
from compute import build_board  # noqa: E402


def load_config() -> dict:
    return yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))


def load_schema() -> dict:
    return json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))


def build(cfg: dict) -> dict:
    raw = gather(cfg)
    board = build_board(raw.get("quotes", []), len(cfg.get("indices", []) or []))
    status = board.pop("_status")
    notes = board.pop("_notes", None)
    board["as_of"] = dt.date.today().isoformat()
    board["disclaimer"] = "Index levels from public market data, delayed. Informational only."

    feed = {
        "service": cfg["service"],
        "schema_version": str(cfg["schema_version"]),
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "status": status,
        "ttl_hours": cfg["ttl_hours"],
        "data": board,
    }
    if notes:
        feed["notes"] = notes
    return feed


def main() -> None:
    cfg = load_config()
    feed = build(cfg)
    jsonschema.validate(feed, load_schema())
    out = ROOT / "out"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index_ticker.json").write_text(json.dumps(feed, indent=2), encoding="utf-8")
    print(f"[index_ticker] status={feed['status']} indices={feed['data']['count']}")


if __name__ == "__main__":
    main()
