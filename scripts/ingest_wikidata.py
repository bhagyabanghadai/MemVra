#!/usr/bin/env python3
"""
Ingest country→capital facts from Wikidata into MemVra.

Requirements:
  - Python 3.8+
  - pip install requests

Environment:
  - MEMVRA_BASE_URL (default: http://localhost:8081)
  - MEMVRA_API_KEY (required)
  - MEMVRA_SECRET_KEY (optional, for local HMAC verification)

Usage:
  python scripts/ingest_wikidata.py --limit 20

On re-running with the same payloads, duplicates return HTTP 409 and do not create new records.
"""

import argparse
import os
import time
import hmac
import hashlib
import base64
import requests

WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

SPARQL_QUERY = """
SELECT ?country ?countryLabel ?capital ?capitalLabel WHERE {
  ?country wdt:P31 wd:Q6256 .            # instance of country
  ?country wdt:P36 ?capital .            # capital property
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY ?countryLabel
LIMIT %d
"""


def qid_from_uri(uri: str) -> str:
    # Example: https://www.wikidata.org/entity/Q142 -> Q142
    return uri.rsplit("/", 1)[-1]


def fetch_country_capitals(limit: int):
    headers = {
        "Accept": "application/sparql-results+json"
    }
    params = {
        "query": SPARQL_QUERY % limit
    }
    resp = requests.get(WIKIDATA_SPARQL_ENDPOINT, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    rows = []
    for b in data.get("results", {}).get("bindings", []):
        country_uri = b["country"]["value"]
        capital_uri = b["capital"]["value"]
        country = b["countryLabel"]["value"]
        capital = b["capitalLabel"]["value"]
        rows.append({
            "country_qid": qid_from_uri(country_uri),
            "capital_qid": qid_from_uri(capital_uri),
            "country": country,
            "capital": capital,
        })
    return rows


def sign_payload(payload: str, secret_key: str) -> str:
    mac = hmac.new(secret_key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256)
    return base64.b64encode(mac.digest()).decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description="Ingest Wikidata country→capital facts into MemVra")
    parser.add_argument("--limit", type=int, default=20, help="How many facts to ingest (default 20)")
    parser.add_argument("--sleep", type=float, default=0.6, help="Delay between posts to respect rate limit (seconds)")
    args = parser.parse_args()

    base_url = os.getenv("MEMVRA_BASE_URL", "http://localhost:8081")
    api_key = os.getenv("MEMVRA_API_KEY")
    secret_key = os.getenv("MEMVRA_SECRET_KEY")

    if not api_key:
        raise SystemExit("MEMVRA_API_KEY is required")

    facts = fetch_country_capitals(args.limit)
    created = 0
    conflicts = 0
    errors = 0
    verified = 0

    for f in facts:
        content = f"The capital of {f['country']} is {f['capital']}."
        source_type = "api_response"
        source_id = f"wikidata:{f['country_qid']}:capital:{f['capital_qid']}"
        recorded_by = "wikidata-ingestor"

        body = {
            "content": content,
            "source_type": source_type,
            "source_id": source_id,
            "recorded_by": recorded_by,
        }

        headers = {
            "Content-Type": "application/json",
            "X-API-Key": api_key,
        }

        try:
            resp = requests.post(f"{base_url}/v1/facts", json=body, headers=headers, timeout=30)
        except requests.RequestException as e:
            print(f"ERROR: POST failed for {source_id}: {e}")
            errors += 1
            time.sleep(args.sleep)
            continue

        if resp.status_code == 201:
            created += 1
            data = resp.json()
            # Optional local verification if secret is provided
            if secret_key:
                payload = "|".join([
                    data["fact_id"],
                    data["content"],
                    data["source_type"],
                    data["source_id"],
                    data["recorded_by"],
                    str(data["created_at"]),
                ])
                computed = sign_payload(payload, secret_key)
                if computed == data.get("signature"):
                    verified += 1
                else:
                    print(f"WARN: Signature mismatch for {data['fact_id']}")
        elif resp.status_code == 409:
            conflicts += 1
        else:
            errors += 1
            try:
                err = resp.json()
                print(f"ERROR: {resp.status_code} {err}")
            except Exception:
                print(f"ERROR: {resp.status_code} {resp.text}")

        time.sleep(args.sleep)

    print("\nIngestion Summary")
    print(f"Total attempted: {len(facts)}")
    print(f"Created:  {created}")
    print(f"Conflicts: {conflicts}")
    print(f"Errors:   {errors}")
    if secret_key:
        print(f"Verified: {verified}")


if __name__ == "__main__":
    main()