# data_lists: which cases are used for what

**What this folder is for.** It holds lists of BraTS 2021 case IDs and labels, and nothing else: no scans, no images, no model output. These lists decide which cases the pretrained model may be tested on. They are committed to Git **before** any model is run, so their commit dates prove they were not adjusted after seeing results.

**The rule (from CLAUDE.md).** Once results exist, these files are never edited. If a mistake is found in them, work stops and the change is discussed, then documented publicly on the Methods page.

## Files

### `case_status.csv` (Session 4, Nov 18, 2026)

One row per BraTS 2021 training case (1,251 rows). Made by `scripts/04_make_case_status.py` from the ID mapping file described in `docs/DATA_ACCESS.md` section 8.3.

| Column | Meaning |
|---|---|
| `case_id` | The case's BraTS 2021 name, as used in the Kaggle copy, for example `BraTS2021_00097` |
| `patient_id` | The patient: the BraTS 2023 name without its timepoint, for example `BraTS-GLI-00097`. 118 patients have two scans (two rows with the same `patient_id`) |
| `status` | `seen_2018`: the patient has a scan in BraTS 2018, the data the model was trained on. `in_earlier_year_not_2018`: the patient has a scan in BraTS 2017, 2019 or 2020, but not 2018. `new_in_2021`: the patient has no scan in any earlier year |

The status is decided per patient: if any scan of a patient was in an earlier year, all of that patient's scans get that status.

Counts: `seen_2018` 285 cases (285 patients); `in_earlier_year_not_2018` 80 cases (80 patients); `new_in_2021` 886 cases (768 patients). Total 1,251 cases, 1,133 patients.

Only `new_in_2021` cases can go into the locked test set or the development pool (Session 5). This is leakage check A. Check B, by source collection, is Session 5.
