# Securitization Portfolio RWA Engine

## Functional Business Requirements (FBR)

---

# 1. Business Objective

Develop a centralized Securitization Capital Calculation Engine capable of calculating Risk Weighted Assets (RWA) and Capital Requirements for all securitization exposures under the Basel III Revised Securitization Framework.

The solution shall:

* Calculate RWA for all securitization positions.
* Support SEC-IRBA, SEC-ERBA and SEC-SA approaches.
* Support STC and Non-STC transactions.
* Provide complete audit trail and regulatory reporting capability.
* Maintain historical calculations for regulatory submissions.
* Support BCBS239 Data Lineage and Data Governance requirements.

---

# 2. Scope

## In Scope

### Regulatory Calculations

* SEC-IRBA
* SEC-ERBA
* SEC-SA
* Capital Requirement Calculation
* Risk Weight Assignment
* RWA Aggregation

### Portfolio Coverage

* Traditional Securitizations
* Synthetic Securitizations
* ABCP Programs
* RMBS
* CMBS
* CLO
* CDO
* Covered Bonds (where applicable)

### Reporting

* Regulatory Capital Reports
* RWA Reporting
* Exposure Reporting
* Stress Testing Inputs
* Internal Management Reporting

---

# 3. High-Level Architecture

```text
Source Systems
      |
      V
+------------------+
| Trade Systems    |
| Treasury Systems |
| Risk Systems     |
| Rating Agencies  |
| Finance Systems  |
+------------------+
      |
      V
+------------------+
| Data Staging     |
+------------------+
      |
      V
+------------------------------+
| Securitization RWA Engine    |
+------------------------------+
      |
      +---- SEC-IRBA
      |
      +---- SEC-ERBA
      |
      +---- SEC-SA
      |
      V
+------------------+
| RWA Repository   |
+------------------+
      |
      V
+------------------+
| Regulatory       |
| Reporting        |
+------------------+
```

---

# 4. Core Data Model

---

## Table 1: SEC_TRANSACTION_MASTER

Stores securitization transaction level information.

| Column Name         | Description                   |
| ------------------- | ----------------------------- |
| Transaction_ID      | Unique Transaction Identifier |
| Transaction_Name    | Deal Name                     |
| Originator          | Transaction Originator        |
| Sponsor             | Transaction Sponsor           |
| Asset_Class         | RMBS/CMBS/CLO etc             |
| Jurisdiction        | Country                       |
| Closing_Date        | Deal Closing Date             |
| Maturity_Date       | Deal Maturity Date            |
| STC_Flag            | STC Indicator                 |
| Regulatory_Approach | IRBA / ERBA / SA              |

---

## Table 2: SEC_POOL_ASSET

Underlying asset pool information.

| Column Name          | Description            |
| -------------------- | ---------------------- |
| Pool_ID              | Asset Pool Identifier  |
| Transaction_ID       | Related Transaction    |
| Asset_Type           | Mortgage/Loan/Card etc |
| Outstanding_Balance  | Pool Balance           |
| Defaulted_Amount     | Default Balance        |
| Delinquent_Amount    | Delinquent Balance     |
| Recovery_Amount      | Recovery Amount        |
| Weighted_Average_LGD | LGD                    |
| Weighted_Average_PD  | PD                     |

---

## Table 3: SEC_TRANCHE

Stores tranche structure.

| Column Name       | Description           |
| ----------------- | --------------------- |
| Tranche_ID        | Tranche Identifier    |
| Transaction_ID    | Transaction Reference |
| Tranche_Name      | Class A/B/C           |
| Seniority         | Senior/Subordinate    |
| Attachment_Point  | A                     |
| Detachment_Point  | D                     |
| Tranche_Thickness | D-A                   |
| Maturity          | MT                    |
| Currency          | Currency              |

---

## Table 4: SEC_POSITION

Bank's investment position.

| Column Name          | Description          |
| -------------------- | -------------------- |
| Position_ID          | Position Identifier  |
| Tranche_ID           | Tranche Reference    |
| Exposure_Amount      | EAD                  |
| Carrying_Value       | Book Value           |
| Off_Balance_Exposure | Off Balance Exposure |
| Exposure_Type        | Investment/Retained  |
| Reporting_Date       | As Of Date           |

---

## Table 5: SEC_RATING

External rating information.

| Column Name    | Description       |
| -------------- | ----------------- |
| Rating_ID      | Rating Record     |
| Tranche_ID     | Tranche           |
| Agency         | Moody's/S&P/Fitch |
| Rating         | AAA, AA etc       |
| Effective_Date | Rating Date       |
| Expiry_Date    | Expiry Date       |

---

## Table 6: SEC_POOL_DELINQUENCY

Required for SEC-SA calculations.

| Column Name       | Description         |
| ----------------- | ------------------- |
| Pool_ID           | Pool Identifier     |
| Delinquent_Amount | Delinquent Exposure |
| Total_Exposure    | Total Exposure      |
| W_Factor          | Delinquency Ratio   |

---

## Table 7: SEC_KIRB_INPUT

Required for SEC-IRBA.

| Column Name | Description                   |
| ----------- | ----------------------------- |
| Pool_ID     | Pool                          |
| KIRB        | Capital Charge                |
| LGD         | Loss Given Default            |
| PD          | Probability of Default        |
| N           | Effective Number of Exposures |

---

## Table 8: SEC_KSA_INPUT

