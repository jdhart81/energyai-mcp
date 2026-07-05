#!/usr/bin/env bash
# EnergyAI free agent tools — plain REST, no API key.
BASE=https://api.energyaisolution.com/api/v1/agent

# Current incentives for a ZIP (also returns the canonical consent text for routing)
curl -s -X POST $BASE/check_incentives -H 'content-type: application/json' \
  -d '{"args":{"zipCode":"59715"}}'

# Honest-range solar production for an 8 kW system in Phoenix
curl -s -X POST $BASE/estimate_production -H 'content-type: application/json' \
  -d '{"args":{"zipCode":"85004","systemKw":8}}'

# Instant Energy Node Score from partial facts
curl -s -X POST $BASE/get_node_score -H 'content-type: application/json' \
  -d '{"args":{"zipCode":"05401","propertyType":"single_family","heatingFuel":"oil","monthlyBillUsd":220}}'
