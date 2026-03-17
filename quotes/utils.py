import json
import time
from typing import Any


def now_ms() -> int:
    return int(time.time() * 1000)


def require_non_empty(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def as_float(value: Any, field_name: str) -> float:
    if value is None:
        raise ValueError(f"{field_name} must be numeric, got None")
    return float(value)


def as_int(value: Any, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} must be integer-like, got None")
    return int(value)


def compact_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
