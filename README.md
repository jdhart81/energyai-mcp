# EnergyAI MCP — energy planning tools for AI agents

**Solar, heat pump and battery decisions for agents: incentives, estimates, quote review, installers.** By [Viridis LLC](https://energyaisolution.com).

EnergyAI helps an agent answer a homeowner's energy questions and act on them. Check solar, heat pump, battery and weatherization incentives by state and ZIP, estimate solar production, read 98 plain-language guides, find local installers, and send a homeowner to an independent human review of their installer quote. 34 tools in all: 16 work with no key, 7 more are free with a free key. 11 paid tools, from $0.02 to $1.00 per call, add a full power screen, project roadmaps and installer quote review. Remote server over Streamable HTTP: claude mcp add --transport http energyai https://api.energyaisolution.com/mcp

The public catalog supports solar, weatherization, EV charging, home batteries and heat-pump planning. 17 tools need no key to start. Estimates and scores use supplied facts and stated assumptions; they do not establish site suitability, incentive eligibility, installation approval or verified savings.

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
- **For agents:** [`llms.txt`](llms.txt) is the short index; [`AGENTS.md`](AGENTS.md) holds the consent, key and pricing rules agents must follow.
- **Official MCP Registry:** [`com.energyaisolution/energyai`](https://registry.modelcontextprotocol.io/v0.1/servers/com.energyaisolution%2Fenergyai/versions/latest) · [`com.energyaisolution/solar-home-incentives`](https://registry.modelcontextprotocol.io/v0.1/servers/com.energyaisolution%2Fsolar-home-incentives/versions/latest)

## Tools, allowances and prices

<!-- tool-count:start (must equal the live server; scripts/check-listing.mjs enforces it) -->
**35 tools:** 17 work with no key (6 informational tools share the anonymous allowance; 11 are always free), 7 more are free with a free key, and 11 are paid.

17 tools free with no key (20 calls a day for the 6 informational ones), or a free key for 100 calls a month and 7 more free tools. 11 paid tools cost $0.02 to $1.00 per call from a prepaid balance starting at $5.
<!-- tool-count:end -->

### No key: informational tools

The five informational tools share **20 anonymous calls per caller per 24 hours**. A free key includes **100 informational calls per rolling 30 days**. Sustained informational use requires an active Builder subscription; prepaid credit funds priced commercial tools.

| Informational tool | What you get |
|---|---|
| `check_incentives` | Source-linked incentive guidance by country and postal code; eligibility remains unverified. |
| `estimate_production` | A modeled annual solar production range with assumptions. |
| `get_node_score` | A provisional seven-axis score and next action from supplied property facts. |
| `list_guides` | US home-energy guides by state and topic, with sources and canonical links. |
| `get_guide` | One source-cited guide by returned slug. |
| `check_quote_red_flags` | Free automated check of an installer quote's key numbers: up to 5 red flags with questions for the installer, a summary for the homeowner, and the $49 Quote Guardian human review as the next step. Never a sign-off. |

### No key: 11 always-free tools

| Tool | What you get |
|---|---|
| `get_quote_link` | Optional household assessment and human-review handoffs; no project submission or payment. |
| `get_power_passport_link` | A website handoff for a candidate site and workload; scope review precedes payment. |
| `get_power_service_quote` | A signed, time-limited quote for a Power Screen; creating the quote does not spend funds. |
| `route_lead` | A consented homeowner project submitted to the guarded installer-matching workflow. Unmatched projects may remain recorded. |
| `create_builder_key` | A production key after the human operator has authorized the Terms and Privacy Policy. |
| `get_builder_upgrade_link` | A human activation, Builder or prepaid handoff; the caller cannot accept terms or pay for the human. |
| `find_local_installers` | Public-reputation contractor options. Public listings do not imply EnergyAI vetting, endorsement or partnership. |
| `energy_calendar` | Energy Odds (paper mode): upcoming target dates for three public EIA numbers and whether a forecast is logged. |
| `energy_forecast` | Energy Odds: the forecast logged in advance for a series and target date, with quantiles and a verifiable hash. |
| `energy_track_record` | Energy Odds public scores (Brier, CRPS, calibration) against two simple baselines. |
| `verify_forecast` | Recomputes the hash chain for one forecast and reports whether it was logged before its cutoff. |

### Free with a free key (7)

| Tool | What you get |
|---|---|
| `create_energy_assessment` | Starts a guided assessment and returns an `assessmentId`. |
| `answer_energy_assessment_question` | Records one answer and returns the next question. |
| `complete_energy_assessment` | Finalizes an assessment and starts the recommendation workflow. |
| `create_energy_node_roadmap_checkout` | A homeowner-facing checkout link for the full roadmap. |
| `get_eta_i_metric` | The platform intelligence-efficiency metric. |
| `record_quote_review_outcome` | Records operator-confirmed usefulness of a completed quote review. |
| `submit_contractor_match_request` | A consented installer lead for a completed assessment. |

### Paid (11), per call from prepaid balance

| Tool | Price |
|---|---|
| `get_energy_incentives` | $0.02 |
| `generate_energy_recommendation_preview` | $0.05 |
| `get_energy_node_score` | $0.05 |
| `match_installers` | $0.05 |
| `bootstrap_energy_project` | $0.10 |
| `get_energy_node_roadmap` | $0.10 |
| `review_installer_quote` | $0.10 |
| `generate_intelligence_bound_report` | $0.25 |
| `get_information_theoretic_recommendation` | $0.25 |
| `run_power_screen` | $1.00 |
| `get_anonymized_dataset_sample` | $1.00 |

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

Both manifests in [`manifests/`](manifests/) describe **v1.4.0**, live since 2026-11-25. The official registry still lists v1.3.0 until v1.4.0 is published there; merge this change together with that publication. Registry presence and endpoint responses are availability evidence; they do not establish adoption, paid delivery, repeat use or revenue.

This repository contains documentation and client examples. The service is hosted separately; merging these files does not publish a registry version, deploy the service or activate a customer account.

## License

Documentation and examples: MIT. The hosted service is © Viridis LLC.
