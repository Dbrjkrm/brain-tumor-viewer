# 05_spot_check.py
#
# What this file is for: a by-hand check of 5 cases, end to end. For each case it prints the
# raw row from each original file (the Synapse mapping file, TCIA's table) next to what our
# own list data_lists/case_status.csv says, so a person can check by eye that the status and
# source were copied correctly.
#
# How it fits the project: Session 5, Half A, third task. Scripts can be wrong in ways their own
# totals do not show; reading a few raw rows by eye catches that kind of bug.
#
# Which 5 cases: chosen by a rule, not by looking: the lowest-numbered case of each kind:
#   1. seen_2018 from TCGA       2. in_earlier_year_not_2018     3. new_in_2021, a patient with two scans
#   4. new_in_2021 from UPENN    5. new_in_2021 from a private collection (not in TCIA)
#
# It also runs one whole-list check with a third TCIA file, NotPreviouslyInTCIA.csv (a list of file
# paths for cases with no earlier TCIA copy): every case we mark source_in_tcia = "no" should appear
# in it, and no case marked "yes" should.
#
# How to run it, from the project folder:
#     .\.venv\Scripts\python.exe scripts\05_spot_check.py

import os
import pandas as pd

META = r"C:\BrainTumorData\meta"
status = pd.read_csv(os.path.join("data_lists", "case_status.csv"), dtype=str, keep_default_na=False)
synapse = pd.read_excel(os.path.join(META, "BraTS2023_2017_GLI_Mapping.xlsx"), dtype=str, keep_default_na=False)
tcia = pd.read_excel(os.path.join(META, "BraTS2021_MappingToTCIA.xlsx"), dtype=str, keep_default_na=False)

# --- Pick the 5 cases by the rule above (case_status.csv is sorted by case ID, so .iloc[0] is the lowest) ---
two_scan_patients = status["patient_id"][status["patient_id"].duplicated()]
picks = {
    "seen_2018, TCGA": status[(status["status"] == "seen_2018") & status["source"].str.startswith("TCGA")],
    "in_earlier_year_not_2018": status[status["status"] == "in_earlier_year_not_2018"],
    "new_in_2021, two-scan patient": status[(status["status"] == "new_in_2021") & status["patient_id"].isin(two_scan_patients)],
    "new_in_2021, UPENN": status[(status["status"] == "new_in_2021") & status["source"].str.startswith("UPENN")],
    "new_in_2021, private (not in TCIA)": status[(status["status"] == "new_in_2021") & (status["source_in_tcia"] == "no")
                                                 & ~status["source"].str.contains("UCSF|UPENN")],
}

# --- Print each case's raw rows ---
for kind, rows in picks.items():
    case = rows.iloc[0]["case_id"]
    print("=" * 100)
    print(kind, "->", case)
    print("  OUR LIST:", status[status["case_id"] == case].to_dict("records")[0])
    print("  SYNAPSE MAPPING ROW:", synapse[synapse["BraTS2021"] == case].to_dict("records")[0])
    print("  TCIA TABLE ROW:     ", tcia[tcia["BraTS2021 ID"] == case].to_dict("records")[0])
    # For a two-scan patient, also show the other scan of the same patient.
    patient = status[status["case_id"] == case].iloc[0]["patient_id"]
    others = status[(status["patient_id"] == patient) & (status["case_id"] != case)]
    for _, other in others.iterrows():
        print("  SAME PATIENT'S OTHER SCAN:", other.to_dict())

# --- Whole-list check with NotPreviouslyInTCIA.csv ---
# The file has no header; each line is one file path, e.g. ".../new-not-previously-in-TCIA/BraTS2021_00118/BraTS2021_00118_flair.nii.gz"
paths = pd.read_csv(os.path.join(META, "NotPreviouslyInTCIA.csv"), header=None, dtype=str)[0]
ids_in_file = set(paths.str.extract(r"(BraTS2021_\d{5})")[0].dropna())
marked_no = set(status.loc[status["source_in_tcia"] == "no", "case_id"])
marked_yes = set(status.loc[status["source_in_tcia"] == "yes", "case_id"])
print("=" * 100)
print("NotPreviouslyInTCIA.csv: lines", len(paths), "| distinct BraTS 2021 case IDs", len(ids_in_file))
print("Our cases marked source_in_tcia = no: ", len(marked_no), "| of these, found in the file:", len(marked_no & ids_in_file))
print("Our cases marked source_in_tcia = yes:", len(marked_yes), "| of these, found in the file (should be 0):", len(marked_yes & ids_in_file))
missing = sorted(marked_no - ids_in_file)
if missing:
    print("Marked 'no' but missing from the file:", missing)
