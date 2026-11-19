# CLAUDE.md: standing rules for every build session

Read this file and the current session in PLAN.md before doing anything. PROJECT_BRIEF.md is the original brief; where PLAN.md differs from it, PLAN.md wins (section 4 of PLAN.md explains each difference).

## Who you are working with

- Debraj Karmaker, first-year Life Sciences student at UTM, aiming for trauma surgery.
- Coding level: light Java from a Grade 11 intro course. No Python, JavaScript, Git or machine-learning background. Assume nothing; explain everything once, plainly.
- He must be able to explain every part of this project without notes, to a research PI or a med-school interviewer. **His understanding matters more than speed.** Priority order when they conflict: 1. rigor, 2. his understanding, 3. polish.
- He may cross-check your work with Codex and Gemini. Write code and explanations that hold up to that.

## How a session runs

Sessions are 1 hour, split into two 30-minute halves (he works around Fajr). Each half must end at a natural stopping point with nothing left broken.

**Who does what (changed Nov 18, 2026, at his request).** Claude does all the building and runs every command itself: scripts, installs, Git, Kaggle runs, file edits. He follows along and learns; he does not run commands, click through steps or type anything mid-session. The only things he does himself are steps that truly need him: signing in to an account, accepting terms, phone verification, creating an API token, sending an email, or approving a download over about 2 GB.

**Outside emails (from Nov 19, 2026, at his request).** He writes every email to people outside the project (TCIA, the university, reviewers, labs) himself, in his own words. Claude does not draft them; Claude only checks the facts in his draft (IDs, numbers, licence names, what the project actually does). Reason: TCIA said the first, Claude-drafted email read as AI-written.

1. **Start.** He says "Do session N from PLAN.md". Read that session. Restate its goal in two sentences and say what will exist at the end. Check the Session log for anything carried over. Then give him **one list of every step only he can do this session**, all together, so he does them in one go before the building starts. If there are none, say so.
2. **Explain as you go.** Before each step, say in plain English what it will do and why; after it, say what the output means. Introduce at most two or three new ideas per half. Use an everyday analogy when one helps. Do not stop to make him do things.
3. **Small steps.** Write a little, run it, look at the output, explain it. Do not produce a large file in one go. If a step that truly needs him comes up unexpectedly, collect it and ask at the next natural stopping point, not in the middle of a step. Decisions that are his to make (a change to PLAN.md, for example) are also collected for that stopping point.
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
- **Before any step that downloads more than about 2 GB to the laptop, stop and say so**, with the size, and wait for his go-ahead. If it can be foreseen, put it on the start-of-session list instead.
- Never put Kaggle or Synapse tokens in code, notebooks, commits, logs or exports. Use the platform's secrets feature. The Kaggle API token lives only in `C:\Users\debra\.kaggle\`, outside the project folder; never copy it anywhere else or print it.
- Attribution follows `docs/DATA_ACCESS.md` exactly (TCIA dataset DOI, the BraTS papers, the source-dataset citations).

## Environment

- Windows 11, PowerShell. Git 2.56, Node 26 LTS, Python 3.12.10. HP laptop, i5-1135G7, 8 GB RAM, no GPU.
- The project folder path contains spaces; quote paths in commands.
- Accounts already set up: GitHub, Kaggle, Google Colab, Synapse.
- Budget: about $50 total. Do not suggest paid services unless a free route has failed.
- Python libraries live in the project's own virtual environment, `.venv` (ignored by Git). Run Python as `.\.venv\Scripts\python.exe`, not plain `python`. Installed Nov 18, 2026: pandas 3.1.1, openpyxl 3.1.5, numpy 2.5.5. pip downloads on this connection can stall; use `--timeout 60 --retries 5`.

## Running Kaggle notebooks (planned Nov 18, 2026; login tested, runs not tested yet)

Status Nov 18, 2026: the CLI is installed in `.venv` (`kaggle` 2.2.5, plus `six` 1.17.0, which kaggle 2.2.5 imports but does not install by itself) and logs in with the token in `C:\Users\debra\.kaggle\access_token`: `kaggle datasets files dschettler8845/brats-2021-task1` and `kaggle kernels list --mine` both work. Not yet tested: `kernels push`, `status` and `output`. Phone verification: done by him, confirmed Nov 19, 2026, so GPU and internet should now be available in notebooks. Not tested with a run yet, on purpose: Session 7 is the first GPU run.

Claude runs Kaggle notebooks from the laptop with the official Kaggle command-line tool, so he never has to click around Kaggle. Source: the official docs at https://github.com/Kaggle/kaggle-cli (README, docs/README.md, docs/kernels.md, docs/kernels_metadata.md), read Nov 18, 2026, when the main branch was version 2.2.5. Check them again before the first run.

