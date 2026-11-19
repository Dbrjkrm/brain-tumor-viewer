# 05_add_source.py
#
# What this file is for: it adds a "source" column (where each case came from) to
# data_lists/case_status.csv, and runs leakage check B: does the source information agree
# with check A (Session 4), and does it reveal any case the model might have seen after all?
#
# How it fits the project: Session 5, Half A. Check A used the organisers' mapping file
# (BraTS2023_2017_GLI_Mapping.xlsx, from Synapse). Check B uses a second, independent file
# made by TCIA: BraTS2021_MappingToTCIA.xlsx, the "mapping table" TCIA's helpdesk pointed us
# to on Nov 19, 2026. If the two files tell the same story, we can trust the unseen pool more.
#
# Three checks are run:
#   1. Every case joins: each of the 1,251 cases is found exactly once in the TCIA table.
#   2. The 285 seen cases, counted by source, must match what their BraTS 2018 names say:
#      30 named "2013" (the original 2013 challenge cases), 167 named "TCIA.." (the TCGA
#      cases) and 88 named "CBICA" (University of Pennsylvania). If not, the script stops.
#   3. Contradictions: an unseen case (new_in_2021) that comes from TCGA-GBM or TCGA-LGG
#      (the TCGA collections BraTS 2018 drew from), or that shares a TCIA patient ID with
#      any other case. Each one found would be treated as seen.
#
# It also compares the institution number recorded in both files (Site ID / Site No).
#
# How to run it, from the project folder:
#     .\.venv\Scripts\python.exe scripts\05_add_source.py

import os
import sys
import pandas as pd

TCIA_TABLE = r"C:\BrainTumorData\meta\BraTS2021_MappingToTCIA.xlsx"
SYNAPSE_MAPPING = r"C:\BrainTumorData\meta\BraTS2023_2017_GLI_Mapping.xlsx"
CASE_STATUS = os.path.join("data_lists", "case_status.csv")
NOT_IN_TCIA = "new-not-previously-in-TCIA"   # what the TCIA table writes instead of a patient ID

# --- Load the three tables, every cell as plain text (so "N/A" stays the text "N/A") ---
status = pd.read_csv(CASE_STATUS, dtype=str, keep_default_na=False)
tcia = pd.read_excel(TCIA_TABLE, dtype=str, keep_default_na=False)
synapse = pd.read_excel(SYNAPSE_MAPPING, dtype=str, keep_default_na=False)

# Give the TCIA table's long column names short ones. Printed first so the renaming can be checked.
print("TCIA table columns, as written:", list(tcia.columns))
tcia.columns = ["collection", "tcia_site_id", "tcia_patient_id", "study_date",
                "case_id", "segmentation_cohort", "mgmt_cohort", "mgmt_value"]

# Keep only the segmentation training cases (the table also lists validation cases and
# 9 rows used only for the separate MGMT task).
tcia_training = tcia[tcia["segmentation_cohort"] == "Training"]
print("TCIA table rows:", len(tcia), "| segmentation training rows:", len(tcia_training),
      "| each case ID once:", tcia_training["case_id"].is_unique)

# --- Check 1: the join. how="left" keeps every case in our list, found or not ---
joined = status.merge(tcia_training[["case_id", "collection", "tcia_site_id", "tcia_patient_id"]],
                      on="case_id", how="left")
not_found = joined["collection"].isna().sum()
print("Cases in case_status.csv:", len(status), "| after the join:", len(joined),
      "| not found in the TCIA table:", not_found)
if not_found > 0 or len(joined) != len(status):
    sys.exit("STOP: some cases did not join exactly once.")

# The new columns: the source collection exactly as TCIA's table names it, and whether
# that case's scans exist in a TCIA source collection (i.e. has a real TCIA patient ID).
joined["source"] = joined["collection"]
joined["source_in_tcia"] = ["no" if p == NOT_IN_TCIA else "yes" for p in joined["tcia_patient_id"]]

# --- Counts: status by source ---
print()
print("Cases by source and status:")
print(pd.crosstab(joined["source"], joined["status"], margins=True, margins_name="total").to_string())

