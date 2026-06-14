Here’s a **README.md file in plain text** that explains what the pipeline is doing, why it matters under regulation, and the end‑to‑end steps as per Basel 3.1 / PRA rules:

---

# Basel 3.1 / PRA RWA Calculation Pipeline

## Purpose
This project implements an end‑to‑end pipeline for calculating **Risk‑Weighted Assets (RWA)** under the **Basel 3.1 Standardized Approach**, aligned with **PRA (UK)** regulatory expectations. It ensures exposures are correctly classified, EAD is computed, risk weights are applied, and credit risk mitigation (CRM) is reflected in final capital requirements.

---

## Regulatory Context
- **Basel 3.1** introduces updated standardized risk weights, conversion factors (CCFs), and stricter treatment of unrated corporates.  
- **PRA overlays** require conservative floors for certain exposures and stricter eligibility rules for collateral and guarantees.  
- The pipeline follows the regulatory sequence: Exposure → EAD → Risk Weight → RWA → CRM → Capital Requirement.  
- Output aligns with supervisory reporting templates (COREP / PRA returns).

---

## Input Files
The pipeline uses structured CSV templates:

- **Exposures.csv** – trade details, product type, notional, currency, maturity, CCF, EAD.  
- **Counterparties.csv** – counterparty ID, name, LEI, type, ratings, domicile, industry.  
- **Agreements.csv** – netting/CSA agreements, thresholds, margin rules.  
- **Collateral.csv** – collateral type, market value, currency, haircut, eligibility.  
- **Guarantees.csv** – guarantor details, coverage amount, maturity, eligibility.  
- **RiskWeights.csv** – mapping of counterparty type + rating → risk weight %.  
- **RegulatoryParameters.csv** – supervisory haircuts, conversion factors, overlays.  
- **LossParameters.csv** – PD, LGD, EL, BEEL.  

---

## End‑to‑End Calculation Steps

1. **Exposure at Default (EAD)**  
   - On‑balance sheet: EAD = Notional × 100%  
   - Off‑balance sheet: EAD = Notional × CCF  
   - CCF values: 10%, 20%, 50%, 100% depending on product type  

2. **Risk Weight Assignment**  
   - Map counterparty type and rating to risk weight % using RiskWeights.csv  
   - Apply PRA overlays for unrated corporates and sovereign exposures  

3. **RWA Calculation**  
   - RWA = EAD × Risk Weight  

4. **Credit Risk Mitigation (CRM)**  
   - Collateral: apply supervisory haircuts and eligibility rules  
   - Guarantees: substitute guarantor rating/weight if eligible  
   - Compute Pre‑CRM RWA and Post‑CRM RWA  

5. **Expected Loss (EL) and BEEL**  
   - EL = PD × LGD × EAD  
   - BEEL = EL adjusted for CRM  

6. **Capital Requirement**  
   - Capital Requirement = RWA × 8% (Basel minimum)  

---

## Output File
The pipeline produces **RWAResults.csv** with:

- Trade ID, counterparty details, product type, notional, currency, maturity  
- Agreement, collateral, guarantee references  
- Covered EAD, EAD, risk weight, RWA  
- Pre‑CRM, Post‑CRM, Expected Loss, BEEL  
- Capital Requirement  

---

## Usage

1. Generate input templates:  
   `python generate_input_templates.py`

2. Populate input files with trade and counterparty data.

3. Run calculation engine:  
   `python calculate_rwa.py`

4. Review results in:  
   `RWA-Output-Templates/RWAResults.csv`

---

## Notes
- Aligns with Basel 3.1 standardized approach.  
- PRA overlays: stricter treatment for unrated corporates.  
- Error injection in Exposures.csv helps test data quality checks.  
- Output is regulator‑ready and can be mapped to COREP/PRA reporting templates.  

---

Would you like me to now **draft the `calculate_rwa.py` script** that actually reads your input files, applies these steps, and generates the populated `RWAResults.csv`? That would make this README actionable.
