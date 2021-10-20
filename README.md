# Overview

This repo provides example JSON body sections to enable and disable the CIS Benchmarks for Azure in Lacework when calling the PATCH method on *https://lacework-tenant.lacework.net/api/v1/external/recommendations/azure* API Endpoint via the Lacework CLI

# Script - azure-cis-config.py
This script can be used to bulk enable/disable compliance checkers on your target environment.

### Pre-requisites
- Lacework CLI installed
- Lacework CLI configured, targeting the desired Lacework tenant
- Python 3 installed

### Usage

`azure-cis-config.sh [disable_cis_10|enable_cis_10|disable_cis_131|enable_cis_131|enable_all|disable_all] [lacework-tenant]`

Where the first argument is the action you wish to perform, and the second argument is your lacework tenant (without the `.lacework.net`)

If the Lacework CLI is not configured to the same lacework-tenant provided in the ARGs the command will fail.

This script also generates an updated version of the checker maps based on the recommendations(checkers) deployed to the target environment.
