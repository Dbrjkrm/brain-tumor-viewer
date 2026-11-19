# PLAN.md: Brain Tumor Viewer

Written Nov 16, 2026 by the planning session (Claude Fable 5.2) from PROJECT_BRIEF.md and two rounds of questions with Debraj.

**How to use this file.** Start each build session with "Do session N from PLAN.md". Tick the boxes at the end. If a session is not finished, leave its boxes unticked and finish it in the next buffer session. Never skip ahead past an unticked box without writing why in the Session log at the bottom.

---

## 1. The project in one paragraph

A free, open-source website where anyone can open 8 real brain MRI cases, see an AI model's outline of the tumor in 3D and in slices, and compare it to the expert-approved outline. The model is a pretrained one (not trained by me), evaluated on several hundred cases it has never seen, with Dice and HD95 reported honestly, including failures. Research and education only, not for diagnosis.

## 2. Fixed dates

| Dates | What happens |
|---|---|
| Mon Nov 16 – Wed Dec 9 | Core build: data, leakage check, inference, evaluation, viewer |
| Thu Dec 10 – Fri Dec 18 | Exam period. Light work only: review and writing, no new concepts. Exam days (Dec 11, 12, 13, 18) are optional |
| Sat Dec 19 | Aim: site feature-complete. Anything unfinished moves to January |
| Sun Dec 20 – Tue Dec 22 | Main Fable review |
| Dec 23 – Jan 9 | Thailand. Zero planned work |
| Sun Jan 10 – Sun Jan 31 | Review fixes, MedMNIST warm-up, stretch goal (if chosen), polish, write-up, full checkpoints |
| Thu Jan 28 | Short final Fable check |
| Sun Jan 31 | Done |
| Feb 1 – 14 | Outreach (checklist in section 9; outside the build scope) |

Session shape: 1 hour, split into Half A and Half B (30 minutes each, around Fajr). Each half ends at a natural stopping point. On days with 1.5–2 hours, use the extra time on the "If you have extra time" list in section 8, or start the next session's Half A.

Every Sunday is a **buffer session**: finish anything unticked from the week. If nothing is unticked, do an item from the extra-time list or rest.

## 3. What the planning session verified

| Claim in the brief | Finding | Source |
|---|---|---|
| Model: MONAI `brats_mri_segmentation`, SegResNet, trained on BraTS 2018 | Confirmed. Bundle v0.5.4, Apache 2.0 licence. Trained on the 285 BraTS 2018 training cases | Bundle README and metadata.json |
| Input: T1c, T1, T2, FLAIR. Output: WT, TC, ET | Confirmed. Input order is T1c, T1, T2, FLAIR. Output channel order is **TC, WT, ET** (not WT first) | metadata.json |
| Dice about 0.90 WT, 0.86 TC, 0.79 ET | Confirmed as reported: 0.9026 / 0.8559 / 0.7905. But measured on the authors' **own 42-case split** of the 285 cases, not the official BraTS validation set | Bundle README |
| BraTS 2021 on TCIA is CC BY 4.0 | Confirmed for the challenge NIfTI package, which includes the labels. Scans are brain-extracted | TCIA collection page (version of 2023-08-25) |
| A BraTS-to-TCIA crosswalk exists | Confirmed: `BraTS2021_MappingToTCIA.xlsx`, small direct download | TCIA collection page |

Source links:
- https://huggingface.co/MONAI/brats_mri_segmentation
- https://github.com/Project-MONAI/model-zoo/tree/dev/models/brats_mri_segmentation
- https://www.cancerimagingarchive.net/analysis-result/rsna-asnr-miccai-brats-2021/ (DOI 10.7937/jc8x-9874)
- https://www.synapse.org/Synapse:syn25829067 (BraTS 2021 on Synapse)

**Not verified yet (each has a hands-on check in a session):**
- ~~The exact name and columns of the mapping file.~~ Answered in Session 2: `BraTS2023_2017_GLI_Mapping.xlsx` (Synapse syn51615438, in the BraTS 2023 project, not the 2021 one). Columns in `docs/DATA_ACCESS.md` 8.3.
- ~~Whether the TCIA Aspera package lets you download single cases.~~ Answered in Session 2: single files can be selected in the browser listing; an actual transfer (needs the Aspera client) is tested in Buffer B1.
- NiiVue's left-right handling and phone performance. Checked in Sessions 18 and 34.
- Current free GPU limits on Kaggle and Colab. Kaggle answered in Session 3: the account shows 30 GPU hours a week, usable only after phone verification (done by Debraj, confirmed Nov 19, 2026; first GPU run is Session 7). Colab was not checked; it is the fallback and is checked only if Kaggle fails.
- The bundle's exact inference settings (normalisation, sliding window). Read from `inference.json` in Session 7.

## 4. Where the brief was wrong or unrealistic

1. **"Verify these Dice numbers yourself" cannot be done exactly.** The authors' 200/42/43 split is made at run time without a properly fixed seed and the case IDs are not published. So nobody can re-run their validation set. What we do instead: run the model on about 20 cases it has certainly seen (BraTS 2018 training cases), as a pipeline sanity check. Those numbers are optimistic by design and are labelled that way.
2. **The split being unrecoverable means all 285 BraTS 2018 training cases count as "seen".** We cannot use the authors' 43 "test" cases as held-out data.
3. **The TCIA crosswalk alone does not prove a case is unseen.** It maps BraTS 2021 IDs to TCIA IDs, not to BraTS 2018 IDs. The plan uses two independent checks (section 5.3).
4. **The TCIA download is a single 142 GB Aspera package.** It will not be downloaded to the laptop. Heavy data stays in the cloud.
5. **"Never commit scan files to Git" conflicts with static hosting.** The 8 demo cases must live somewhere public. Decision in section 5.6: a separate small data repo. Debraj confirmed this on Nov 16, 2026.
6. **"Expert outline" needs careful wording.** The BraTS 2021 labels were, as I understand the BraTS 2021 paper, produced by fusing earlier algorithms' outputs and then manually refined and approved by neuroradiologists. Session 2 confirms this in the paper. The site should say "expert-approved reference outline", not "drawn by hand by an expert".
7. **HD95 has undefined cases.** Some tumors have no enhancing region. The rule for those cases must be written down before any results are seen (Session 11).
8. **3-hour sessions and 2–4 hours/week** are replaced by daily 1-hour sessions, per Debraj's update.
9. **The Colab notebook deliverable** will need the reader's own Kaggle or Synapse login to fetch the data. That is normal for BraTS and gets stated in the README.
10. **Phone support** stays a nice-to-have. 3D volume rendering on a phone may be slow; slices should work.

## 5. Answers to "Questions the plan must answer"

### 5.1 Which viewer: NiiVue

| | NiiVue | vtk.js | three.js |
|---|---|---|---|
| Built for NIfTI brain scans | Yes | Partly | No |
| Slices and 3D in one synced canvas | Built in | Build it yourself | Build it yourself |
| Overlays (tumor on brain) | Built in | Possible, more code | Build it yourself |
| Beginner readability | A few dozen lines | Steep | Very steep for medical data |
| Phone | Runs where WebGL2 runs; to be tested | Heavy | Depends on what you build |

Choice: **NiiVue**, in a plain **Vite + JavaScript** site with no framework (no React). Reason: the least code Debraj has to be able to explain. Hosting: **GitHub Pages**. Build sessions must check NiiVue's current docs rather than rely on memory of its API.

### 5.2 Volume sizes, compression, hosting

