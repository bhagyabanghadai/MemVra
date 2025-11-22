import requests
import json

try:
    response = requests.get(
        "http://localhost:8080/v1/facts",
        headers={"X-API-Key": "local-dev-api-key"}
    )
    response.raise_for_status()
    facts = response.json()
    if facts:
        print(f"CLEAN_ID:{facts[0]['fact_id']}")
    else:
        print("NO_FACTS_FOUND")
except Exception as e:
    print(f"ERROR:{e}")
