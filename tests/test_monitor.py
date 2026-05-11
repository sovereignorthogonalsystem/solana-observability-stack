import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from monitor import CheckResult


def test_check_result_shape():
    result = CheckResult(name="demo", ok=True, latency_seconds=0.1, details={"hello": "world"})
    assert result.name == "demo"
    assert result.ok is True
    assert result.details["hello"] == "world"


def test_metrics_server_imports():
    import metrics_server
    config = metrics_server.get_config()
    assert "solana_rpc_url" in config
    assert "agenttxguard_url" in config
