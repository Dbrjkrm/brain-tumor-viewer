# 05_make_split.py
#
# What this file is for: it makes the three frozen case lists the rest of the project uses:
#   data_lists/locked_test.csv   about 400 unseen cases. All headline numbers and all demo cases come
#                                from here. Never used to tune or choose anything.
#   data_lists/dev_pool.csv      the other unseen cases. Kept for the fine-tuning stretch goal and v2.
#   data_lists/seen_sanity.csv   20 cases the model was trained on (seen_2018). Used only to check the
#                                pipeline works (Session 10); their numbers are optimistic by design.
#
# How it fits the project: Session 5, Half B. PLAN.md section 5.3. These lists are committed to Git
# BEFORE any model is run on them, so their commit date proves they were not adjusted after results.
# Once results exist they are never edited (CLAUDE.md, Rigor rules).
#
# How the split works:
#   - Only new_in_2021 cases are eligible (leakage checks A and B, Sessions 4 and 5).
#   - The split is by PATIENT, not by case: both scans of a two-scan patient go to the same list.
#   - It is STRATIFIED: patients are shuffled and dealt out separately within each group, so each
#     list gets a fair share of every group. A patient's group is their institution (the source
#     collection with "_Additional" removed, because e.g. UCSF-PDGM and UCSF-PDGM_Additional are the
#     same hospital, and a two-scan patient has one scan under each label) plus whether they have one
#     or two scans (so the number of cases, not just patients, comes out near 400).
#   - In each group, round(TEST_FRACTION x number of patients) go to the locked test set.
#   - The shuffle uses a fixed SEED, chosen before the first run (Nov 19, 2026) and never changed.
#     The same seed and the same input always give the same lists.
#
# How to run it, from the project folder:
#     .\.venv\Scripts\python.exe scripts\05_make_split.py

import os
import sys
import numpy as np
import pandas as pd

SEED = 20261119                 # fixed before the first run; never change it to get a "nicer" split
TARGET_TEST_CASES = 400         # PLAN.md 5.3: "about 400 cases"
SANITY_CASES = 20               # PLAN.md: 20 seen cases
CASE_STATUS = os.path.join("data_lists", "case_status.csv")

status = pd.read_csv(CASE_STATUS, dtype=str, keep_default_na=False)

# The institution: the source label without "_Additional".
status["institution"] = status["source"].str.replace("_Additional", "", regex=False)

# One random-number generator, made once from the seed, used for every shuffle below in a fixed order.
rng = np.random.default_rng(SEED)
print("Seed:", SEED, "| numpy", np.__version__, "| pandas", pd.__version__)

# ---------------------------------------------------------------------------------------------
# Part 1: locked test set and development pool, from the unseen cases
# ---------------------------------------------------------------------------------------------
pool = status[status["status"] == "new_in_2021"].copy()

# One row per patient: their institution and how many scans they have.
patients = pool.groupby("patient_id").agg(institution=("institution", "first"),
                                          n_institutions=("institution", "nunique"),
                                          n_scans=("case_id", "size")).reset_index()
if (patients["n_institutions"] != 1).any():
    sys.exit("STOP: a patient has scans from two institutions.")
patients["group"] = patients["institution"] + " | " + patients["n_scans"].astype(str) + " scan(s)"

test_fraction = TARGET_TEST_CASES / len(pool)
print("Unseen pool:", len(pool), "cases,", len(patients), "patients | test fraction = 400 /",
      len(pool), "=", round(test_fraction, 4))

# Go through the groups in alphabetical order (a fixed order, so the run is repeatable).
# Within each group, sort the patient IDs, shuffle them with the seeded generator, and put the
# first round(fraction x size) into the test set.
test_patients = []
summary = []
for group in sorted(patients["group"].unique()):
    ids = sorted(patients.loc[patients["group"] == group, "patient_id"])
    shuffled = list(rng.permutation(ids))
    n_test = int(round(test_fraction * len(ids)))
    test_patients += shuffled[:n_test]
    summary.append((group, len(ids), n_test, len(ids) - n_test))