- One BraTS volume is 240 × 240 × 155 voxels. Each case has 4 scans plus a label map. Expect roughly 10–15 MB per case as downloaded (compressed). Measure in Session 3.
- For the web: convert each scan to 8-bit (0–255) after clipping extreme intensities, and save as `.nii.gz`. Expect roughly 1–2 MB per scan. Label maps compress to well under 1 MB.
- 8 cases × (4 scans + AI mask + expert mask) is expected to be 50–100 MB total. The site loads one case at a time, and loads T1c first.
- GitHub Pages limits: 100 MB per file, about 1 GB per site. We are far below both.

### 5.3 Leakage: which cases count as held out

A case is **held out** only if it passes both checks:

- **Check A (ID mapping):** in the BraTS 2021-to-earlier-years mapping file, the case has no ID in any earlier BraTS year (2017–2020). This is stricter than "not in 2018" and also protects against the same patient appearing twice.
- **Check B (source collection):** using the TCIA crosswalk and `NotPreviouslyInTCIA.csv`, record which institution or collection each case came from. Report results by source, and confirm no held-out case traces to a TCIA subject that appears in the BraTS 2018 TCGA-GBM/LGG lists.

If the mapping file for Check A cannot be obtained, the fallback is Check B alone, restricted to collections that were not part of BraTS 2018 at all, with that limitation stated on the Methods page.

The held-out pool is then split once, with a recorded random seed, stratified by source:

- **Locked test set** (about 400 cases, or 60% of the pool if it is smaller than expected). All headline numbers and all demo cases come from here. It is never used to tune anything.
- **Development pool** (the rest). Reserved for the fine-tuning stretch goal and for v2.

The ID lists are committed to Git **before** any inference on them. Only IDs, never scans.

### 5.4 Does inference fit on a free GPU

Expected yes. SegResNet is small, and one case should take seconds on a free T4. About 400 cases should take 1–2 hours as an unattended Kaggle run. **Primary platform: Kaggle** (BraTS 2021 is already hosted there as a dataset, and the weekly GPU quota is predictable). Fallbacks, in order: Colab free tier; CPU inference on Kaggle (minutes per case, run overnight on fewer cases); one month of Colab Pro (within budget).

### 5.5 Data route (brief question 9)

- **Licence we rely on for public display:** TCIA's CC BY 4.0 release, with full attribution (dataset DOI, the three BraTS papers, six source-dataset citations, the TCGA acknowledgement sentence).
- **Where compute reads the data:** a cloud copy (the Kaggle-hosted BraTS 2021 dataset, or the official Synapse copy pulled straight into the cloud notebook).
- **The gap to close in Session 2:** show that the files we display are the same files TCIA licenses. First choice: download only the 8 demo cases from the TCIA package and compare checksums. If the package is all-or-nothing, ask the TCIA helpdesk to confirm in writing, and record the answer in `docs/DATA_ACCESS.md`.
- **Changed Nov 19, 2026 (agreed with Debraj).** The 8 demo cases are downloaded straight from the TCIA package (single files can be selected) and only those files are displayed. Kaggle is for compute only. Each of the 8 is compared value by value with its Kaggle copy (grid, orientation header, every voxel), which shows the AI outline (made from the Kaggle copy) sits exactly on the displayed scan. The Kaggle-vs-TCIA checksum comparison in Buffer B1 becomes a secondary check, because TCIA said Aspera checksums "have occasionally been unreliable"; the 3D Slicer check by eye in Session 14 is the main check that the files look right. The full evaluation still runs on the Kaggle copy; that is stated as a limitation.
- **Synapse terms:** read them in Session 2 and write down what they say about redistribution. If they forbid redistributing files obtained through Synapse, the displayed files must come from TCIA or from a copy shown to be identical.

### 5.6 Where the demo files live

A second public repo, `brain-tumor-viewer-data`, served by GitHub Pages. It contains only the 8 curated, web-compressed demo cases, their masks, metrics JSON, and a LICENSE/ATTRIBUTION file. The code repo `brain-tumor-viewer` contains **no scan files at all**. This is a narrow, deliberate exception to "no scan files in Git": the files are public, de-identified, CC BY 4.0, and a few MB each.

### 5.7 Case selection for the demo

Chosen by a rule written down before looking at pictures, to avoid cherry-picking: from the locked test set, 2 cases near the median Dice, 2 from the top quarter, 2 clear failures of different kinds (bottom tenth), and 2 chosen for variety (for example a very small tumor, or one with no enhancing region). Every pick is checked slice by slice in 3D Slicer. The Methods page says how they were chosen.

### 5.8 Metrics

Dice and HD95 for WT, TC and ET, per case. Reported as mean ± SD (as the brief asks) and also median with interquartile range, because HD95 is skewed. Number of cases, number of undefined cases and the rule used for them are always shown next to the numbers. Also reported: results by source collection, and the seen-case sanity numbers, clearly labelled as not held out.

### 5.9 Risks and the cut list

| Risk | Likelihood | Response |
|---|---|---|
| Mapping file not obtainable | Medium | Fallback in 5.3 |
| Cannot show displayed files match the TCIA release | Medium | Changed Nov 19, 2026: display TCIA's own files for the 8 demo cases, compared value by value with the Kaggle copy. Hosting question (U6) asked of TCIA, and UTM Library's copyright office asked by Debraj; site launch waits on both, the build does not |
| Kaggle GPU needs phone verification or quota runs out | Low | Colab; CPU run |
| Pipeline bug (wrong channel order, wrong labels) | Medium | Session 10 tests: seen-case sanity run and channel-swap test |
| Left-right flipped in the viewer | Medium | Session 18 proof against 3D Slicer; re-checked in the Fable review |
| Exams or travel eat more time than planned | High | Sunday buffers; Dec 19 is an aim, not a wall |
| Understanding falls behind the code | Medium | Daily three-sentence explain-back; 8 full checkpoints; a session does not count as done until the explain-back passes |

**Cut list, first to go at the top:**
1. Fine-tuning stretch goal
2. Custom domain
3. Phone support
4. 3D surface meshes for the tumor (keep volume overlay)
5. Results by source collection
6. Demo cases reduced from 8 to 5
7. MedMNIST warm-up

**Never cut:** the leakage check, the locked test set, correct metrics, two failure cases, left-right correctness, the disclaimer, attribution, and the explain-backs.

### 5.10 The stretch goal (fine-tuning)

**Does it fit in January with the Jan 31 deadline?** A small version fits, on two conditions: the site was feature-complete by Dec 19 (or within two sessions of it), and the Fable review produced at most three sessions of must-fix work.

- **Decision date: Wed Jan 13**, after the review fixes are triaged. **Latest safe date to say yes: Fri Jan 15.**
- **Hard stop: Sun Jan 24.** If there is no finished, checked comparison by then, the stretch goal leaves v1 and is not mentioned in the write-up except as a next step.
- **What "small version" means:** fine-tune the pretrained model for a few epochs on the development pool, then compare it to the baseline on the same locked test set, case by case. Report it whatever the outcome, including "no improvement".
- If the answer on Jan 13 is no, Sessions 37–40 become the polish track instead.

### 5.11 Budget

Required spend: $0. Optional: a domain (about $15/year), one month of Colab Pro only if both free platforms fail.

---

## 6. Explain-back rules

- **Every session** ends with: "Explain today in three sentences": what we built, why, and one thing that could go wrong with it. Claude corrects gently and asks one follow-up. About 5 minutes.
- **Full checkpoints (8)** are interviewer-style. Claude plays a PI, asks the listed questions plus follow-ups, and Debraj answers without notes. Claude then says plainly which answers were solid and which need work. Weak answers are written into the Session log and re-asked at the next checkpoint.

---

## 7. Sessions

