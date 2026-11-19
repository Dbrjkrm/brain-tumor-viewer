# Methods notes

**What this file is for.** A running technical record of how the evaluation was done: which cases were used and why, the model's settings, and the tests that show the pipeline is right. The Results & Methods page of the website (Sessions 26–27) is written from this file.

**How it fits the project.** Facts here come from scripts and files in this repo. Sessions 6 and later add paragraphs in Debraj's own words; Claude edits those only for accuracy.

---

## 1. The frozen case lists (Session 5, Nov 19, 2026)

The three lists in `data_lists/` were committed and pushed to GitHub **before any model was run on any case**:

- Commit that froze the lists: **to be filled in by the next commit** (see section 1.1).
- Files: `data_lists/locked_test.csv` (399 cases, 346 patients), `data_lists/dev_pool.csv` (487 cases, 422 patients), `data_lists/seen_sanity.csv` (20 cases).
- SHA-256 fingerprints at the freezing commit: `locked_test.csv` `88e9cbceb24dcceaa7905dad34beaa5cce30dadcbb46a30d3196568e259bacb6`; `dev_pool.csv` `e7cffe57e43bd08d465623bbb98bb9e05016054b1d843544960b98e53ffaae51`; `seen_sanity.csv` `1f32ab7a63811c4217480636a15fa5d33080fa89e78b705937466681bbd0ad82`; `case_status.csv` `cc35b3f87fa888b4dd5e23ad9cfa3fc203071f15f5ff6cbabe05a82abde1894d`.
- Rule (CLAUDE.md): never edited once results exist. Any change found necessary is discussed first and stated publicly on the Methods page.

### 1.1 Commit hash

Filled in after the freezing commit (a commit cannot contain its own hash).

---

## 2. Leakage checks

The model (MONAI `brats_mri_segmentation`, not trained by us) was trained on the 285 BraTS 2018 training cases. A case it may have seen must never be used to test it.

### 2.1 Check A: the organisers' ID mapping (Session 4)

From `BraTS2023_2017_GLI_Mapping.xlsx` (Synapse; `docs/DATA_ACCESS.md` 8.3), decided per patient: `seen_2018` 285 cases, `in_earlier_year_not_2018` 80, `new_in_2021` 886 (768 patients). Only `new_in_2021` is eligible. Script: `scripts/04_make_case_status.py`.

### 2.2 Check B: TCIA's source table (Session 5)

From TCIA's `BraTS2021_MappingToTCIA.xlsx` (`docs/DATA_ACCESS.md` 8.1), a file made by a different organisation from check A's. Script: `scripts/05_add_source.py`. Results:

- All 1,251 cases found in TCIA's table, each exactly once.
- **The 285 seen cases, by source, match their BraTS 2018 names exactly:** 30 named `2013` are all `Collection 4`; 167 named `TCIA01`–`TCIA13` are all TCGA (102 `TCGA-GBM`, 65 `TCGA-LGG`); 88 named `CBICA` are all University of Pennsylvania (86 `UPENN-GBM`, 2 `UPENN-GBM_Additional`). 30 + 167 + 88 = 285.
- **Contradictions: 0.** No unseen case comes from `TCGA-GBM` or `TCGA-LGG`, and no TCIA patient ID belongs to more than one case (UPENN IDs compared without their `_11` timepoint ending).
- 351 cases have no earlier TCIA copy (`new-not-previously-in-TCIA`); all 351, and no other case, appear in TCIA's `NotPreviouslyInTCIA.csv`.
- Institution number agrees between the two files for 1,250 of 1,251 cases. Exception: `BraTS2021_01162` (Collection 9), 24 in TCIA's table, 23 in the Synapse file. It does not affect its status.
- Changed from PLAN.md with Debraj's agreement (Nov 19, 2026): no outside "BraTS 2018 TCGA list" was downloaded. TCIA's table already shows every TCGA case is `seen_2018` and no unseen case is TCGA, so such a list could only re-confirm cases already excluded.

Hand spot-check of 5 cases, chosen by rule (the lowest-numbered case of each kind; `scripts/05_spot_check.py`): `00100` (TCGA, seen), `00115` (IvyGAP, earlier year), `00008` with its second scan `01559` (UCSF two-scan patient), `00155` (UPENN, unseen), `00118` (Collection3, unseen, not in TCIA). Raw rows in both files agree with our list for all 5.

---

## 3. The split (Session 5)

Script: `scripts/05_make_split.py`. numpy 2.5.5, pandas 3.1.1.

- **Seed `20261119`**, fixed before the first run and never changed. Re-running the script gives byte-for-byte identical lists (checked Nov 19, 2026).
- **By patient:** both scans of each of the 118 two-scan patients are on the same side.
- **Stratified** by institution (source collection with `_Additional` removed, since e.g. `UCSF-PDGM` and `UCSF-PDGM_Additional` are the same hospital and a two-scan patient has one scan under each) and by number of scans.
- In each group, round(400 / 886 × patients) go to the locked test set (400 is PLAN.md 5.3's "about 400 cases"). Result: 399 cases.
- `seen_sanity`: 20 of the 285 seen cases, in proportion to institution: 7 TCGA-GBM, 5 TCGA-LGG, 2 Collection 4, 6 UPENN-GBM.

| Group | Patients | Locked test | Dev pool |
|---|---|---|---|
| ACRIN-FMISO-Brain, 1 scan | 4 | 2 | 2 |
| CPTAC-GBM, 1 scan | 33 | 15 | 18 |
| Collection 5, 1 scan | 38 | 17 | 21 |
| Collection 7, 1 scan | 4 | 2 | 2 |
| Collection 9, 1 scan | 1 | 0 | 1 |
| Collection1, 1 scan | 35 | 16 | 19 |
| Collection3, 1 scan | 7 | 3 | 4 |
| UCSF-PDGM, 1 scan | 146 | 66 | 80 |
| UCSF-PDGM, 2 scans | 118 | 53 | 65 |
| UPENN-GBM, 1 scan | 382 | 172 | 210 |

Note: case `BraTS2021_00495` was opened in Session 3 (Nov 16), before these lists existed, to learn the file format (shape, orientation, label values). Nothing was tuned or chosen from it. The seeded split put it in the locked test set, and it was left there rather than moved by hand.

---

## Limitations (notes for the Limitations section, Session 27)

- **The full evaluation runs on the Kaggle copy** of the BraTS 2021 training data (`docs/DATA_ACCESS.md` 8.4), not on files downloaded from TCIA. Only the 8 demo cases are compared value by value with TCIA's own files (Session 14). The checksum comparison of the whole Kaggle copy with TCIA's list is a secondary check, because TCIA said Aspera checksums "have occasionally been unreliable". (Added Nov 19, 2026, at Debraj's request.)
- **The leakage check trusts the organisers' records.** For private-collection cases (351 with no earlier TCIA copy) there is no public patient ID, so "this patient was not in BraTS 2018" rests on the organisers' mapping file alone; check B can confirm the source but not the patient's identity.
- **The reference outlines started as computer output** and were then corrected and approved by experts (`docs/DATA_ACCESS.md` 6.4).
- **`seen_sanity` scores are optimistic by design** (the model trained on those cases) and are never presented as the result.
