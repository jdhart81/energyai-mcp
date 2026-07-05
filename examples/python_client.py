"""Minimal EnergyAI client — free tools, no API key.

Works standalone, or as the executor behind OpenAI function-calling /
LangChain / CrewAI tools (spec: https://api.energyaisolution.com/api/v1/agent/openai-tools.json).
"""
import requests

BASE = "https://api.energyaisolution.com/api/v1/agent"

def call_energyai(tool: str, args: dict, api_key: str | None = None) -> dict:
    """POST a tool call. Returns {ok, data} or {ok: False, error}.
    api_key is optional — attach yours on route_lead to earn the 20% bounty."""
    headers = {"content-type": "application/json"}
    if api_key:
        headers["authorization"] = f"Bearer {api_key}"
    r = requests.post(f"{BASE}/{tool}", json={"args": args}, headers=headers, timeout=30)
    return r.json()

if __name__ == "__main__":
    print(call_energyai("check_incentives", {"zipCode": "59715"}))
    print(call_energyai("estimate_production", {"zipCode": "85004", "systemKw": 8}))
    print(call_energyai("get_node_score", {"zipCode": "05401", "heatingFuel": "oil", "monthlyBillUsd": 220}))