From Nov 18, 2026 (Session 4 onward), Claude does every step in the boxes below and runs every command, explaining as it goes; Debraj follows along. Steps only Debraj can do (sign-ins, accepting terms, phone verification, API tokens, sending email, approving a download over 2 GB) are listed together at the start of each session. See "How a session runs" in CLAUDE.md. The explain-backs and full checkpoints are unchanged.

### Stage 0: Setup and data access

#### Session 1: Mon Nov 16. Project skeleton
Half A
- [x] Check whether this project folder is really syncing to OneDrive. If it is, decide with Claude whether to move the repo to a non-synced folder (thousands of small build files sync badly)
- [x] `git init`, add `.gitignore` (node_modules, .venv, *.nii, *.nii.gz, data folders), first commit
- [x] Create the public GitHub repo `brain-tumor-viewer` and push

Half B
- [x] Create `C:\BrainTumorData` with a short README saying what belongs there
- [x] Add README.md stub with the not-for-diagnosis statement, and LICENSE (MIT for code, unless Debraj prefers another)
- [x] Confirm the data-repo decision in section 5.6 (confirmed by Debraj on Nov 16, 2026: yes, separate data repo)
- [x] Fill in the "Commands" section of CLAUDE.md with what was actually run
- [x] Explain today in three sentences

Works when: the repo is visible on GitHub with README, LICENSE, PLAN.md, CLAUDE.md and PROJECT_BRIEF.md.

#### Session 2: Tue Nov 17. Data route and licence gate
Half A
- [x] Read the TCIA BraTS 2021 page together. Write `docs/DATA_ACCESS.md`: licence, required citations, what is and is not allowed
- [x] Download the small files to `C:\BrainTumorData\meta`: `BraTS2021_MappingToTCIA.xlsx`, `NotPreviouslyInTCIA.csv` (well under 2 GB)
- [x] Open the TCIA Aspera package link and see whether single cases can be selected. Do not download anything large

Half B
- [x] On Synapse, find the file mapping BraTS 2021 IDs to earlier years. Record its exact name, location and columns. Download it (small)
- [x] Read the Synapse data-use terms. Record what they say about redistribution and public display
- [x] If single-case TCIA download is impossible, draft the TCIA helpdesk email (Debraj sends it himself). Single cases can be selected, but the email was drafted anyway for other reasons: `docs/TCIA_HELPDESK_EMAIL.md`. **Sent by Debraj on Nov 18, 2026**; waiting on TCIA's reply
- [x] In the BraTS 2021 paper (arXiv 2107.02314), find how the labels were made and note the exact wording
- [x] Explain today in three sentences

Works when: `docs/DATA_ACCESS.md` states the chosen route, what is still unconfirmed, and who was asked.

#### Session 3: Wed Nov 18. First look at a real case (in the cloud)
Half A
- [x] On Kaggle: confirm GPU access is enabled (phone verification if asked) and note the weekly quota shown in the account. Half done on Nov 16, 2026: quota noted (30 GPU hours a week); the account was not phone-verified yet. **Phone verification done by Debraj himself (some time before Nov 19); he confirmed it on Nov 19, 2026.** GPU access has not been tested with a run on purpose: Session 7 is the first GPU run
- [x] Find the hosted BraTS 2021 training dataset. Record its exact name, uploader and case count in `docs/DATA_ACCESS.md`
- [x] New notebook: list one case's files and their sizes

Half B
- [x] Load one case with nibabel. Print shape, voxel size, data type and the orientation codes
- [x] Plot one slice of each of the 4 scans and the label map. Print the label values present (expect 0, 1, 2, 4; if 3 appears instead of 4, note it)
- [x] Save the notebook to the repo under `notebooks/` (saved with its text outputs and without the scan picture)
- [x] Explain today in three sentences. Attempted on Nov 16, 2026 and not passed; repeated at the start of Session 4 on Nov 18, 2026 and passed (see the Session log)

Works when: Debraj can point at the four scan types and say what each label value means.

### Stage 1: The held-out list

#### Session 4: Thu Nov 19. Leakage check A (ID mapping)
Half A
- [x] Load the mapping file with pandas. Look at 10 rows together and explain each column
- [x] Count cases by "earliest BraTS year they appeared in"

