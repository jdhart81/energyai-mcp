# EnergyAI MCP — energy planning tools for AI agents

**Solar estimates, incentive sources, provisional Energy Node Scores, cited guides, contractor discovery and consented installer routing — through MCP and REST.** By [Viridis LLC](https://energyaisolution.com).

The public catalog supports solar, weatherization, EV charging, home batteries and heat-pump planning. Twelve tools need no key to start. Estimates and scores use supplied facts and stated assumptions; they do not establish site suitability, incentive eligibility, installation approval or verified savings.

## Your first call — no key

```bash
curl -X POST https://api.energyaisolution.com/api/v1/agent/check_incentives \
  -H 'content-type: application/json' -d '{"args":{"zipCode":"59715"}}'
```

This requests incentive source guidance for a US ZIP. For a production estimate, use `estimate_production` with `{"zipCode":"59715","systemKw":6}`. For a provisional score, use `get_node_score` with `{"zipCode":"59715","serviceType":"solar","monthlyBillRange":"150_250"}`. These informational tools accept omitted inputs with documented assumptions or broader guidance; inspect the live schema for the job you need.

- **Full MCP endpoint:** `https://api.energyaisolution.com/mcp`
- **Discovery MCP endpoint:** `https://api.energyaisolution.com/mcp/solar`
- **REST:** `POST https://api.energyaisolution.com/api/v1/agent/{tool}`
- **[Agent guide](https://energyaisolution.com/agents)** · **[Live catalog](https://api.energyaisolution.com/api/v1/agent)** · **[Live prices](https://api.energyaisolution.com/api/v1/mcp/pricing)**
- **Official MCP Registry:** [`com.energyaisolution/energyai`](https://registry.modelcontextprotocol.io/v0.1/servers/com.energyaisolution%2Fenergyai/versions/latest) · [`com.energyaisolution/solar-home-incentives`](https://registry.modelcontextprotocol.io/v0.1/servers/com.energyaisolution%2Fsolar-home-incentives/versions/latest)

## No-key tools and allowances

The five informational tools share **20 anonymous calls per caller per 24 hours**. A free key includes **100 informational calls per rolling 30 days**. Sustained informational use requires an active Builder subscription; prepaid credit funds priced commercial tools.

| Informational tool | What you get |
|---|---|
| `check_incentives` | Source-linked incentive guidance by country and postal code; eligibility remains unverified. |
| `estimate_production` | A modeled annual solar production range with assumptions. |
| `get_node_score` | A provisional seven-axis score and next action from supplied property facts. |
| `list_guides` | US home-energy guides by state and topic, with sources and canonical links. |
| `get_guide` | One source-cited guide by returned slug. |

These seven tools remain free without a key:

| Tool | What you get |
|---|---|
| `get_quote_link` | Optional household assessment and human-review handoffs; no project submission or payment. |
| `get_power_passport_link` | A website handoff for a candidate site and workload; scope review precedes payment. |
| `get_power_service_quote` | A signed, time-limited quote for a Power Screen; creating the quote does not spend funds. |
| `route_lead` | A consented homeowner project submitted to the guarded installer-matching workflow. Unmatched projects may remain recorded. |
| `create_builder_key` | A production key after the human operator has authorized the Terms and Privacy Policy. |
| `get_builder_upgrade_link` | A human activation, Builder or prepaid handoff; the caller cannot accept terms or pay for the human. |
| `find_local_installers` | Public-reputation contractor options. Public listings do not imply EnergyAI vetting, endorsement or partnership. |

Hourly safety limits also apply: 120 calls per caller, with `route_lead` limited to 10 per hour. Read each tool's schema and consent requirements before submitting information or requesting a key.

## Connect an MCP client

```json
{ "mcpServers": {
  "energyai": { "type": "http", "url": "https://api.energyaisolution.com/mcp" }
}}
```

```bash
claude mcp add --transport http energyai https://api.energyaisolution.com/mcp
```

For OpenAI function calling or other tool clients, fetch the [function specification](https://api.energyaisolution.com/api/v1/agent/openai-tools.json). See [`examples/`](examples/) for Python and shell clients.

## Review an installer quote

After authorized key activation, call `review_installer_quote` on the full MCP endpoint with `postalCode` and redacted `quoteText` (at most 6,000 characters), or an `assessmentId` belonging to the Builder account. Use `serviceType` for solar, battery, EV charging, efficiency or heat pumps. No prior assessment setup is required.

The public price is **$0.10 per call**, covered by a new key's three eligible commercial trials. The result provides source-matched terms, practical installer questions and explicit unknowns. It is automated decision support; human review, price fairness, incentive eligibility and useful household delivery are not established by a successful tool response.

`bootstrap_energy_project` also costs **$0.10** and creates persisted project context, a provisional score, an input-coverage map and a reusable `assessmentId` when a quote is not yet available. Use free `check_incentives` for general guidance; the paid `get_energy_incentives` requires a completed assessment.

New keys include **three trial calls for eligible tools priced at $0.25 or less**, after operator-authorized Terms acceptance. Builder is **$19/month with $20 in monthly tool credit**; prepaid top-ups remain available with a $5 minimum. Consult [live pricing and plan details](https://energyaisolution.com/agents) before a billed call, and use an operator-approved spending ceiling. Key creation, terms acceptance and subscription activation are separate steps.

If the operator has not authorized the Terms and Privacy Policy, present the human activation link from `get_builder_upgrade_link`. Store a returned key securely; never print it in a user-visible reply. `record_quote_review_outcome` is a free, keyed tool for recording actual operator-confirmed usefulness and household delivery status; never infer that feedback from technical success.

## Routing a homeowner — explicit consent required

1. Retrieve the current `consentTextForRouting` from `check_incentives`.
2. Show that text verbatim to the homeowner and record their agreement and timestamp.
3. Call `route_lead` with the required project and contact details, `consentText` and `consentTimestamp`. Alternate consent language requires an explicit `consentVersion`.
4. Report the returned `leadId` and actual routing status. Prefer `get_quote_link` when consent is not already available.

The current public quote handoff describes an authenticated referral incentive as **20% non-cash EnergyAI tool credit after verified purchase**. Disclose that interest, preserve the customer price and independent review, and consult the current terms. This is not a cash bounty or evidence that a purchase occurred.

## Public research context

The [physics ledger](https://api.energyaisolution.com/physics) presents platform-reported research context and metrics. Model-based estimates, software checks and reported metrics do not by themselves establish measured physical energy, empirical performance or a certified thermodynamic bound.

## Manifests

Both manifests in [`manifests/`](manifests/) match the official registry's active latest **v1.3.0** entries observed on **October 7, 2026**. The live catalog also reports v1.3.0. Registry presence and endpoint responses are availability evidence; they do not establish adoption, paid delivery, repeat use or revenue.

This repository contains documentation and client examples. The service is hosted separately; merging these files does not publish a registry version, deploy the service or activate a customer account.

## License

Documentation and examples: MIT. The hosted service is © Viridis LLC.
