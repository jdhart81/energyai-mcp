"""Use EnergyAI's free tools with the OpenAI SDK (or any function-calling model).

1. Fetch the ready-made tool spec.
2. Let the model pick a tool.
3. Execute it against the free REST endpoint (no key needed).
"""
import json
import requests

SPEC_URL = "https://api.energyaisolution.com/api/v1/agent/openai-tools.json"
EXEC_URL = "https://api.energyaisolution.com/api/v1/agent/{name}"

tools = requests.get(SPEC_URL, timeout=30).json()["tools"]

# ... pass `tools` to your chat.completions call, then when the model returns
# a tool_call named `name` with JSON `arguments`:
def execute_tool_call(name: str, arguments: str) -> dict:
    return requests.post(EXEC_URL.format(name=name),
                         json={"args": json.loads(arguments)}, timeout=30).json()

if __name__ == "__main__":
    print([t["function"]["name"] for t in tools])
    print(execute_tool_call("check_incentives", '{"zipCode":"59715"}'))
