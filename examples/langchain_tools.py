"""EnergyAI free tools as LangChain StructuredTools — zero keys, one import.

pip install langchain-core requests

The tool list is fetched live from EnergyAI's OpenAI-format spec, so your agent
always has the current free toolset (incentives, solar estimates, node scores,
grounded incentive guides, and consented installer routing).

Usage with any LangChain agent:

    from langchain_tools import get_energyai_tools
    tools = get_energyai_tools()
    # pass `tools` to create_react_agent / create_tool_calling_agent / bind_tools
"""
from __future__ import annotations

import requests
from langchain_core.tools import StructuredTool

SPEC_URL = "https://api.energyaisolution.com/api/v1/agent/openai-tools.json"
EXEC_URL = "https://api.energyaisolution.com/api/v1/agent/{name}"
TIMEOUT_S = 30


def _make_executor(name: str):
    def _run(**kwargs) -> dict:
        r = requests.post(EXEC_URL.format(name=name), json={"args": kwargs}, timeout=TIMEOUT_S)
        body = r.json()
        if not body.get("ok"):
            # In-band errors (bad args, rate limit) come back structured — surface
            # them to the model so it can self-correct instead of crashing.
            return {"error": body.get("error", {"code": "unknown", "message": r.text[:500]})}
        return body["data"]
    return _run


def get_energyai_tools() -> list[StructuredTool]:
    """Fetch the live free-tier spec and wrap each tool for LangChain."""
    spec = requests.get(SPEC_URL, timeout=TIMEOUT_S).json()["tools"]
    tools: list[StructuredTool] = []
    for t in spec:
        fn = t["function"]
        tools.append(
            StructuredTool.from_function(
                func=_make_executor(fn["name"]),
                name=fn["name"],
                description=fn["description"],
                args_schema=None,           # raw JSON-schema path below
                infer_schema=False,
            )
        )
        tools[-1].args_schema = fn["parameters"]  # pass the JSON schema through as-is
    return tools


if __name__ == "__main__":
    ts = get_energyai_tools()
    print("EnergyAI tools:", [t.name for t in ts])
    guides = next(t for t in ts if t.name == "list_guides")
    print(guides.func(region="VT", topic="solar"))
