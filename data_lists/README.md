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

Only `new_in_2021` cases can go into the locked test set or the development pool. This is leakage check A.

**Added Nov 19, 2026 (Session 5, `scripts/05_add_source.py`):** two more columns, from TCIA's table `BraTS2021_MappingToTCIA.xlsx` (leakage check B):

| Column | Meaning |
|---|---|
| `source` | The source collection exactly as TCIA's table names it, for example `UCSF-PDGM`, `TCGA-GBM`, `Collection 5`. This is what each case cites (TCIA's advice, `docs/DATA_ACCESS.md` 10.1) |
| `source_in_tcia` | `yes` if the case has a TCIA patient ID in an earlier TCIA collection; `no` if TCIA's table says `new-not-previously-in-TCIA` (351 cases) |

Check B found 0 contradictions, and the 285 `seen_2018` cases split by source exactly as their BraTS 2018 names say (30 + 167 + 88). Details in `docs/METHODS_NOTES.md`.

### `locked_test.csv`, `dev_pool.csv`, `seen_sanity.csv` (Session 5, Nov 19, 2026)

Made by `scripts/05_make_split.py` with seed `20261119`. Columns: `case_id`, `patient_id`, `status`, `source` (same meanings as above).

| File | Cases | Patients | What it is for |
|---|---|---|---|
| `locked_test.csv` | 399 | 346 | All headline numbers and all 8 demo cases. Never used to tune or choose anything |
| `dev_pool.csv` | 487 | 422 | The rest of the unseen pool. Fine-tuning stretch goal and v2 only |
| `seen_sanity.csv` | 20 | 20 | Cases the model trained on. Pipeline check only (Session 10); their scores are optimistic by design and are never the result |

The split is by patient (both scans of a two-scan patient are on the same side) and stratified by institution and by number of scans. How and why: `docs/METHODS_NOTES.md`.