# --- Check 2: the 285 seen cases by source, against their BraTS 2018 names ---
# A BraTS 2018 name looks like "Brats18_TCIA01_231_1"; the second part ("TCIA01", "2013", "CBICA")
# says which group the organisers put the case in.
synapse_2018 = synapse[(synapse["BraTS2021"] != "N/A") & (synapse["BraTS2018"] != "N/A")].copy()
group = synapse_2018["BraTS2018"].str.split("_").str[1]
synapse_2018["group_2018"] = ["TCIA (TCGA)" if g.startswith("TCIA") else g for g in group]
seen = joined[joined["status"] == "seen_2018"].merge(
    synapse_2018[["BraTS2021", "group_2018"]], left_on="case_id", right_on="BraTS2021", how="left")
print()
print("The", len(seen), "seen_2018 cases: BraTS 2018 name group (rows) by TCIA source (columns):")
print(pd.crosstab(seen["group_2018"], seen["source"], margins=True, margins_name="total").to_string())

expected = {"2013": 30, "TCIA (TCGA)": 167, "CBICA": 88}
counted = seen["group_2018"].value_counts().to_dict()
sources_by_group = {
    "2013": {"Collection 4"},
    "TCIA (TCGA)": {"TCGA-GBM", "TCGA-LGG"},
    "CBICA": {"UPENN-GBM", "UPENN-GBM_Additional"},
}
problems = []
if len(seen) != 285:
    problems.append(f"{len(seen)} seen cases, expected 285")
if counted != expected:
    problems.append(f"group counts {counted}, expected {expected}")
for g, allowed in sources_by_group.items():
    actual = set(seen.loc[seen["group_2018"] == g, "source"])
    if not actual <= allowed:
        problems.append(f"group {g} has sources {actual}, expected only {allowed}")
if problems:
    print("PROBLEMS:", problems)
    sys.exit("STOP: the 285 seen cases do not split by source as expected. Discuss before going on.")
print("Check 2 passed: 285 seen cases = 30 (2013, all Collection 4) + 167 (TCGA, all TCGA-GBM/LGG) "
      "+ 88 (CBICA, all UPENN-GBM).")

# --- Check 3: contradictions ---
unseen = joined[joined["status"] == "new_in_2021"]
tcga_unseen = unseen[unseen["source"].isin(["TCGA-GBM", "TCGA-LGG"])]
print()
print("Unseen cases from TCGA-GBM or TCGA-LGG:", len(tcga_unseen))

# Same TCIA patient under two BraTS case IDs? UPENN-GBM IDs end in a timepoint ("_11" for the
# first scan), so compare the part before the "_".
real_ids = joined[joined["tcia_patient_id"] != NOT_IN_TCIA].copy()
real_ids["tcia_patient_base"] = real_ids["tcia_patient_id"].str.split("_").str[0]
shared = real_ids[real_ids.duplicated("tcia_patient_base", keep=False)]
print("Cases sharing a TCIA patient ID with another case:", len(shared))
if len(shared):
    print(shared[["case_id", "patient_id", "status", "source", "tcia_patient_id"]].to_string(index=False))

contradictions = len(tcga_unseen) + len(shared)
print("Contradictions found:", contradictions)
if contradictions:
    sys.exit("STOP: contradictions found. Each must be marked seen; discuss before saving.")

# --- Extra check: the institution number in both files ---
site = joined.merge(synapse[["BraTS2021", "Site No (represents the originating institution)"]],
                    left_on="case_id", right_on="BraTS2021", how="left")
site_match = (site["tcia_site_id"] == site["Site No (represents the originating institution)"])
print()
print("Institution number agrees between the two files:", site_match.sum(), "of", len(site))
if not site_match.all():
    print(site.loc[~site_match, ["case_id", "source", "tcia_site_id",
                                 "Site No (represents the originating institution)"]].to_string(index=False))

# --- Save: the same rows as before, plus the two new columns ---
output = joined[["case_id", "patient_id", "status", "source", "source_in_tcia"]].sort_values("case_id")
output.to_csv(CASE_STATUS, index=False, lineterminator="\n")
print()
print("Saved", CASE_STATUS, "with", len(output), "rows and columns", list(output.columns))