- **Install:** the `kaggle` package, into `.venv` (it needs Python 3.11 or newer). Record the version installed.
- **One-time steps only he can do** (go on the start-of-session list of the first session that needs Kaggle): phone-verify the Kaggle account (Kaggle keeps GPU and internet switched off in notebooks until then), and create an API token at https://www.kaggle.com/settings/api ("Generate New Token"). Either Claude runs `kaggle auth login` and he approves it in the browser, or the token is saved as `C:\Users\debra\.kaggle\access_token`. Never in the project folder.
- **A run is a folder** holding the notebook (`.ipynb`) or script (`.py`) and a `kernel-metadata.json` file: `id` `debrajkarmaker/<slug>`, `title`, `code_file`, `language` `python`, `kernel_type` `notebook` or `script`, `is_private` `true`, `enable_gpu` (only when the step needs a GPU), `enable_internet` (only when it must download something), `machine_shape` (for example `NvidiaTeslaT4` for GPU T4 ×2), and `dataset_sources` `["dschettler8845/brats-2021-task1"]`.
- **Commands:** `kaggle kernels push -p <folder>` uploads and runs it (a full, non-interactive run); `kaggle kernels status debrajkarmaker/<slug>` says whether it is running, finished or failed; `kaggle kernels output debrajkarmaker/<slug> -p <folder>` downloads the files it wrote.
- **Where the data is inside a run:** `/kaggle/input/datasets/dschettler8845/brats-2021-task1/` (seen in Session 3; the docs do not state it, so the notebook lists `/kaggle/input` first).
- Downloaded outputs that contain scan pictures or scan data go to `C:\BrainTumorData`, never the project folder. Only ID lists, tables and code come into the repo.
- Fallback if the command-line route fails: he signs in to Kaggle in Claude's browser pane and Claude drives the notebook there (as in Session 3).

## Commands

Kept current. Only commands that have actually been run in this project are listed. Still to come: running the site locally, building it, deploying it, running the tests, and running the web-data script (added in the sessions that create them).

Claude runs these. They are listed so he can see what each one does, and repeat one if he ever wants to. Every command runs from the project folder; a new PowerShell window starts in `C:\Users\debra`, which is the wrong place.

```powershell
# Go to the project folder (quotes needed because the path has spaces).
cd "C:\Users\debra\Projects\Brain Tumor Viewer"

# See what has changed since the last commit.
git status

# Save a snapshot: stage every change, then commit with a message.
git add .
git commit -m "Describe what changed"

# Send new commits to GitHub.
git push

# Check which GitHub account this laptop is signed in to.
gh auth status

# Run a project script with the project's own Python (first used in Session 4).
.\.venv\Scripts\python.exe scripts\04_look_at_mapping.py

# Rebuild data_lists\case_status.csv from the mapping file (Session 4). Do not re-run once results exist.
.\.venv\Scripts\python.exe scripts\04_make_case_status.py

# Check the Kaggle command-line tool can log in (read-only; never print the token).
.\.venv\Scripts\kaggle.exe datasets files dschettler8845/brats-2021-task1
.\.venv\Scripts\kaggle.exe kernels list --mine
```

One-time setup, run in Session 4 (Nov 18, 2026), not needed again:

```powershell
python -m venv .venv             # create the project's private Python toolbox
.\.venv\Scripts\python.exe -m pip install --timeout 60 --retries 5 pandas openpyxl
.\.venv\Scripts\python.exe -m pip install --timeout 60 --retries 5 kaggle six   # Kaggle command-line tool (Nov 18)
```

One-time setup, run in Session 1 (Nov 16, 2026), not needed again:

```powershell
git init -b main                 # start tracking this folder, main line named "main"
winget install GitHub.cli        # install GitHub's command-line tool (gh 2.104.0)
gh auth login --hostname github.com --git-protocol https --web   # sign in through the browser
gh repo create brain-tumor-viewer --public --description "Research and education project: view brain MRI cases with an AI tumor outline. Not for diagnosis." --source . --remote origin --push
```

- Repo: https://github.com/Dbrjkrm/brain-tumor-viewer (remote name `origin`, branch `main`).
- If a new terminal says `gh` is not recognised, close and reopen it, or use the full path `& "C:\Program Files\GitHub CLI\gh.exe"`.

## Model split

- Build sessions run on Opus 5.5.
- Planning, the main review (Sessions 32–34) and the final check (Session 51) run on Fable 5.2.
- Switch a build session to Fable only when stuck on something hard, and switch back afterwards.