Half B
- [x] Mark every BraTS 2021 training case as `seen_2018`, `in_earlier_year_not_2018`, or `new_in_2021`
- [x] Save `data_lists/case_status.csv` (IDs and status only; changed Nov 18, 2026, with Debraj's agreement, to add a `patient_id` column and to decide the status per patient). Check the totals add up to the dataset's case count
- [x] Explain today in three sentences

Works when: there is a table of counts per status that sums correctly.

#### Session 5: Fri Nov 20. Leakage check B and locking the test set
Half A
- [x] Join the TCIA crosswalk to `case_status.csv`. Add a `source` column (collection or institution, or "not in TCIA")
- [x] Look for contradictions: any `new_in_2021` case whose TCIA subject is in the BraTS 2018 TCGA lists. Resolve each one by treating it as seen. (Changed Nov 19, 2026, with Debraj's agreement: no outside TCGA list is downloaded; the check uses the TCIA crosswalk and the mapping file already on the laptop, plus a count of the 285 seen cases by source. Reason in the Session log)
- [x] Spot-check 5 cases by hand, end to end

Half B
- [x] Split the held-out pool into locked test set and development pool, stratified by source, with a recorded seed. Split by patient (`patient_id` in `case_status.csv`): both scans of a two-scan patient go on the same side (added Nov 18, 2026)
- [x] Save `data_lists/locked_test.csv`, `data_lists/dev_pool.csv`, `data_lists/seen_sanity.csv` (20 seen cases)
- [x] Commit and push the lists **now**, before any inference. Note the commit hash in `docs/METHODS_NOTES.md`
- [x] Explain today in three sentences

Works when: the three lists are on GitHub with a commit date earlier than any results.

#### Session 6: Sat Nov 21. FULL CHECKPOINT 1: data and leakage
Half A: checkpoint. Questions a PI would ask:
- [ ] What is BraTS, and where do these scans come from?
- [ ] What are the four MRI sequences and why does a tumor look different in each?
- [ ] What is data leakage, in one sentence, and why would it make your numbers look better than they are?
- [ ] How exactly did you decide a case was unseen? What would make that check wrong?
- [ ] Why can't you use the model authors' own test split?
- [ ] Why lock a test set before running anything?
- [ ] Under what licence are you showing these scans, and what do you owe in return?

Half B
- [ ] Write the "Dataset" and "Leakage check" paragraphs in `docs/METHODS_NOTES.md`, in Debraj's own words, Claude editing only for accuracy
- [ ] Log weak answers in the Session log

#### Buffer B1: Sun Nov 22
Start-of-session list for Debraj (one-time, if not already done): ~~phone-verify the Kaggle account~~ (done; confirmed by Debraj Nov 19, 2026); ~~create a Kaggle API token~~ (done Nov 18, 2026); be ready to approve anything the IBM Aspera installer or download page asks of the browser.
- [x] Set up the Kaggle command-line tool in `.venv` and check it can see the account. Record its version. Done early, Nov 18, 2026: `kaggle` 2.2.5 (plus `six` 1.17.0), login works (see CLAUDE.md)
- [ ] Aspera test (moved from Session 2): install the IBM Aspera client, download `RSNA-ASNR-MICCAI-BraTS-2021.sums` (47.5 MB) and one 125 KB label file. Record the checksum type in `docs/DATA_ACCESS.md`
- [ ] Compare the Kaggle copy's checksums against the `.sums` list (needs Session 3's Kaggle dataset; run through the Kaggle command-line tool). Record the result. **Secondary check (changed Nov 19, 2026):** a mismatch is recorded and reported, but does not block launch; see section 5.5

### Stage 2: Running the model

#### Session 7: Mon Nov 23. Download the model and run one case
Half A
- [ ] In the Kaggle notebook, install MONAI and download the bundle. Record bundle version and MONAI version
- [ ] Read `inference.json` together, line by line in plain English: loading, normalisation, sliding window, sigmoid, threshold. Write the settings into `docs/METHODS_NOTES.md`

Half B
- [ ] Run the model on one locked-test case on GPU. Record time and GPU memory used
- [ ] Print the output shape and say what each of the 3 channels is (TC, WT, ET)
- [ ] Explain today in three sentences

Works when: one prediction exists and its shape matches the input scan.

#### Session 8: Tue Nov 24. From model output to regions, and a first Dice by hand
Half A
- [ ] Convert the expert label map (1, 2, 4) into the three nested regions WT, TC, ET. Draw the nesting on paper first
- [ ] Plot AI vs expert-approved outline on three slices for each region

Half B
- [ ] Write a 5-line Dice function. Work one tiny example on paper and check the function gives the same answer
- [ ] Compute Dice for the three regions on this case
- [ ] Save the prediction as a NIfTI file with the same orientation information as the input
- [ ] Explain today in three sentences

Works when: three Dice numbers exist for one case and Debraj can compute Dice on a 4×4 grid by hand.

#### Session 9: Wed Nov 25. Check it in 3D Slicer
Half A
- [ ] Install 3D Slicer (about 1 GB installer; allowed, it is under 2 GB)
- [ ] Download that one case and its prediction to `C:\BrainTumorData\cases` (tens of MB)

Half B
- [ ] Load scans, expert labels and AI prediction in Slicer. Scroll all three planes
- [ ] Record in `docs/ORIENTATION.md`: which side of the brain the tumor is on, with a screenshot, and how Slicer labels left and right. This is the reference the website must match
- [ ] Explain today in three sentences

Works when: the tumor's side is written down with a screenshot.

#### Session 10: Thu Nov 26. Prove the pipeline is right
Half A
- [ ] Run the model on the 20 `seen_sanity` cases. Compare mean Dice to the bundle's reported numbers. They should be in the same range; if far lower, stop and find the bug
- [ ] Write down why this number is optimistic and must never be presented as the result

Half B
- [ ] Channel-swap test: feed the scans in a wrong order on 3 cases and confirm Dice drops sharply
- [ ] Label test: confirm a perfect prediction (the expert labels themselves) scores Dice 1.0 through our own code
- [ ] Record all three test results in `docs/METHODS_NOTES.md`
- [ ] Explain today in three sentences

Works when: the three tests pass and are written up.

### Stage 3: Evaluation

#### Session 11: Fri Nov 27. FULL CHECKPOINT 2, then metric rules
Half A: checkpoint (model and inference). PI questions:
- [ ] What does this model take in and give out? Why three overlapping regions rather than three separate ones?
- [ ] In broad strokes, what is a U-Net-style network doing? What is SegResNet's variation?
- [ ] Why does the scan get normalised before the model sees it?
- [ ] You did not train this model. What exactly is your contribution?
- [ ] How do you know you fed the scans in the right order?
- [ ] Why were the "seen case" numbers higher, and why is that expected?
- [ ] What is a sigmoid and what does thresholding at 0.5 mean here?

Half B
- [ ] Learn HD95 on paper with two small shapes. Why the 95th percentile and not the maximum
- [ ] Write `docs/METRIC_RULES.md` **before seeing results**: voxel spacing used, what happens when a region is empty in the reference, in the prediction, or in both, and what gets reported
- [ ] Commit it

#### Session 12: Sat Nov 28. Metrics code, tests, and launch the big run
Half A
- [ ] Write the metrics module (Dice and HD95 per region), following `METRIC_RULES.md`
- [ ] Tests with known answers: identical shapes, shifted cube, empty region. Cross-check our Dice against MONAI's on 5 cases

Half B
- [ ] Assemble the batch notebook: loop over `locked_test.csv`, save each prediction and one row of metrics per case
- [ ] Dry run on 5 cases. Then start the full run as a background Kaggle job
- [ ] Explain today in three sentences

Works when: tests pass and the full run is running or finished.

#### Buffer B2: Sun Nov 29
- [ ] Also: confirm the batch run finished and download `metrics_per_case.csv` (small)

#### Session 13: Mon Nov 30. Read the results honestly
Half A
- [ ] Mean ± SD and median with IQR for Dice and HD95, per region. Count undefined cases
- [ ] Histograms of Dice per region. What does a long left tail mean?

Half B
- [ ] Table by source collection. Table of held-out vs seen-sanity
- [ ] List the 20 worst cases. Look at 5 of them in the notebook and write one line each on what went wrong
- [ ] Save tables and figures to `results/`. Every number on the site will come from these files
- [ ] Explain today in three sentences

Works when: `results/summary.json` and the figures exist and are committed.

#### Session 14: Tue Dec 1. Choose and check the demo cases
Half A
- [ ] Write the selection rule from section 5.7 into `docs/METHODS_NOTES.md` first
- [ ] Apply it. Produce a shortlist of 12

Half B
- [ ] Download the 12 shortlisted cases and predictions to `C:\BrainTumorData\cases` (expected under 300 MB; check the size before downloading)
- [ ] Check each in 3D Slicer. Pick the final 8. Write 2 sentences per case on what it shows. This check by eye is the main check that the files look right (TCIA's advice, Nov 19, 2026)
- [ ] Download the final 8 cases from the TCIA package (Aspera, about 8 MB each) to `C:\BrainTumorData\tcia_cases`. Compare each with its Kaggle copy value by value (grid, orientation header, every voxel); if any differ, stop and discuss. Open each TCIA case in Slicer and check it by eye. Only these TCIA files are made into web files (changed Nov 19, 2026; replaces "compare checksums for these 8")
- [ ] Explain today in three sentences

Works when: 8 case IDs are fixed, with notes, including at least 2 failures.

#### Session 15: Wed Dec 2. FULL CHECKPOINT 3, then prepare web files
Half A: checkpoint (metrics and results). PI questions:
- [ ] Define Dice. What Dice would two half-overlapping equal shapes get?
- [ ] What does HD95 capture that Dice misses? Give an example where Dice is high and HD95 is bad
- [ ] Why is ET the hardest region?
- [ ] Your numbers versus the reported ones: higher or lower, and why might that be?
- [ ] What did you do when a tumor had no enhancing region, and when did you decide that?
- [ ] Why report median as well as mean?
- [ ] Show me a failure. What do you think went wrong, and how sure are you?
- [ ] How did you pick the cases on the website? Could you have made the model look better?

Half B
- [ ] Write `scripts/prepare_web_case.py`: clip intensities, convert to 8-bit, keep orientation information, save `.nii.gz`; write masks and a per-case `case.json` with its metrics
- [ ] Run it on one case, reading the TCIA file (Session 14). Record file sizes
- [ ] Reload the output in Slicer and confirm nothing flipped

### Stage 4: The viewer

#### Session 16: Thu Dec 3. First pixels in the browser
Half A
- [ ] Create the Vite project in `site/`. Run the dev server. Explain what `index.html`, `main.js` and `package.json` each do
- [ ] Add NiiVue (check its current docs for the install and API)

Half B
- [ ] Show one T1c scan in a four-panel layout: axial, coronal, sagittal, 3D
- [ ] Scroll, rotate, zoom. Confirm the crosshair moves all views together
- [ ] Explain today in three sentences

Works when: a real brain is on screen at localhost.

#### Session 17: Fri Dec 4. Tumor overlays and region toggles
Half A
- [ ] Load the AI mask as an overlay with a fixed colour per region. Choose colours that work for colour-blind viewers
- [ ] Toggles for WT, TC, ET

Half B
- [ ] Load the expert-approved mask. Add the switch: AI, reference, or both (both shown as fill plus outline, or two colours)
- [ ] Opacity slider
- [ ] Explain today in three sentences

Works when: any region of either outline can be shown or hidden in every view.

#### Session 18: Sat Dec 5. Left-right proof
Half A
- [ ] Turn on radiological convention (patient's left on screen right) and on-screen L/R labels
- [ ] Compare against the Session 9 Slicer screenshot, for the same case and slice

Half B
- [ ] Repeat for a second case with the tumor on the other side
- [ ] Add both comparisons to `docs/ORIENTATION.md` with screenshots
- [ ] Add a one-line note under the viewer explaining the convention to visitors
- [ ] Explain today in three sentences

Works when: two side-by-side screenshot pairs agree.

#### Buffer B3: Sun Dec 6

#### Session 19: Mon Dec 7. Case picker and scores
Half A
- [ ] Run `prepare_web_case.py` for all 8 cases, from the TCIA files. Write `cases.json` listing them
- [ ] Case picker in the page. Loading indicator while a case downloads

Half B
- [ ] Panel showing that case's Dice and HD95 per region, with a plain-language line for each region
- [ ] Scan-type switch (T1c, T1, T2, FLAIR), loading the others only when asked
- [ ] Explain today in three sentences

Works when: all 8 cases load and show their own numbers.

#### Session 20: Tue Dec 8. Pages and the disclaimer
Half A
- [ ] Not-for-diagnosis banner visible without scrolling on every page
- [ ] Site navigation: Viewer, Results & Methods, About

Half B
- [ ] Results & Methods page skeleton, with the summary table generated from `results/summary.json` (no hand-typed numbers)
- [ ] About page skeleton: Debraj Karmaker, independent personal project, not affiliated with or endorsed by the university, what was AI-assisted
- [ ] Explain today in three sentences

Works when: three pages exist and the banner cannot be missed.

#### Session 21: Wed Dec 9. Put it on the internet
Half A
- [ ] Create `brain-tumor-viewer-data` with the 8 web cases and LICENSE/ATTRIBUTION. Enable GitHub Pages. (Skip if the TCIA confirmation (U6) is still open, or if UTM Library's copyright office has objected or not yet replied: then deploy with one placeholder case and note it. Changed Nov 19, 2026: the library gate is "no objection", not an explicit yes; whatever the library says is recorded in `docs/DATA_ACCESS.md` section 10)
- [ ] Point the site at the data URL

Half B
- [ ] Deploy `site/` to GitHub Pages. Open the live link on the laptop
- [ ] Open it on a phone once and write down what happens (no fixing today)
- [ ] Explain today in three sentences

Works when: a public URL shows the viewer.

### Stage 5: Exam period (light work, no new concepts)

#### Session 22: Thu Dec 10. FULL CHECKPOINT 4: the viewer
PI questions:
- [ ] What happens, step by step, between someone opening the link and seeing a brain?
- [ ] Why is there no server running the model?
- [ ] What is a NIfTI file and what is in its header that matters for left and right?
- [ ] How do you know your left and right are correct?
- [ ] Why did you convert the scans to 8-bit, and what was lost?
- [ ] Why NiiVue and not building it yourself?
- [ ] Where do the numbers on the page come from? Could one be mistyped?

#### Sessions 23–25: Fri Dec 11, Sat Dec 12, Sun Dec 13 (exam days, optional)
- [ ] Optional, 15–30 minutes: reread one of `METHODS_NOTES.md`, `METRIC_RULES.md`, `ORIENTATION.md` and explain it aloud

#### Session 26: Mon Dec 14. Results & Methods text, part 1
- [ ] Dataset, model and leakage-check sections, adapted from `METHODS_NOTES.md`
- [ ] Full citations and attribution block as TCIA requires, including each demo case's own source collection (U7, U15) and the Kaggle compute-data credit (`docs/DATA_ACCESS.md` 3.5, added Nov 19, 2026)
- [ ] Explain today in three sentences

#### Session 27: Tue Dec 15. Results & Methods text, part 2
- [ ] Results section with the generated table and two figures
- [ ] Two failure cases with images and an honest explanation, including what is not known
- [ ] Limitations section (include the notes in `docs/METHODS_NOTES.md` "Limitations", among them that the full evaluation runs on the Kaggle copy and only the 8 demo cases are compared value by value with TCIA's files)
- [ ] Explain today in three sentences

#### Session 28: Wed Dec 16. About page and README
- [ ] Finish the About page
- [ ] README: what it is, live link, how to run the site locally, how to reproduce the evaluation, results summary, licences, attribution
- [ ] Explain today in three sentences

#### Session 29: Thu Dec 17. Reproducibility notebook
- [ ] Tidy the notebook so it runs top to bottom: get data, load lists, run model, compute metrics, make the tables
- [ ] Add an "Open in Colab" link and a note that the reader needs their own data access
- [ ] Start a clean run in the background
- [ ] Explain today in three sentences

#### Session 30: Fri Dec 18 (last exam, optional)
- [ ] Optional: check the clean notebook run reproduced `summary.json` (small differences are expected; the bundle is documented as non-deterministic. Note the size of the difference)

#### Session 31: Sat Dec 19. FULL CHECKPOINT 5 and feature-complete pass
Half A
- [ ] Go through the brief's "Website features" list. Tick what exists. Write everything unfinished into the January list (section 8)
- [ ] Debraj's own review: read every page as a skeptical PI and list what he would attack

Half B: checkpoint (whole project, 10 minutes, no notes)
- [ ] Give the 2-minute version of the project
- [ ] What is the single weakest part of it?
- [ ] What would you do with three more months?
- [ ] What did you learn about reading brain MRI?

### Stage 6: Main Fable review (run these three on Fable 5.2)

#### Session 32: Sun Dec 20. Review 1: is the evaluation true?
- [ ] Re-derive the held-out list from the raw mapping files independently and compare to the committed lists
- [ ] Confirm the lists were committed before the results (Git history)
- [ ] Recompute metrics for 10 random cases with independent code. Compare to `metrics_per_case.csv`
- [ ] Check `METRIC_RULES.md` was followed for every undefined case
- [ ] Check every number on the site against `results/`
- [ ] Explain today in three sentences

#### Session 33: Mon Dec 21. Review 2: orientation, claims, licence
- [ ] Left-right re-check on 3 cases against Slicer
- [ ] Read every sentence on the site and README for overclaiming. Nothing may imply diagnosis or clinical use
- [ ] Attribution complete against the TCIA requirements. Data-route question from Session 2 closed, or launch blocked on it
- [ ] Code read-through: comments in every file, nothing Debraj cannot explain
- [ ] Explain today in three sentences

#### Session 34: Tue Dec 22. Review 3: triage and pack up
- [ ] Sort findings into must-fix, should-fix, won't-fix (with reasons). Write them into section 8
- [ ] Phone test properly; record results
- [ ] Commit and push everything. Confirm the live site matches the repo
- [ ] Write a "where I left off" note at the top of the Session log for Jan 10
- [ ] Explain the review's three most important findings in three sentences each

### Trip: Dec 23 – Jan 9. No sessions.
If Wi-Fi is good and you feel like it: reread the docs and explain them aloud. Do not build.

### Stage 7: January (Opus for building; Fable where marked)

#### Session 35: Sun Jan 10. Re-entry
- [ ] Before opening anything: explain the whole project aloud from memory. Note what was fuzzy
- [ ] Reread the "where I left off" note and the must-fix list
- [ ] Run the site locally and open the live link. Confirm nothing broke

#### Session 36: Mon Jan 11. Must-fix, part 1
- [ ] Work the must-fix list from the top
- [ ] Explain today in three sentences

#### Session 37: Tue Jan 12. Must-fix, part 2
- [ ] Finish must-fix. Re-run any affected results
- [ ] Explain today in three sentences

#### Session 38: Wed Jan 13. Stretch-goal decision, then MedMNIST part 1
Half A
- [ ] Decide the stretch goal using section 5.10. Write the decision and the reason in the Session log

Half B
- [ ] MedMNIST in Colab: load a tiny dataset, look at images and labels, define a very small network
- [ ] Explain today in three sentences

#### Session 39: Thu Jan 14. MedMNIST part 2
- [ ] Train it. Watch the loss go down. Plot training vs validation accuracy
- [ ] Break it on purpose: train too long, or with too little data, and see overfitting
- [ ] Explain today in three sentences

#### Session 40: Fri Jan 15. FULL CHECKPOINT 6: what training is
PI questions:
- [ ] What is a loss function? What was it for the tumor model?
- [ ] What happens in one training step?
- [ ] Training, validation, test: what is each for? Map them onto this project
- [ ] What is overfitting and how did you see it?
- [ ] What is fine-tuning and why might it help on BraTS 2021 data?
- [ ] Why does training need a GPU when your website does not?

Half B
- [ ] Should-fix items, or start the track below

#### Session 41: Sat Jan 16. Track day 1
**If stretch = yes:** 
- [ ] Split the development pool into fine-tune-train and fine-tune-validation. Commit the lists. The locked test set is not touched
- [ ] Set up the fine-tuning notebook from the bundle's training config. Run 1 epoch as a test

**If stretch = no (polish track):**
- [ ] Visual design pass: type, spacing, colour, a real landing section

#### Buffer B4: Sun Jan 17

#### Session 42: Mon Jan 18. Track day 2
**Stretch:** 
- [ ] Launch the fine-tuning run in the background. While it runs, write down the hypothesis and what result would count as "no improvement"

**Polish:** 
- [ ] Loading states, error messages, keyboard use, readable on a small laptop

#### Session 43: Tue Jan 19. Track day 3
**Stretch:** 
- [ ] Pick the checkpoint using the validation split only. Run it once on the locked test set

**Polish:** 
- [ ] Phone layout: slices first, 3D optional

#### Session 44: Wed Jan 20. Track day 4
**Stretch:** 
- [ ] Case-by-case comparison with the baseline on the same cases: how many improved, how many got worse, size of the difference, and a paired statistical test explained in plain words
- [ ] Add a short, honest section to the Results page

**Polish:** 
- [ ] Optional 3D surface meshes for the tumor, or deeper failure-case write-ups

#### Session 45: Thu Jan 21. FULL CHECKPOINT 7
If stretch: PI questions:
- [ ] What exactly did you change and what stayed fixed?
- [ ] Why is it fair to compare on the locked test set? What would have made it unfair?
- [ ] Is the difference real or noise? How do you know?
- [ ] If it did not improve, why might that be?

If no stretch: failure-analysis checkpoint:
- [ ] Walk through both failure cases on screen. What anatomy is involved? What would a radiologist say? What would you test next?

#### Session 46: Fri Jan 22. Design polish 1
- [ ] Visual design pass (or second pass). Compare against two real product sites Debraj likes
- [ ] Explain today in three sentences

#### Session 47: Sat Jan 23. Design polish 2
- [ ] Remaining should-fix items. Check the site on a second browser
- [ ] Decide on the custom domain (optional)
- [ ] Explain today in three sentences

#### Buffer B5: Sun Jan 24
- [ ] Stretch hard stop: if the comparison is not finished and checked, remove it from v1 today

#### Session 48: Mon Jan 25. Write-up draft
- [ ] Debraj drafts the 1–2 page write-up himself from the docs: motivation, dataset and licence, method in plain language, results, failure cases, limitations, next steps, what he learned about reading brain MRI
- [ ] Claude checks every number against `results/` and flags any overclaiming. Wording stays modest: "a pretrained model that achieved X on N held-out cases from a public dataset"

#### Session 49: Tue Jan 26. Write-up final, README final, notebook final
- [ ] Revise the write-up. Export to PDF
- [ ] Final README. Final clean notebook run
- [ ] Explain today in three sentences

#### Session 50: Wed Jan 27. FULL CHECKPOINT 8: mock interview, no notes
- [ ] 20 minutes as a PI, 10 minutes as a med-school interviewer. Questions drawn from all earlier checkpoints, plus every weak answer in the Session log
- [ ] "Why should I take a first-year into my lab on the strength of this?"
- [ ] "What part of this did the AI do and what part did you do?"
- [ ] List anything still shaky. Those get reviewed on Jan 29–30

#### Session 51: Thu Jan 28. Final Fable check (run on Fable 5.2)
- [ ] Confirm every must-fix from December is closed
- [ ] Re-check: held-out lists unchanged since Nov 20 (Git), site numbers match `results/`, left-right, disclaimer, attribution, write-up claims
- [ ] If the stretch goal is included: locked test set was used exactly once for the fine-tuned model
- [ ] Final list of fixes, each small enough for one session

#### Session 52: Fri Jan 29. Final fixes
- [ ] Apply the fixes. Redeploy
- [ ] Review the shaky answers from Session 50

#### Session 53: Sat Jan 30. Release
- [ ] Explain the whole project without notes one last time, start to finish
- [ ] Tag `v1.0` on GitHub. Check the live link, the README link, the notebook link and the PDF in a private browser window
- [ ] One-page CV has the project line and link

#### Sun Jan 31: Done. Last buffer if needed.

---

## 8. Running lists

**If you have extra time (in rough priority order):**
- Re-explain an earlier stage aloud without notes
- Read the Myronenko 2018 paper's abstract and figure 1, and the BraTS 2021 paper's data section
- Glossary in `docs/GLOSSARY.md`, one term per day in your own words
- Start the next session's Half A

**Moved to January (filled in on Dec 19):**
- 

**Review findings (filled in on Dec 22 and Jan 28):**
- Must-fix:
- Should-fix:
- Won't-fix, with reason:

## 9. Feb 1–14 outreach checklist (outside the build scope)

- [ ] List 3–5 possible reviewers (UTM profs, TAs, course instructors). Send short critique requests with the live link and the write-up. Ask one specific question each
- [ ] Shortlist 5–10 UofT labs with active funding and recent papers in imaging, neuro or computational work
- [ ] For each lab: read the latest paper, note one specific method or figure, and find the grad students and postdocs as well as the PI
- [ ] Draft each email: what you can concretely help with, the live site link, the one-page CV attached
- [ ] Apply reviewer critique that is quick to apply before sending. Log the rest as v2 notes
- [ ] Send in small batches. Track replies in a simple sheet

## 10. Room for later versions

- **v2 (own model):** the development pool and the locked test set already exist, so a trained or fine-tuned model can be compared fairly on day one. nnU-Net is the benchmark to beat.
- **v3 (head-trauma bleeds on CT):** the viewer takes any NIfTI volume plus label maps and a `case.json`, so a CT module is a new data folder and a new set of region names, not a rewrite. Dataset and licence still to be researched.

## 11. Session log

Add one line per session: date, session number, what got done, anything carried over, weak explain-back answers to revisit.

- **Nov 16, 2026, Session 1 (run on Fable 5.2 at Debraj's request, for today only).** Done: folder confirmed not syncing to OneDrive (it sits outside the OneDrive folder; no move needed); `.gitignore`, first commit `340e7eb`; public repo https://github.com/Dbrjkrm/brain-tumor-viewer created and pushed; README stub, MIT LICENSE, `C:\BrainTumorData` with README, Commands section in CLAUDE.md. Change from plan: the repo was created with GitHub CLI (`gh` 2.104.0, installed with winget at Debraj's request) instead of in the browser. Incident: `git init` was first run in `C:\Users\debra` by mistake (Claude had not given the `cd` command); stopped, the stray `.git` deleted, nothing committed or uploaded. Lesson: check the prompt shows the project folder before any Git command. Nothing carried over. **Weak explain-back answers to revisit:** (1) described the whole project instead of today's work; (2) said "detection" and "building a model": it is *segmentation* (outlining where the tumor is; every case already has one) by a pretrained model we *evaluate*, not build; (3) called the data "MRI photos from the internet" rather than 3D scans from a public, licensed research dataset (BraTS 2021); (4) gave tidiness as the reason for `.gitignore` and missed the main one: scan files, model weights and login tokens must never become public. Solid: the model is pretrained; research only; named both error directions (healthy tissue marked as tumor, tumor marked as healthy).
- **Nov 16, 2026, Session 2 (run on Fable 5.2 at Debraj's request; switched to Opus 5.5 for the explain-back and wrap-up).** Done: `docs/DATA_ACCESS.md` written from primary sources with exact quotes and CONFIRMED/UNCONFIRMED labels; `BraTS2021_MappingToTCIA.xlsx`, `NotPreviouslyInTCIA.csv` and `BraTS2023_2017_GLI_Mapping.xlsx` saved to `C:\BrainTumorData\meta` with SHA-256 fingerprints; TCIA helpdesk email drafted (`docs/TCIA_HELPDESK_EMAIL.md`, not sent yet). Labels confirmed in the paper: fused output of three algorithms, refined by volunteer neuroradiologists, approved by two senior neuroradiologists, so "expert-approved reference outline" stands. **Plan changes agreed with Debraj:** (1) Synapse BraTS 2021 page is archived; the mapping file is in the BraTS 2023 project and needed his sign-in and acceptance of CC BY-NC post-challenge terms; (2) display route is TCIA only, or files proven identical to TCIA's by checksum; Synapse is used for the mapping file only, because its copy is CC BY-NC and altered (ET label 3, renamed cases); (3) compute on the Kaggle copy, verified against TCIA's `.sums` checksum list instead of downloading 8 demo cases by hand; (4) Aspera test moved to Buffer B1. New finding: TCIA's policy adds duties for anyone hosting a copy (link the policy, ask reusers to do the same); this is one of the helpdesk questions. Carried over: send the helpdesk email; Aspera test and checksum comparison (B1). **Weak explain-back answers to revisit:** (1) said we were "grabbing all of that information and storing it": we downloaded only ~400 KB of ID spreadsheets and no scans, on purpose; (2) said the data is "a basis to learn and train from": the same slip as Session 1; we evaluate a pretrained model, we do not train; (3) described the licence risk as data being "only for research and larger places" instead of the real difference, CC BY 4.0 (TCIA) versus CC BY-NC (Synapse); (4) follow-up: could not say why the mapping file is needed (it tells us which cases the model saw in BraTS 2018 training, for the leakage check). Solid: the check-question answer "licence is permission, citation is credit, and we need both"; named licensing as the main risk.
- **Nov 16, 2026, Session 3 (both halves and the explain-back run on Fable 5.2 at Debraj's request).** Done: Kaggle copy identified and written up in `docs/DATA_ACCESS.md` section 8.4: "BRaTS 2021 Task 1 Dataset" by Darien Schettler (`dschettler8845/brats-2021-task1`, dataset ID 1541666, version 1, uploaded 2021-08-19, 13,417,502,720 bytes, three `.tar` archives, licence field "Data files © Original Authors", source the 2021 Synapse page). Counted in a Kaggle notebook: 1,251 cases, 5 files each, TCIA's file names, one junk `.DS_Store`; cases 00495 and 00621 are identical duplicates of copies inside the big archive; case 00118's five file sizes equal TCIA's listed sizes. One case (00495) opened with nibabel 5.4.2: 240 × 240 × 155 voxels of 1 mm, orientation L, P, S, label values 0, 1, 2 and 4 with no 3. Measured size per case (section 5.2 asked for this): 7.9 MB for case 00118, 10.3 MB for case 00495, about 10.7 MB on average. Notebook saved as `notebooks/01_first_look.ipynb`. **Changes from plan, agreed with or asked for by Debraj:** (1) Debraj signed in to Kaggle in Claude's browser pane and Claude ran the notebook while he watched, instead of Debraj typing the cells himself; (2) the repo copy of the notebook keeps the real text outputs but has the scan picture removed, because the Kaggle copy came through the Synapse door and scan images are never committed; Debraj's full download stays outside the project folder; (3) one idea was added that the plan did not expect: the data is packed in `.tar` archives, so a case has to be unpacked to scratch space before it can be opened. **Notes for later:** case 00495 was looked at before the locked test set exists (format check only, nothing tuned); the Kaggle session restarts and loses its memory when the notebook is renamed. **Carried over:** phone-verify the Kaggle account (GPU and internet stay off until then; Half A's first box is unticked for this reason); send the TCIA helpdesk email; Aspera test and checksum comparison (B1). **Explain-back not passed; the box is unticked and it is repeated at the start of Session 4 before any new work.** Weak answers to revisit: (1) described today as "matching the identifier to the photo of the brain" and a way to "upload a photo of a brain and identify where it is in the data set": nothing is uploaded, ever, and the ID matching is Session 4's job; today was identifying and checking the Kaggle copy and opening one case; said himself that it was a guess; (2) "photo" again (third session running): scans are 3D grids of numbers; (3) first read the five panels as five different slices from top to bottom, then corrected himself: they are one slice shown five ways; (4) called T1ce "grayed out" and T2 and FLAIR "another edit": they are four separate scans, T1ce is taken after a contrast dye is injected, T2 and FLAIR make fluid and swelling bright; (5) could not say what label values 0, 1, 2 and 4 mean (not tumor, necrotic core, edema, enhancing tumor); (6) said the tumor is at the "back left": left and right are not verified until Session 18. Solid: worked out unprompted that `seg` shows only the tumor and that its colours stand for different parts of the tumor; saw that the same region shows up differently in each scan; was honest about guessing.
- **Nov 18, 2026, rules change (agreed with Debraj, made during Session 4 Half A, run on Opus 5.5).** At his request, CLAUDE.md "How a session runs" now says: Claude does all the building and runs every command itself, explaining in plain English as it goes; Debraj no longer runs commands, clicks through steps or types mid-session ("He runs commands himself where practical" removed). Steps that truly need him (sign-ins, accepting terms, phone verification, API tokens, sending email, approving a download over 2 GB) are listed together at the start of each session; one that comes up unexpectedly is collected and asked at a natural stopping point. The end-of-session explain-back and the full PI-style checkpoints are unchanged and stay non-negotiable. New CLAUDE.md section "Running Kaggle notebooks": Claude will run Kaggle notebooks with the official Kaggle command-line tool (`kaggle kernels push`, `status`, `output`), planned from the official docs and not yet tested; the one-time phone verification and API token are on the start-of-session list of Buffer B1; the token stays in `C:\Users\debra\.kaggle\`, and `.gitignore` now also blocks `access_token` and `.kaggle/`. `.gitignore` also blocks `exports/` (the private study packs and nightly digests, added Nov 16). Left unchanged on purpose and flagged to Debraj: the tasks that ask for his own words (Session 6 Methods paragraphs; the write-up he drafts himself), because they are about his understanding and authorship, not about running commands.
- **Nov 18, 2026, Session 4 (run on Opus 5.5; one day ahead of the plan's Thu Nov 19).** Started with the repeated Session 3 explain-back: **passed**, with one correction (he described opening a case but missed Session 3's main job, checking the Kaggle copy, and its real risk, that the copy may not be identical to TCIA's files); his follow-up answer was right ("anyone can upload anything to Kaggle and name it anything"). Done: project virtual environment `.venv` with pandas 3.1.1, openpyxl 3.1.5, numpy 2.5.5 (first pip try timed out on the connection; worked with `--timeout 60 --retries 5`); scripts `04_look_at_mapping.py`, `04_count_by_earliest_year.py`, `04_check_repeat_scans.py`, `04_make_case_status.py`; `data_lists/case_status.csv` (1,251 cases: `seen_2018` 285, `in_earlier_year_not_2018` 80, `new_in_2021` 886; 1,133 patients, 768 of them in the unseen pool) and `data_lists/README.md`. Findings: the mapping file holds exactly the 1,251 training cases plus 4 BraTS 2020 IvyGAP cases not in 2021; 285 cases in 2018 matches the model's 285 training cases; no case skips a year; no empty year cells. **Correction to an earlier record:** Session 2 recorded the mapping file as 2,040 case rows; it has 1,255 data rows (Session 2 counted Excel's formatted area); fixed in `docs/DATA_ACCESS.md` 8.3, file fingerprint unchanged. **Plan changes agreed with Debraj:** (1) 118 patients have two scans (BraTS 2023 names end `-000` and `-001`; the official BraTS 2023 submission page defines the 5 digits as the case ID and the 3 as the timepoint); `case_status.csv` gets a `patient_id` column and the status is decided per patient (any scan in 2017–2020 marks all of that patient's scans); Debraj asked for a Local ID and Site No check first: Site No and Cohort match for all 118 pairs, but Local ID is `N/A` for every private case, so it could not confirm the pairing; the evidence is the official naming rule; (2) the patient rule removed **0** cases from the unseen pool (all 236 two-scan cases are new in 2021); (3) Session 5 splits by patient, keeping both scans of a person on the same side. Carried over: send the TCIA helpdesk email; Kaggle phone verification and API token (start of B1); Aspera test and checksum comparison (B1). **Explain-back passed.** Weak point to revisit at Checkpoint 1: on why the `patient_id` column matters when it changed nothing, he said it is proof the check ran (a fair second reason); the main reason is the Session 5 split, so one person cannot be in both the locked test set and the development pool or be counted twice. Solid: the three statuses and why leakage fakes good results; named a real risk (a wrong mapping file); the four scan types and the label values 0, 1, 2, 4 all correct at the start of the session; "photo" slip gone.
- **Nov 18, 2026, after Session 4 (two updates from Debraj).** (1) **TCIA helpdesk email sent** by Debraj on Nov 18, 2026, from his university email account, with small edits to the draft ("converted to 8-bit" wording; numbered questions). Recorded in `docs/DATA_ACCESS.md` section 10 and `docs/TCIA_HELPDESK_EMAIL.md`. **Waiting on TCIA's reply** (open items U4, U6, U7); site launch waits on it, the build does not. (2) **Kaggle API token** saved by Debraj at `C:\Users\debra\.kaggle\access_token` (outside the repo; never printed). Claude installed the Kaggle command-line tool in `.venv` (`kaggle` 2.2.5, plus `six` 1.17.0, which kaggle needs but did not install itself) and confirmed the login with two read-only commands: the dataset's three archives are listed at the recorded sizes, and `kernels list --mine` shows the Session 3 notebook under Debraj's account. The first box of Buffer B1 is ticked early. Still carried over: Kaggle phone verification (GPU and internet stay off until then); Aspera test and checksum comparison (B1).
- **Nov 19, 2026, Session 5 (run on Opus 5.5; one day ahead of the plan's Fri Nov 20).** **Updates first, from Debraj:** (1) Kaggle phone verification done by him, confirmed today; Session 3 Half A's first box ticked, B1 start list and CLAUDE.md updated; no GPU run done (Session 7 is the first). (2) TCIA replied (Tracy Nolan, TCIA Support Team, ticket TH-60610); reply and Debraj's follow-up recorded word for word in `docs/DATA_ACCESS.md` 10.1 and 10.2. U7 closed (cite each case's source collection from TCIA's mapping table, plus the BraTS papers); U4 and U5 note that Aspera checksums "have occasionally been unreliable"; U6 still open (not answered; his follow-up asks again); new U15 (cases with no TCIA source collection to cite). **TCIA said the first email read as AI-written. From now on Debraj writes all outside emails himself; Claude only checks the facts** (added to CLAUDE.md). **Plan changes agreed with Debraj today:** (a) the 8 demo cases are downloaded straight from the TCIA package and only those files are displayed; Kaggle is for compute only; each of the 8 is compared value by value with its Kaggle copy (Session 14); (b) the Kaggle-vs-TCIA checksum comparison (B1) becomes a secondary check and U4/U5 no longer block launch; the 3D Slicer check by eye (Session 14) is the main check; Limitations note added to `docs/METHODS_NOTES.md`: the full evaluation runs on the Kaggle copy and only the 8 demo cases are compared with TCIA's files; (c) Debraj emails UTM Library's copyright office himself this week (U16); Session 21 creates the data repo only if the reply raises no objection (an explicit yes is not needed); no reply by Session 21 does not count as no objection, so the placeholder fallback is used until a reply comes; if no reply a week after sending, he sends one follow-up himself; (d) the Kaggle copy is credited as compute data (`docs/DATA_ACCESS.md` 3.5); (e) the outside "BraTS 2018 TCGA lists" step was replaced: TCIA's table already showed every TCGA case is `seen_2018` and no unseen case is TCGA, so such a list could only re-confirm excluded cases; instead the 285 seen cases were counted by source and had to come to 285 (they did: 30 `2013` = Collection 4, 167 `TCIA..` = TCGA-GBM 102 + TCGA-LGG 65, 88 `CBICA` = UPENN-GBM 86 + UPENN-GBM_Additional 2). **Done:** `scripts/05_add_source.py` (source and `source_in_tcia` columns added to `case_status.csv`; check B: 0 contradictions; 351 not-in-TCIA cases all match `NotPreviouslyInTCIA.csv`; Site ID disagrees for one case, 01162, 24 vs 23, no effect); `scripts/05_spot_check.py` (5 cases by rule, all agree); `scripts/05_make_split.py` (by patient, stratified by institution and scan count, seed 20261119, reproducible byte for byte): `locked_test.csv` 399 cases / 346 patients, `dev_pool.csv` 487 / 422, `seen_sanity.csv` 20; frozen in commit `93f180b`, pushed before any inference, hash and fingerprints in `docs/METHODS_NOTES.md`. Case 00495 (opened in Session 3 for the file format only) landed in the locked test set and was left there. Carried over: Aspera test and secondary checksum comparison (B1); U6 and U16 replies. **Explain-back passed.** Corrections: (1) Git does not lock the lists, it makes any later change visible; (2) for the baseline scores the main leak is a 2018 training patient in the test set (checks A and B); a patient split across test and dev matters for the fine-tuning stretch goal (the per-patient split). Follow-up asked, answer to record at the start of Session 6: why shuffle within each institution instead of all 768 patients together? Solid: the order (cross-check, split, commit before any model run) and naming a leaky split as the risk.
