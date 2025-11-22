import os
import sys
import time
import uuid
from typing import Dict, Any

import requests


BASE_URL = os.getenv("MEMVRA_BASE_URL", "http://localhost:8081")
API_KEY = os.getenv("MEMVRA_API_KEY", "dev-key")

def unique_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def pretty(name: str, ok: bool, info: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name} {('- ' + info) if info else ''}")


def post_fact(payload: Dict[str, Any], headers: Dict[str, str] | None) -> requests.Response:
    merged = {"Content-Type": "application/json"}
    if headers:
        merged.update(headers)
    return requests.post(f"{BASE_URL}/v1/facts", json=payload, headers=merged)


def run_auth_scenarios() -> None:
    name = "Unauthorized POST returns 401"
    payload = {
        "content": "Paris is the capital of France",
        "source_type": "api_response",
        "source_id": unique_id("Q142"),
        "recorded_by": "unauth-scenario"
    }
    r = post_fact(payload, headers={})
    ok = r.status_code == 401
    info = f"status={r.status_code} body={r.text[:200]}"
    pretty(name, ok, info)

    # Excluded paths accessible without API key (Swagger, health)
    name = "Swagger docs accessible without API key"
    r = requests.get(f"{BASE_URL}/v3/api-docs")
    pretty(name, r.status_code == 200, f"status={r.status_code}")

    name = "Actuator health accessible without API key"
    r = requests.get(f"{BASE_URL}/actuator/health")
    pretty(name, r.status_code in (200, 503), f"status={r.status_code}")


def run_happy_path_and_dedup() -> str:
    headers = {"X-API-Key": API_KEY}
    payload = {
        "content": "Berlin is the capital of Germany",
        "source_type": "api_response",
        "source_id": unique_id("Q183"),
        "recorded_by": "scenario-test-unit"
    }

    r1 = post_fact(payload, headers=headers)
    ok1 = r1.status_code == 201
    pretty("Create fact returns 201", ok1, f"status={r1.status_code}")
    fact_id = ""
    try:
        fact_id = r1.json().get("fact_id", "")
    except Exception:
        pass

    r2 = post_fact(payload, headers=headers)
    ok2 = r2.status_code == 409
    pretty("Duplicate fact returns 409", ok2, f"status={r2.status_code}")

    return fact_id


def run_validation_and_errors(fact_id_created: str) -> None:
    headers = {"X-API-Key": API_KEY}

    # Malformed JSON -> 400
    name = "Malformed JSON returns 400"
    bad_headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    r = requests.post(f"{BASE_URL}/v1/facts", data="{", headers=bad_headers)
    pretty(name, r.status_code == 400, f"status={r.status_code} body={r.text[:200]}")

    # Validation error -> 422 (bad source_id)
    name = "Validation error returns 422 (invalid source_id)"
    payload = {
        "content": "Madrid is the capital of Spain",
        "source_type": "api_response",
        "source_id": "INVALID ID WITH SPACES",
        "recorded_by": "scenario-test"
    }
    r = post_fact(payload, headers=headers)
    pretty(name, r.status_code == 422, f"status={r.status_code}")

    # GET invalid id format -> 400
    name = "GET invalid id format returns 400"
    r = requests.get(f"{BASE_URL}/v1/facts/not-a-valid-id", headers=headers)
    pretty(name, r.status_code == 400, f"status={r.status_code}")

    # GET not found -> 404
    name = "GET non-existent id returns 404"
    random_id = f"mv-{uuid.uuid4()}"
    r = requests.get(f"{BASE_URL}/v1/facts/{random_id}", headers=headers)
    pretty(name, r.status_code == 404, f"status={r.status_code}")

    # GET created id -> 200
    if fact_id_created:
        name = "GET created id returns 200"
        r = requests.get(f"{BASE_URL}/v1/facts/{fact_id_created}", headers=headers)
        pretty(name, r.status_code == 200, f"status={r.status_code}")
    else:
        pretty("GET created id returns 200", False, "missing fact_id from creation response")


def run_rate_limit_test() -> None:
    headers = {"X-API-Key": API_KEY}
    name = "Rate limit returns 429 when exceeding per-minute quota"

    # Fire 8 requests quickly to trigger 429 when rate limit is set low (e.g., 5)
    statuses = []
    for i in range(8):
        payload = {
            "content": f"Test RL message {i}",
            "source_type": "api_response",
            "source_id": unique_id(f"RLQ{i}"),
            "recorded_by": "rl-scenario"
        }
        r = post_fact(payload, headers=headers)
        statuses.append(r.status_code)
        time.sleep(0.15)

    ok = 429 in statuses
    pretty(name, ok, f"statuses={statuses}")


def main() -> int:
    print(f"Running scenarios against {BASE_URL}")
    run_auth_scenarios()
    fid = run_happy_path_and_dedup()
    run_validation_and_errors(fid)
    run_rate_limit_test()
    return 0


if __name__ == "__main__":
    sys.exit(main())