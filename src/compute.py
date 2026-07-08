"""Pure computation for index_ticker. No I/O, unit-testable."""
from __future__ import annotations

from typing import Any, Dict, List


def build_board(quotes: List[Dict[str, Any]], expected: int) -> Dict[str, Any]:
    clean = [q for q in quotes if isinstance(q, dict) and q.get("price") is not None]
    if not clean:
        status, notes = "unavailable", "No index quotes available."
    elif expected and len(clean) < expected:
        status, notes = "partial", f"Only {len(clean)}/{expected} indices resolved."
    else:
        status, notes = "active", None
    return {
        "indices": clean,
        "count": len(clean),
        "_status": status,
        "_notes": notes,
    }
