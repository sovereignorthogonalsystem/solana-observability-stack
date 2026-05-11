# Solana Observability Stack

Observability stack for Solana RPC, AgentTxGuard, and autonomous transaction infrastructure.

## Purpose

This repo demonstrates production-style monitoring for autonomous Solana agent systems.

It exposes Prometheus metrics for Solana RPC health, Solana RPC slot, Solana RPC latency, AgentTxGuard health, AgentTxGuard latency, monitor check totals, and monitor error totals.

## Endpoints

- GET /
- GET /health
- GET /checks
- GET /metrics

## Run Locally

pip install -r requirements.txt
uvicorn metrics_server:app --reload --port 9000

Open:

- http://127.0.0.1:9000/checks
- http://127.0.0.1:9000/metrics

## Environment Variables

- SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
- AGENTTXGUARD_URL=http://127.0.0.1:8000
- AGENTTXGUARD_API_KEY=optional

## Run Tests

pytest

## Status

Experimental portfolio project. Not financial, legal, security, or investment advice.
