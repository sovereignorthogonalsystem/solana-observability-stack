from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx


DEFAULT_SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
DEFAULT_AGENTTXGUARD_URL = "http://127.0.0.1:8000"


@dataclass
class CheckResult:
    name: str
    ok: bool
    latency_seconds: float
    details: Dict[str, Any]


def _elapsed(start: float) -> float:
    return round(time.perf_counter() - start, 6)


def check_solana_rpc(
    rpc_url: str = DEFAULT_SOLANA_RPC_URL,
    timeout_seconds: float = 5.0,
) -> CheckResult:
    start = time.perf_counter()

    try:
        with httpx.Client(timeout=timeout_seconds) as client:
            health_response = client.post(
                rpc_url,
                json={"jsonrpc": "2.0", "id": 1, "method": "getHealth"},
            )
            health_response.raise_for_status()
            health_data = health_response.json()

            slot_response = client.post(
                rpc_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "getSlot",
                    "params": [{"commitment": "processed"}],
                },
            )
            slot_response.raise_for_status()
            slot_data = slot_response.json()

        health_result = health_data.get("result")
        slot_result = slot_data.get("result")
        ok = health_result == "ok" and isinstance(slot_result, int)

        return CheckResult(
            name="solana_rpc",
            ok=ok,
            latency_seconds=_elapsed(start),
            details={
                "rpc_url": rpc_url,
                "health": health_result,
                "slot": slot_result,
            },
        )

    except Exception as exc:
        return CheckResult(
            name="solana_rpc",
            ok=False,
            latency_seconds=_elapsed(start),
            details={"rpc_url": rpc_url, "error": str(exc)},
        )


def check_agenttxguard(
    base_url: str = DEFAULT_AGENTTXGUARD_URL,
    timeout_seconds: float = 3.0,
    api_key: Optional[str] = None,
) -> CheckResult:
    start = time.perf_counter()

    headers = {}
    if api_key:
        headers["X-API-Key"] = api_key

    try:
        url = base_url.rstrip("/") + "/health"

        with httpx.Client(timeout=timeout_seconds) as client:
            response = client.get(url, headers=headers)

        response.raise_for_status()
        data = response.json()
        ok = data.get("status") == "ok"

        return CheckResult(
            name="agenttxguard",
            ok=ok,
            latency_seconds=_elapsed(start),
            details={"base_url": base_url, "health": data},
        )

    except Exception as exc:
        return CheckResult(
            name="agenttxguard",
            ok=False,
            latency_seconds=_elapsed(start),
            details={"base_url": base_url, "error": str(exc)},
        )