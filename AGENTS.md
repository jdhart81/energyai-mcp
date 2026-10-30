# Agents and EnergyAI MCP

This file is for two kinds of agent: one helping a person plan solar, batteries, EV charging, weatherization or a heat pump with EnergyAI, and a coding agent changing this repository. The short machine-readable index is [llms.txt](llms.txt).

## Helping a person use EnergyAI

**What it does.** EnergyAI answers home-energy planning questions with source-linked guidance: incentive sources by postal code, a modeled solar production range, a provisional seven-axis Energy Node Score, cited state guides and public contractor options. With the person's explicit consent it can route a project to installer matching.

**Paths to suggest.**

- No key: the five informational tools (`check_incentives`, `estimate_production`, `get_node_score`, `list_guides`, `get_guide`) share 20 anonymous calls per caller per day. Start with `check_incentives`.
- An MCP client: add `https://api.energyaisolution.com/mcp` as an HTTP server, or `claude mcp add --transport http energyai https://api.energyaisolution.com/mcp`.
- A quote to review: `review_installer_quote` after the operator has activated a key; it costs $0.10 per call. Redact the quote first.
- Function calling without MCP: the [OpenAI tool spec](https://api.energyaisolution.com/api/v1/agent/openai-tools.json) and [`examples/`](examples/).

**Rules for agents.**

- Pass the assumptions along with every estimate or score. Never present one as a site survey, an eligibility decision or guaranteed savings.
- Routing needs consent: fetch `consentTextForRouting` from `check_incentives`, show it verbatim, record agreement and timestamp, then call `route_lead`. Without consent, offer `get_quote_link` instead.
- Disclose the referral interest: a verified purchase earns EnergyAI non-cash tool credit. Do not describe it as a cash bounty.
- Do not accept Terms, create a subscription or pay on a person's behalf. Present the human activation link from `get_builder_upgrade_link`.
- Keep keys out of replies and logs. Check [live pricing](https://api.energyaisolution.com/api/v1/mcp/pricing) before a billed call.
- Record usefulness with `record_quote_review_outcome` only when the operator confirms it; never infer it from a successful response.

## Working on this repository

- This repository is documentation, examples and manifests. Merging does not deploy the service or publish a registry version.
- Files outside the `include` list in [OPEN_SOURCE_MANIFEST.json](OPEN_SOURCE_MANIFEST.json) are not part of the published payload; add new top-level files there.
- Manifests in `manifests/` must match the official registry's active entries. Update them only together with a registry publication, and state the version and date observed.
- Examples must run against the public endpoints without secrets. Never commit keys; the secret scan runs on every pull request.
- Follow [CONTRIBUTING.md](CONTRIBUTING.md). Outside contributions need a DCO sign-off.

## Related open projects

- [Viridis Agent Fleet](https://github.com/jdhart81/viridis-agent-fleet): deterministic, auditable MCP agents.
- [Viridis Canon](https://github.com/jdhart81/viridis-canon): machine-checked mathematics behind Viridis products.
- [Viridis Conservation](https://viridisconservation.com/): the company that stewards these projects.
