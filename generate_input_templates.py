"""
generate_rwa_output_template.py

Purpose:
- Create a CSV template for RWA calculation output
- Schema aligns with Basel 3.1 / PRA reporting
- Produces RWAResults.csv with headers only (no data yet)
"""

import os
import pandas as pd

# -------------------------------
# Config
# -------------------------------
OUTPUT_DIR = "RWA-Output-Templates"
USER_DIR = "C:/Users/prita/OneDrive/Documents/Basel3.1RWA/RWA-Output-Templates"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(USER_DIR, exist_ok=True)

def save_csv(df, filename):
    """Save CSV to both local and user directories"""
    df.to_csv(os.path.join(OUTPUT_DIR, filename), index=False)
    df.to_csv(os.path.join(USER_DIR, filename), index=False)
    print(f"✅ {filename} saved in both {OUTPUT_DIR} and {USER_DIR}")

# -------------------------------
# RWA Results Schema
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

# -------------------------------
# Create Empty Template
# -------------------------------
df = pd.DataFrame(columns=rwaresults_schema)
save_csv(df, "RWAResults.csv")

print("\n🎉 RWAResults template generated successfully in both locations!")
