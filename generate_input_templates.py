"""
generate_input_templates.py

Purpose:
- Generate empty/synthetic CSV templates for Basel 3.1 / PRA RWA calculation
- Covers Exposures (with EAD formulas + random errors), Counterparties,
  Agreements, Collateral, Guarantees, RiskWeights, RegulatoryParameters,
  LossParameters, RWAResults
"""

import os
import pandas as pd
import random

# -------------------------------
# Config
# -------------------------------
OUTPUT_DIR = "RWA-Input-Templates"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------
# Exposures (On/Off Balance Products with EAD + Random Errors)
# -------------------------------
exposures_schema = [
    "trade_id","product_type","balance_sheet_flag","notional","currency",
    "maturity_years","CCF","EAD_formula","EAD_value"
]

product_mapping = [
    {"product_type":"Loan","balance_sheet_flag":"On","CCF":1.0,"formula":"EAD = Notional × 100%"},
    {"product_type":"Bond","balance_sheet_flag":"On","CCF":1.0,"formula":"EAD = Notional × 100%"},
    {"product_type":"Equity Investment","balance_sheet_flag":"On","CCF":1.0,"formula":"EAD = Notional × 100%"},
    {"product_type":"Other Funded Exposure","balance_sheet_flag":"On","CCF":1.0,"formula":"EAD = Notional × 100%"},
    {"product_type":"Commitment (cancellable)","balance_sheet_flag":"Off","CCF":0.1,"formula":"EAD = Notional × 10%"},
    {"product_type":"Commitment (other)","balance_sheet_flag":"Off","CCF":0.5,"formula":"EAD = Notional × 50%"},
    {"product_type":"Guarantee","balance_sheet_flag":"Off","CCF":1.0,"formula":"EAD = Notional × 100%"},
    {"product_type":"Letter of Credit","balance_sheet_flag":"Off","CCF":0.2,"formula":"EAD = Notional × 20%"},
    {"product_type":"Standby LC","balance_sheet_flag":"Off","CCF":0.5,"formula":"EAD = Notional × 50%"},
    {"product_type":"Other OBS Exposure","balance_sheet_flag":"Off","CCF":0.25,"formula":"EAD = Notional × CCF"}
]

exposures_rows = []
for i, p in enumerate(product_mapping, start=1):
    trade_id = f"T{str(i).zfill(4)}"
    notional = random.randint(100000, 5000000)
    currency = random.choice(["USD","EUR","GBP","INR","JPY"])
    maturity_years = round(random.uniform(0.5,5.0),2)
    ead_value = round(notional * p["CCF"],2)

    # Inject random errors in ~20% of rows
    if random.random() < 0.2:
        error_type = random.choice(["missing_field","negative_notional","bad_currency","wrong_ccf"])
        if error_type == "missing_field":
            currency = ""  # blank currency
        elif error_type == "negative_notional":
            notional = -notional  # invalid negative
        elif error_type == "bad_currency":
            currency = "XXX"  # invalid currency code
        elif error_type == "wrong_ccf":
            p["CCF"] = 999  # nonsensical CCF

    exposures_rows.append({
        "trade_id": trade_id,
        "product_type": p["product_type"],
        "balance_sheet_flag": p["balance_sheet_flag"],
        "notional": notional,
        "currency": currency,
        "maturity_years": maturity_years,
        "CCF": p["CCF"],
        "EAD_formula": p["formula"],
        "EAD_value": ead_value
    })

exposures_df = pd.DataFrame(exposures_rows, columns=exposures_schema)
exposures_df.to_csv(os.path.join(OUTPUT_DIR,"Exposures.csv"), index=False)
print("✅ Exposures.csv with EAD formulas and random errors generated")

# -------------------------------
# Counterparties
# -------------------------------
counterparties_schema = [
    "counterparty_id","counterparty_name","LEI","counterparty_type",
    "external_rating","internal_rating","domicile_country","industry_sector"
]
pd.DataFrame(columns=counterparties_schema).to_csv(os.path.join(OUTPUT_DIR,"Counterparties.csv"), index=False)

# -------------------------------
# Agreements
# -------------------------------
agreements_schema = [
    "agreement_id","netting_set_id","counterparty_id","threshold",
    "minimum_transfer_amount","independent_amount","margin_frequency",
    "eligible_collateral_types","haircut_schedule"
]
pd.DataFrame(columns=agreements_schema).to_csv(os.path.join(OUTPUT_DIR,"Agreements.csv"), index=False)

# -------------------------------
# Collateral
# -------------------------------
collateral_schema = [
    "collateral_id","trade_id","agreement_id","collateral_type",
    "collateral_market_value","collateral_currency","collateral_haircut",
    "collateral_eligibility_flag"
]
pd.DataFrame(columns=collateral_schema).to_csv(os.path.join(OUTPUT_DIR,"Collateral.csv"), index=False)

# -------------------------------
# Guarantees
# -------------------------------
guarantees_schema = [
    "guarantee_id","linked_exposure_id","guarantor_id","guarantor_type",
    "guarantor_rating","guarantee_coverage_amount","guarantee_currency",
    "guarantee_maturity_years","guarantee_eligibility_flag"
]
pd.DataFrame(columns=guarantees_schema).to_csv(os.path.join(OUTPUT_DIR,"Guarantees.csv"), index=False)

# -------------------------------
# RiskWeights
# -------------------------------
riskweights_schema = ["counterparty_type","rating","maturity_bucket","risk_weight"]
pd.DataFrame(columns=riskweights_schema).to_csv(os.path.join(OUTPUT_DIR,"RiskWeights.csv"), index=False)

# -------------------------------
# RegulatoryParameters
# -------------------------------
regparams_schema = ["parameter_name","parameter_value","description","source"]
pd.DataFrame(columns=regparams_schema).to_csv(os.path.join(OUTPUT_DIR,"RegulatoryParameters.csv"), index=False)

# -------------------------------
# LossParameters
# -------------------------------
lossparams_schema = ["trade_id","counterparty_id","PD","LGD","EL","BEEL","model_source"]
pd.DataFrame(columns=lossparams_schema).to_csv(os.path.join(OUTPUT_DIR,"LossParameters.csv"), index=False)

# -------------------------------
# RWAResults
# -------------------------------
rwaresults_schema = [
    "trade_id","counterparty_id","counterparty_name","LEI","counterparty_type",
    "external_rating","internal_rating","domicile_country","industry_sector",
    "product_type","notional","currency","maturity_years","off_balance_flag",
    "agreement_id","netting_set_id","threshold","minimum_transfer_amount",
    "independent_amount","margin_frequency","eligible_collateral_types",
    "haircut_schedule","collateral_id","collateral_type","collateral_market_value",
    "collateral_currency","collateral_haircut","collateral_eligibility_flag",
    "guarantee_id","guarantor_id","guarantor_type","guarantor_rating",
    "guarantee_coverage_amount","guarantee_currency","guarantee_maturity_years",
    "guarantee_eligibility_flag","covered_ead","ead","risk_weight","rwa",
    "pre_crm","post_crm","expected_loss","beel","capital_requirement"
]
pd.DataFrame(columns=rwaresults_schema).to_csv(os.path.join(OUTPUT_DIR,"RWAResults.csv"), index=False)

print("🎉 All Basel 3.1 / PRA input templates generated successfully!")
