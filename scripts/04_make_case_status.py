# 04_make_case_status.py
#
# What this file is for: it gives every BraTS 2021 training case a leakage status and a patient ID,
# and saves them as data_lists/case_status.csv (IDs and labels only, no scan data).
#
# How it fits the project: Session 4 (Leakage check A). The pretrained model was trained on the
# BraTS 2018 training cases. A case it may have seen must never be used to test it.
# The three statuses:
#   seen_2018                 the patient has a scan in BraTS 2018: the model trained on it
#   in_earlier_year_not_2018  the patient has a scan in BraTS 2017, 2019 or 2020, but not 2018
#   new_in_2021               the patient has no scan in any earlier year: the only cases eligible for testing
#
# The rule is applied PER PATIENT, not per scan: 118 patients have two scans (a first scan and a
# follow-up). If any scan of a patient was in an earlier year, all of that patient's scans get that
# status. Where the patient ID comes from: the BraTS 2023 name "BraTS-GLI-00097-001" is the 5-digit
# case ID (00097) and the 3-digit timepoint (001), as the BraTS 2023 submission page states
# (see docs/DATA_ACCESS.md section 8.3).
#
# How to run it, from the project folder:
#     .\.venv\Scripts\python.exe scripts\04_make_case_status.py

import os
import pandas as pd

MAPPING_FILE = r"C:\BrainTumorData\meta\BraTS2023_2017_GLI_Mapping.xlsx"
OUTPUT_FILE = os.path.join("data_lists", "case_status.csv")
EARLIER_YEARS = ["BraTS2017", "BraTS2018", "BraTS2019", "BraTS2020"]

# Read every cell as plain text; keep "N/A" as the text "N/A" (see 04_look_at_mapping.py).
mapping = pd.read_excel(MAPPING_FILE, dtype=str, keep_default_na=False)

# Keep the 1,251 BraTS 2021 cases. (The 4 rows with "N/A" here are BraTS 2020 cases not in BraTS 2021.)
cases = mapping[mapping["BraTS2021"] != "N/A"].copy()

# Patient ID: "BraTS-GLI-00097-001" -> "BraTS-GLI-00097" (everything before the timepoint).
cases["patient_id"] = cases["BraTS2023"].str[:15]

# Per scan: was this scan in BraTS 2018? Was it in any earlier year at all? (True or False for each row.)
cases["scan_in_2018"] = cases["BraTS2018"] != "N/A"
cases["scan_in_any_earlier"] = (cases[EARLIER_YEARS] != "N/A").any(axis=1)

# Per patient: was ANY scan of this patient in 2018 / in any earlier year?
# groupby("patient_id") puts each patient's scans together; transform("any") gives every scan
# of that patient the answer for the whole patient.
cases["patient_in_2018"] = cases.groupby("patient_id")["scan_in_2018"].transform("any")
cases["patient_in_any_earlier"] = cases.groupby("patient_id")["scan_in_any_earlier"].transform("any")

# Turn the True/False answers into a status. The order matters: 2018 is checked first.
def status_from(in_2018, in_any_earlier):
    if in_2018:
        return "seen_2018"
    if in_any_earlier:
        return "in_earlier_year_not_2018"
    return "new_in_2021"

cases["status"] = [status_from(a, b) for a, b in zip(cases["patient_in_2018"], cases["patient_in_any_earlier"])]

# For comparison only: the status each scan would get if we looked at that scan alone.
cases["status_scan_alone"] = [status_from(a, b) for a, b in zip(cases["scan_in_2018"], cases["scan_in_any_earlier"])]

# --- Report ---
print("Cases:", len(cases), "| each listed once:", cases["BraTS2021"].is_unique)
print("Patients:", cases["patient_id"].nunique())
print("Scans per patient:", cases.groupby("patient_id").size().value_counts().sort_index().to_dict())
print()
print("Status per patient rule (cases):")
for status, count in cases["status"].value_counts().sort_index().items():
    patients = cases.loc[cases["status"] == status, "patient_id"].nunique()
    print(" ", status, "|", count, "cases |", patients, "patients")
print("  total |", len(cases))
print()
changed = cases[cases["status"] != cases["status_scan_alone"]]
unseen_alone = (cases["status_scan_alone"] == "new_in_2021").sum()
unseen_patient = (cases["status"] == "new_in_2021").sum()
print("Unseen pool, judging each scan alone:  ", unseen_alone, "cases")
print("Unseen pool, judging by patient:        ", unseen_patient, "cases")
print("Cases removed from the unseen pool by the patient rule:", unseen_alone - unseen_patient)
print("Cases whose status changed at all:", len(changed))
if len(changed):
    print(changed[["BraTS2021", "patient_id", "status_scan_alone", "status"]].to_string(index=False))

# --- Save: IDs and labels only, sorted by case ID ---
os.makedirs("data_lists", exist_ok=True)
output = cases[["BraTS2021", "patient_id", "status"]].rename(columns={"BraTS2021": "case_id"})
output = output.sort_values("case_id")
output.to_csv(OUTPUT_FILE, index=False, lineterminator="\n")
print()
print("Saved", OUTPUT_FILE, "with", len(output), "rows and columns", list(output.columns))
