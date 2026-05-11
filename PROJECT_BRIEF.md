# Solana Observability Stack: Monitoring for Autonomous Transaction Infrastructure

## Summary

Solana Observability Stack is a production-style monitoring project for Solana RPC, AgentTxGuard, and autonomous transaction infrastructure.

It exposes health checks, Prometheus metrics, alert rules, Grafana dashboards, Docker Compose configuration, runbooks, and a postmortem template.

## Problem

Autonomous crypto agents depend on external infrastructure such as Solana RPC providers, quote APIs, transaction simulation, and preflight verification services.

If RPC latency spikes, AgentTxGuard goes down, simulations fail, or slot data becomes stale, agents should not continue execution blindly.

## Solution

This project provides an observability layer around that infrastructure.

It monitors Solana RPC and AgentTxGuard, exposes Prometheus-compatible metrics, and includes operational assets for incident response.

## Monitored Targets

### Solana RPC

- health status
- current slot
- request latency
- error count

### AgentTxGuard

- health endpoint status
- health latency
- availability signal

## Metrics

- solana_rpc_up
- solana_rpc_slot
- solana_rpc_latency_seconds
- agenttxguard_up
- agenttxguard_health_latency_seconds
- monitor_check_total
- monitor_check_errors_total

## Operational Assets

- Prometheus scrape config
- Prometheus alert rules
- Grafana dashboard provisioning
- Dockerfile
- Docker Compose
- incident runbooks
- postmortem template
- tests

## Why It Matters

Autonomous agents need operational visibility, not only execution logic.

This stack helps detect infrastructure failures before agents continue acting on stale, slow, or unavailable systems.

## Resume Signal

This repo demonstrates:

- platform engineering
- SRE thinking
- observability design
- Prometheus/Grafana workflow
- Dockerized service design
- Solana infrastructure awareness
- autonomous-agent operational safety
- incident-response documentation habits

## Status

Experimental portfolio project. Not financial, legal, security, or investment advice.
