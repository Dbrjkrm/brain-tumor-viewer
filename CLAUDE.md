# CLAUDE.md: standing rules for every build session

Read this file and the current session in PLAN.md before doing anything. PROJECT_BRIEF.md is the original brief; where PLAN.md differs from it, PLAN.md wins (section 4 of PLAN.md explains each difference).

## Who you are working with

- Debraj Karmaker, first-year Life Sciences student at UTM, aiming for trauma surgery.
- Coding level: light Java from a Grade 11 intro course. No Python, JavaScript, Git or machine-learning background. Assume nothing; explain everything once, plainly.
- He must be able to explain every part of this project without notes, to a research PI or a med-school interviewer. **His understanding matters more than speed.** Priority order when they conflict: 1. rigor, 2. his understanding, 3. polish.
- He may cross-check your work with Codex and Gemini. Write code and explanations that hold up to that.

## How a session runs

Sessions are 1 hour, split into two 30-minute halves (he works around Fajr). Each half must end at a natural stopping point with nothing left broken.

1. **Start.** He says "Do session N from PLAN.md". Read that session. Restate its goal in two sentences and say what will exist at the end. Check the Session log for anything carried over.
2. **Teach before typing.** Before writing code, explain in plain English what it will do and why. Introduce at most two or three new ideas per half. Use an everyday analogy when one helps.
3. **Small steps.** Write a little, run it, look at the output together. Do not produce a large file in one go. He runs commands himself where practical.
4. **End of Half A.** Stop cleanly. Say in one line where things stand.
5. **End of session, always, before anything else:**
   - Run the explain-back: ask him to "explain today in three sentences" (what we built, why, one thing that could go wrong). Correct gently, then ask one follow-up question.
   - On a FULL CHECKPOINT session, play a PI: ask the listed questions plus follow-ups, one at a time, and wait for his answer. Do not answer for him. Afterwards say plainly which answers were solid and which need work.
   - Tick the finished boxes in PLAN.md. Leave unfinished ones unticked.
   - Add one line to the Session log in PLAN.md, including any weak explain-back answers.
   - Commit with a clear message and push.

If time runs out, stop the building early enough to do the explain-back. A session without an explain-back is not done.

Do not run ahead into later sessions, and do not add features that are not in PLAN.md. If something in PLAN.md turns out to be wrong, say so, propose the change, and record it in the Session log once he agrees.

## Code rules

- **Plain-English comments in every file.** A short header at the top saying what the file is for and how it fits the project, and a comment on every block saying what it does and why. Write for someone who has never seen the language.
- Prefer the simplest code that works over clever code. Descriptive names. No abstractions he has not been taught.
- Stack: Python (nibabel, MONAI, pandas, numpy) for data and evaluation; plain JavaScript with Vite and NiiVue for the site. No React or other framework. No new dependency without explaining why it is needed.
- NiiVue and MONAI change between versions. Check their current documentation before using an API; do not rely on memory. Record the versions used.
- Every number shown on the site or in the write-up is generated from files in `results/`. Never hand-type a result.

## Rigor rules (not negotiable)

- The lists in `data_lists/` (locked test set, development pool, seen-sanity cases) are frozen once committed. Never edit them after results exist. If a mistake is found in them, stop and discuss; any change is documented publicly on the Methods page.
- The locked test set is never used to tune, choose or adjust anything. For the fine-tuning stretch goal it is used exactly once, for the final comparison.
- `docs/METRIC_RULES.md` is written before results and followed exactly.
- Never invent, estimate or round a result to look better. If a number cannot be reproduced, say so.
- Report failures and limitations plainly. If something looks too good, treat it as a possible bug first.
- Left and right: the viewer uses radiological convention (patient's left on screen right) and must match 3D Slicer. Any change touching orientation gets re-checked against `docs/ORIENTATION.md`.

## Framing and wording

- This is a research and education project. **Not for diagnosis.** That statement stays visible without scrolling on every page.
- Modest wording only: "a pretrained model that achieved X on N held-out cases from a public dataset". Never "an AI that diagnoses", "clinical-grade", "accurate enough for", or similar.
- Say "expert-approved reference outline", not "ground truth drawn by an expert", unless Session 2 found the paper supports stronger wording.
- He did not train the baseline model. Say so wherever the model is described.

## Identity and branding

- Author: Debraj Karmaker (full name) on the About page, README and repo.
- Project name: "Brain Tumor Viewer". Repo: `brain-tumor-viewer`. Data repo: `brain-tumor-viewer-data`.
- No "UTM" or "University of Toronto" in the project name or branding. The About page may say he is a first-year Life Sciences student at UTM, with a clear note that this is an independent personal project, not affiliated with or endorsed by the university.
- The About page states honestly what was AI-assisted.

## Data rules

- **Never commit scan files to this repo.** No `.nii`, `.nii.gz`, DICOM or model weights. `.gitignore` must block them. ID lists, metrics tables and figures are fine.
- The only scan files that are ever published are the 8 curated, web-compressed demo cases, and they go in the separate `brain-tumor-viewer-data` repo with full attribution. Nothing goes there until the licence route in `docs/DATA_ACCESS.md` is confirmed.
- No real patient data from any other source, ever. No user uploads in v1.
- The full dataset and all heavy compute stay in the cloud (Kaggle first, Colab second). The laptop has 8 GB RAM and no GPU.
- Local scan files live in `C:\BrainTumorData`, never in the project folder.
- **Before any step that downloads more than about 2 GB to the laptop, stop and say so**, with the size, and wait for his go-ahead.
- Never put Kaggle or Synapse tokens in code, notebooks or commits. Use the platform's secrets feature.
- Attribution follows `docs/DATA_ACCESS.md` exactly (TCIA dataset DOI, the BraTS papers, the source-dataset citations).

## Environment

- Windows 11, PowerShell. Git 2.56, Node 26 LTS, Python 3.12.10. HP laptop, i5-1135G7, 8 GB RAM, no GPU.
- The project folder path contains spaces; quote paths in commands.
- Accounts already set up: GitHub, Kaggle, Google Colab, Synapse.
- Budget: about $50 total. Do not suggest paid services unless a free route has failed.

## Commands

(Filled in during Session 1 and kept current: how to run the site locally, build it, deploy it, run the tests, and run the web-data script.)

## Model split

- Build sessions run on Opus 5.5.
- Planning, the main review (Sessions 32–34) and the final check (Session 51) run on Fable 5.2.
- Switch a build session to Fable only when stuck on something hard, and switch back afterwards.
