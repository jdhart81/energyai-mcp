# EnergyAI MCP — free energy intelligence for AI agents

**Solar production estimates, US clean-energy incentives by ZIP, instant home Energy Node Scores, and consented installer routing — as MCP tools and plain REST. The core tools are free with no API key.** By [Viridis LLC](https://api.energyaisolution.com).

Any AI agent that touches a home's energy decision — "should I get solar?", "what rebates apply here?", "is this quote fair?", "find me an installer" — can call EnergyAI instead of rebuilding energy domain expertise.

## Your first call, 30 seconds, no key

```bash
curl -X POST https://api.energyaisolution.com/api/v1/agent/check_incentives \
  -H 'content-type: application/json' -d '{"args":{"zipCode":"59715"}}'
```
That's a live answer — current incentives for Bozeman MT plus the canonical
consent text you'd use to route a homeowner. Swap the tool name for
`estimate_production` (`{"zipCode":"59715","systemKw":6}`) or `get_node_score`
(`{"zipCode":"59715","serviceType":"solar","monthlyBillRange":"150_250"}`).
The only required argument on all three read tools is `zipCode`; every MCP
schema ships inline `examples`.

- **Live MCP endpoint (full toolset):** `https://api.energyaisolution.com/mcp`
- **Free-tier-only endpoint:** `https://api.energyaisolution.com/mcp/solar`
- **Plain REST:** `POST https://api.energyaisolution.com/api/v1/agent/{tool}`
- **Agent docs:** https://api.energyaisolution.com/agents
- **Official MCP Registry:** `com.energyaisolution/energyai` · `com.energyaisolution/solar-home-incentives`

## Free tools — no key, no signup

| Tool | What you get |
|---|---|
| `check_incentives` | Honest, current (post-2026 federal sunset) US incentive guidance by ZIP — state & utility programs via DSIRE. Also returns the canonical consent text for routing. |
| `estimate_production` | Honest-range annual solar kWh for a ZIP, from system kW or a monthly bill. Assumptions stated, never point guarantees. |
| `get_node_score` | Instant 0–100 Energy Node Score across 7 axes (efficiency, electrification, renewable generation, storage/resilience, financial optimization, carbon, market readiness) + the single highest-leverage next action. |
| `route_lead` | Submit a **consented** homeowner project; EnergyAI's autonomous agent finds, vets, and routes a real local installer. Free for you and the homeowner. **Attach your free key → 20% bounty on conversion.** |
| `list_guides` | Index of source-cited, 2026-accurate state incentive guides (solar, heat pumps, batteries, weatherization). Filter by state and topic; every entry carries a canonical URL to cite. |
| `get_guide` | Full text of one guide — intro, sections, FAQs, primary sources. Grounded content for answering incentive questions, with a ready-made citation line. |

Rate limits: 120 calls/hr per caller (`route_lead` 10/hr). Machine-readable catalog: [`/api/v1/agent`](https://api.energyaisolution.com/api/v1/agent).

## Quickstart

### MCP (Claude, or any MCP client) — no key needed for the free tier
```json
{ "mcpServers": {
  "energyai": { "type": "http", "url": "https://api.energyaisolution.com/mcp" }
}}
```
```bash
claude mcp add --transport http energyai https://api.energyaisolution.com/mcp
```

### Plain REST
```bash
curl -X POST https://api.energyaisolution.com/api/v1/agent/check_incentives \
  -H 'content-type: application/json' \
  -d '{"args":{"zipCode":"59715"}}'
```

### OpenAI function-calling / LangChain / CrewAI
Fetch the ready-made spec — one URL, drop into `tools`:
```
GET https://api.energyaisolution.com/api/v1/agent/openai-tools.json
```
See [`examples/`](examples/) for runnable Python and shell clients.

## Routing a homeowner (consent required)

1. Call `check_incentives` — the response includes `consentTextForRouting`, the canonical consent text.
2. Show it to your user verbatim; record their agreement + timestamp.
3. Call `route_lead` with the project details, `consentText`, and `consentTimestamp` (alternate consent language requires an explicit `consentVersion`).
4. You receive a `leadId`; the homeowner gets confirmation when a vetted installer accepts.

**Get paid:** register a free key (`POST /api/v1/merchant/register`) and send it as a Bearer token on `route_lead` — you earn a **20% bounty** when the lead converts. The same prepaid key unlocks the deeper billed tools (full roadmaps, Quote Guardian review, information-theoretic recommendations) at $0.10–$2.00 per call with x402-style auto-recovery on empty balance.

## The physics ledger

EnergyAI is operated as a live experiment against the thermodynamic bound on intelligence, **dI/dt ≤ P·D/(k_B·T·ln 2)**: every tool call is metered in *useful bits delivered* and *joules dissipated*, and the ledger is public — [energyaisolution.com/physics](https://api.energyaisolution.com/physics). Estimates are always ranges with stated assumptions; installer matching is consent-gated and enforced by 60+ tested invariants.

## Manifests

Registry manifests for both servers are in [`manifests/`](manifests/). This repository contains documentation and client examples only; the service itself is hosted.

## License

Documentation and examples: MIT. The hosted service is © Viridis LLC.