Required for SEC-SA.

| Column Name    | Description                 |
| -------------- | --------------------------- |
| Pool_ID        | Pool                        |
| KSA            | Standardized Capital Charge |
| W              | Delinquency Ratio           |
| Effective_Date | Date                        |

---

## Table 9: SEC_STC_ASSESSMENT

STC eligibility results.

| Column Name     | Description |
| --------------- | ----------- |
| Transaction_ID  | Transaction |
| STC_Flag        | Yes/No      |
| STC_Review_Date | Review Date |
| Assessor        | Reviewer    |
| Comments        | Notes       |

---

## Table 10: SEC_RWA_RESULT

Stores final calculations.

| Column Name         | Description      |
| ------------------- | ---------------- |
| Calculation_ID      | Run ID           |
| Position_ID         | Position         |
| Calculation_Method  | IRBA/ERBA/SA     |
| Risk_Weight         | Assigned RW      |
| RWA                 | Final RWA        |
| Capital_Requirement | Capital          |
| Run_Date            | Calculation Date |

---

# 5. Critical Data Elements (CDE)

| Data Element      | Regulatory Critical |
| ----------------- | ------------------- |
| Exposure Amount   | Yes                 |
| Attachment Point  | Yes                 |
| Detachment Point  | Yes                 |
| KIRB              | Yes                 |
| KSA               | Yes                 |
| Rating            | Yes                 |
| Seniority         | Yes                 |
| Maturity          | Yes                 |
| Delinquency Ratio | Yes                 |
| STC Flag          | Yes                 |
| Risk Weight       | Yes                 |
| RWA               | Yes                 |

---

# 6. Source Systems

| Data Element      | Source System            |
| ----------------- | ------------------------ |
| Exposure Amount   | Treasury System          |
| Trade Details     | Front Office             |
| Tranche Structure | Securitization Platform  |
| Ratings           | Rating Vendor Feed       |
| PD/LGD            | Credit Risk Engine       |
| KIRB              | Basel Engine             |
| KSA               | Standardized Risk Engine |
| Delinquency Data  | Servicer Platform        |
| STC Assessment    | Regulatory Team          |

---

# 7. Regulatory Calculation Inputs

## SEC-IRBA Inputs

| Input            |
| ---------------- |
| KIRB             |
| Attachment Point |
| Detachment Point |
| LGD              |
| N                |
| MT               |
| STC Flag         |

---

## SEC-ERBA Inputs

| Input            |
| ---------------- |
| External Rating  |
| Seniority        |
| Attachment Point |
| Detachment Point |
| Maturity         |
| STC Flag         |

---

## SEC-SA Inputs

| Input            |
| ---------------- |
| KSA              |
| W                |
| Attachment Point |
| Detachment Point |
| STC Flag         |

---

# 8. Calculation Workflow

```text
Load Transaction Data
          |
          V
Load Position Data
          |
          V
Load Ratings
          |
          V
Load Pool Metrics
          |
          V
Determine Approach
(IRBA > ERBA > SA)
          |
          V
Calculate Risk Weight
          |
          V
Calculate RWA
          |
          V
Store Results
          |
          V
Generate Reports
```

---

# 9. Data Quality Rules

| Rule ID | Validation                          |
| ------- | ----------------------------------- |
| DQ001   | Exposure Amount > 0                 |
| DQ002   | Attachment Point < Detachment Point |
| DQ003   | Rating Must Exist for ERBA          |
| DQ004   | KIRB Mandatory for IRBA             |
| DQ005   | KSA Mandatory for SA                |
| DQ006   | Maturity Cannot Be Null             |
| DQ007   | STC Flag Validated                  |
| DQ008   | Exposure Currency Populated         |

---

# 10. Lineage Requirements

For every calculated RWA the system shall provide:

* Source System
* Source Table
* Source Column
* Transformation Logic
* Regulatory Rule Applied
* Calculation Timestamp
* User / Process ID

---

# 11. Regulatory Reports

## Output Reports

### RWA Summary Report

| Field               |
| ------------------- |
| Transaction         |
| Tranche             |
| Exposure            |
| Risk Weight         |
| RWA                 |
| Capital Requirement |

### Capital Adequacy Report

| Field                         |
| ----------------------------- |
| Total Securitization Exposure |
| Total RWA                     |
| Capital Charge                |
| CET1 Impact                   |

### Regulatory Submission Report

* Basel Reporting
* ICAAP Reporting
* Internal Capital Reporting

---

# 12. Non-Functional Requirements

## Performance

* Daily Portfolio Processing
* Support 1 Million+ Positions
* Parallel Processing Capability

## Auditability

* Full Calculation Traceability
* Historical Version Retention
* Regulatory Audit Support

## Data Governance

* Business Glossary Integration
* Metadata Repository Integration
* Data Lineage Support
* Data Quality Monitoring

---

# 13. Success Criteria

The solution shall:

* Produce Basel-compliant RWA calculations.
* Support SEC-IRBA, SEC-ERBA and SEC-SA.
* Provide complete auditability.
* Meet BCBS239 principles.
* Support Regulatory Reporting and Capital Management requirements.
* Maintain historical reproducibility of every calculation run.

---

**Version:** 1.0
**Document Type:** Functional Business Requirements (FBR)
**Domain:** Basel III – Securitization Capital Framework
**Owner:** Risk & Regulatory Capital Team
