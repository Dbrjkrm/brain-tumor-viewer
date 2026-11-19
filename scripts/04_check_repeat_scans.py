# 04_check_repeat_scans.py
#
# What this file is for: it checks whether cases that share a BraTS 2023 patient number
# (for example BraTS-GLI-00097-000 and BraTS-GLI-00097-001) really look like the same patient,
# using the other columns of the mapping file. It only reads and prints; it saves nothing.
#
# How it fits the project: Session 4 (Leakage check A). Before we group cases by patient,
# we need evidence that the grouping is right. Checks:
#   1. Do the two scans of each pair come from the same hospital (Site No) and collection (Cohort)?
#   2. Do they have the same patient ID in the original collection (Local ID)?
#   3. Across the WHOLE file, does any Local ID appear under two different patient numbers?
#      (That would be the same person hiding under two names, which the patient number would miss.)
#
# How to run it, from the project folder:
#     .\.venv\Scripts\python.exe scripts\04_check_repeat_scans.py

import pandas as pd

MAPPING_FILE = r"C:\BrainTumorData\meta\BraTS2023_2017_GLI_Mapping.xlsx"
SITE = "Site No (represents the originating institution)"
COHORT = "Cohort Name (if publicly available)"
LOCAL_ID = "Local ID "          # the header really has a space at the end

mapping = pd.read_excel(MAPPING_FILE, dtype=str, keep_default_na=False)

# The patient number is the 5 digits in the middle of the BraTS 2023 name: BraTS-GLI-00097-001 -> 00097.
# The ending (000 or 001) is the last 3 characters.
mapping["patient_number"] = mapping["BraTS2023"].str[10:15]
mapping["ending"] = mapping["BraTS2023"].str[-3:]

cases = mapping[mapping["BraTS2021"] != "N/A"].copy()     # the 1,251 BraTS 2021 cases

# --- Find the patients that have more than one BraTS 2021 case ---
scans_per_patient = cases.groupby("patient_number").size()
repeat_patients = scans_per_patient[scans_per_patient > 1].index
pairs = cases[cases["patient_number"].isin(repeat_patients)].sort_values(["patient_number", "ending"])
print("Patients with more than one case:", len(repeat_patients), "| cases involved:", len(pairs))
print("Scans per such patient:", scans_per_patient[scans_per_patient > 1].value_counts().to_dict())
print("Endings among them:", pairs["ending"].value_counts().to_dict())
print()

# --- Check 1 and 2: within each pair, do Site No, Cohort and Local ID agree? ---
same_site = pairs.groupby("patient_number")[SITE].nunique().eq(1).sum()
same_cohort = pairs.groupby("patient_number")[COHORT].nunique().eq(1).sum()
same_local = pairs.groupby("patient_number")[LOCAL_ID].nunique().eq(1).sum()
print("Pairs with the same Site No:  ", same_site, "of", len(repeat_patients))
print("Pairs with the same Cohort:   ", same_cohort, "of", len(repeat_patients))
print("Pairs with the same Local ID: ", same_local, "of", len(repeat_patients))
print("Site No values in the pairs:", pairs[SITE].value_counts().to_dict())
print("Cohort values in the pairs: ", pairs[COHORT].value_counts().to_dict())
print("Local ID values in the pairs:", pairs[LOCAL_ID].value_counts().to_dict())
print("-> If Local ID is N/A for every pair, it cannot confirm or rule out anything: it is simply not recorded.")
print()

# --- Check 3: does any real Local ID appear under two different patient numbers? ---
# Uses all 1,255 rows, including the 4 BraTS 2020 cases that are not in BraTS 2021.
real_local = mapping[~mapping[LOCAL_ID].str.strip().isin(["N/A", ""])]
names_per_local = real_local.groupby(LOCAL_ID)["patient_number"].nunique()
rows_per_local = real_local.groupby(LOCAL_ID).size()
print("Rows with a real Local ID:", len(real_local), "| distinct Local IDs:", real_local[LOCAL_ID].nunique())
print("Local IDs used by more than one row:", (rows_per_local > 1).sum())
print("Local IDs under more than one patient number:", (names_per_local > 1).sum())
print()

# --- Where do the second scans sit in the BraTS 2021 numbering? ---
second_scans = pairs[pairs["ending"] == "001"]["BraTS2021"]
print("BraTS 2021 IDs of the 118 second scans: from", second_scans.min(), "to", second_scans.max())
all_ids = sorted(cases["BraTS2021"])
block = [i for i in all_ids if second_scans.min() <= i <= second_scans.max()]
print("Cases in that ID range:", len(block), "| of which second scans:", len(second_scans))
