from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest

from monitor import (
    DEFAULT_AGENTTXGUARD_URL,
    DEFAULT_SOLANA_RPC_URL,
    check_agenttxguard,
    check_solana_rpc,
)


app = FastAPI(
    title="Solana Observability Stack",
    description="Prometheus metrics server for Solana RPC and AgentTxGuard health.",
    version="0.1.0",
)


SOLANA_RPC_UP = Gauge("solana_rpc_up", "Whether Solana RPC is healthy: 1 up, 0 down.")
SOLANA_RPC_SLOT = Gauge("solana_rpc_slot", "Latest observed Solana slot.")
SOLANA_RPC_LATENCY = Gauge("solana_rpc_latency_seconds", "Latency for Solana RPC checks.")

AGENTTXGUARD_UP = Gauge("agenttxguard_up", "Whether AgentTxGuard is healthy: 1 up, 0 down.")
AGENTTXGUARD_LATENCY = Gauge(
    "agenttxguard_health_latency_seconds",
    "Latency for AgentTxGuard health endpoint.",
)

MONITOR_CHECK_TOTAL = Counter(
    "monitor_check_total",
    "Total monitor checks performed.",
    ["target"],
)

MONITOR_CHECK_ERRORS_TOTAL = Counter(
    "monitor_check_errors_total",
    "Total failed monitor checks.",
    ["target"],
)


def get_config() -> Dict[str, str]:
    return {
        "solana_rpc_url": os.getenv("SOLANA_RPC_URL", DEFAULT_SOLANA_RPC_URL),
        "agenttxguard_url": os.getenv("AGENTTXGUARD_URL", DEFAULT_AGENTTXGUARD_URL),
        "agenttxguard_api_key_configured": str(bool(os.getenv("AGENTTXGUARD_API_KEY"))),
    }


def run_checks() -> Dict[str, Any]:
    config = get_config()

    solana = check_solana_rpc(config["solana_rpc_url"])
    agenttxguard = check_agenttxguard(
        config["agenttxguard_url"],
        api_key=os.getenv("AGENTTXGUARD_API_KEY"),
    )

    MONITOR_CHECK_TOTAL.labels(target="solana_rpc").inc()
    MONITOR_CHECK_TOTAL.labels(target="agenttxguard").inc()

    SOLANA_RPC_UP.set(1 if solana.ok else 0)
    SOLANA_RPC_LATENCY.set(solana.latency_seconds)

    slot = solana.details.get("slot")
    if isinstance(slot, int):
        SOLANA_RPC_SLOT.set(slot)

    if not solana.ok:
        MONITOR_CHECK_ERRORS_TOTAL.labels(target="solana_rpc").inc()

    AGENTTXGUARD_UP.set(1 if agenttxguard.ok else 0)
    AGENTTXGUARD_LATENCY.set(agenttxguard.latency_seconds)

    if not agenttxguard.ok:
        MONITOR_CHECK_ERRORS_TOTAL.labels(target="agenttxguard").inc()

    return {
        "config": config,
        "solana_rpc": asdict(solana),
        "agenttxguard": asdict(agenttxguard),
    }


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "name": "Solana Observability Stack",
        "status": "running",
        "health": "/health",
        "checks": "/checks",
        "metrics": "/metrics",
    }


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/checks")
def checks() -> Dict[str, Any]:
    return run_checks()


@app.get("/metrics")
def metrics() -> Response:
    run_checks()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)