print()
print(f"{'group':45} {'patients':>8} {'test':>6} {'dev':>6}")
for group, n, n_test, n_dev in summary:
    print(f"{group:45} {n:>8} {n_test:>6} {n_dev:>6}")

pool["list"] = ["locked_test" if p in set(test_patients) else "dev_pool" for p in pool["patient_id"]]
locked_test = pool[pool["list"] == "locked_test"]
dev_pool = pool[pool["list"] == "dev_pool"]

# ---------------------------------------------------------------------------------------------
# Part 2: 20 seen cases for the pipeline sanity check, dealt in proportion to their institution
# ---------------------------------------------------------------------------------------------
seen = status[status["status"] == "seen_2018"].copy()
sanity_ids = []
print()
print("seen_sanity, by institution:")
for inst in sorted(seen["institution"].unique()):
    ids = sorted(seen.loc[seen["institution"] == inst, "case_id"])
    n_pick = int(round(SANITY_CASES * len(ids) / len(seen)))
    sanity_ids += list(rng.permutation(ids))[:n_pick]
    print(f"  {inst:20} {len(ids):>4} seen cases -> {n_pick} picked")
seen_sanity = seen[seen["case_id"].isin(sanity_ids)]

# ---------------------------------------------------------------------------------------------
# Part 3: checks. Any failure stops the script before anything is saved.
# ---------------------------------------------------------------------------------------------
problems = []
if set(locked_test["patient_id"]) & set(dev_pool["patient_id"]):
    problems.append("a patient is in both locked_test and dev_pool")
if len(locked_test) + len(dev_pool) != len(pool):
    problems.append("locked_test + dev_pool does not equal the unseen pool")
if (locked_test["status"] != "new_in_2021").any() or (dev_pool["status"] != "new_in_2021").any():
    problems.append("a non-unseen case got into locked_test or dev_pool")
if len(seen_sanity) != SANITY_CASES or (seen_sanity["status"] != "seen_2018").any():
    problems.append("seen_sanity is not 20 seen_2018 cases")
if set(seen_sanity["case_id"]) & set(pool["case_id"]):
    problems.append("a seen_sanity case is also in the unseen pool")
if problems:
    sys.exit("STOP: " + "; ".join(problems))

print()
print("locked_test:", len(locked_test), "cases,", locked_test["patient_id"].nunique(), "patients")
print("dev_pool:   ", len(dev_pool), "cases,", dev_pool["patient_id"].nunique(), "patients")
print("seen_sanity:", len(seen_sanity), "cases")
print("All checks passed: no patient on both sides, totals add up, statuses correct.")

print()
print("Cases by source in each list:")
both = pd.concat([locked_test, dev_pool])
print(pd.crosstab(both["source"], both["list"], margins=True, margins_name="total").to_string())

# Session 3 opened case 00495 to learn the file format (before these lists existed). Say where it landed.
for case in ["BraTS2021_00495"]:
    where = status.loc[status["case_id"] == case, "status"].iloc[0]
    in_list = pool.loc[pool["case_id"] == case, "list"]
    print()
    print(case, "| status", where, "| list:", in_list.iloc[0] if len(in_list) else "not in the unseen pool")

# ---------------------------------------------------------------------------------------------
# Part 4: save. IDs and labels only, sorted by case ID.
# ---------------------------------------------------------------------------------------------
columns = ["case_id", "patient_id", "status", "source"]
for name, table in [("locked_test", locked_test), ("dev_pool", dev_pool), ("seen_sanity", seen_sanity)]:
    path = os.path.join("data_lists", name + ".csv")
    table[columns].sort_values("case_id").to_csv(path, index=False, lineterminator="\n")
    print("Saved", path, "with", len(table), "rows")
