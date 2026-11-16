# Project Brief: 3D Brain Tumor Viewer with AI Segmentation

Prepared Nov 16, 2026 from a requirements interview. This is the input for the planning stage (Claude Fable). The plan should follow this brief, and any place where the brief seems wrong or unrealistic should be flagged instead of silently changed.

## One-line pitch

A free, open-source website where anyone can open real 3D brain MRI scans, see an AI's outline of the tumor overlaid in 3D, rotate it and peel through the slices, and compare the AI's outline to an expert's outline, with honest, research-grade accuracy metrics.

## Who it's for

1. **Research PIs** (main use in January): proof that I can be useful in an imaging, neuro or computational lab. It goes with cold emails to 5–10 UofT labs asking about summer positions.
2. **Med school admissions** (Temerty and others): a project I can describe and defend in an interview.
3. **Industry recruiters** (backup path is biotech/medtech sales): shows technical fluency.

## About me (the builder)

- First-year Life Sciences at UTM. My goal is trauma surgery.
- Coding: light Java from a Grade 11 intro course. I will rely heavily on Claude to write code and will cross-check with Codex and Gemini.
- **I must be able to explain everything I built.** "Learn as I build" is a requirement:
  - Plain-English comments in every file.
  - An explain-back checkpoint after each stage: I explain what was built and why, and Claude questions me the way an interviewer or PI would.

## Hard constraints

| Constraint | Value |
|---|---|
| Time | 2–4 hours/week, around December exams and a winter-break trip to Thailand |
| Deadline | Show-ready v1 by January 2027 |
| Budget | Up to about $50 total (domain name, a month of Colab Pro if truly needed) |
| Hardware | HP laptop, Windows 11, i5-1135G7, 8 GB RAM, **no GPU**. All model work runs on free cloud GPUs (Google Colab / Kaggle) |
| Scan input | **Curated demo cases only** in v1 (no user uploads). No real patient data from anyone |
| Framing | Prominent "research and education only, not for diagnosis" messaging |
| Code | Public open-source GitHub repo with a clear README |
| Design | Must look polished, like a real product, not a class assignment |

## v1 scope (January)

**Model:** start from a pretrained model and evaluate it honestly. Don't train from scratch in v1.
- Candidate: MONAI Model Zoo `brats_mri_segmentation` (SegResNet, Myronenko 2018). It was trained on BraTS 2018, takes 4 MRI channels (T1c, T1, T2, FLAIR) and outputs 3 nested regions: whole tumor (WT), tumor core (TC) and enhancing tumor (ET). The reported validation Dice is about 0.90 WT, 0.86 TC and 0.79 ET. **Verify these numbers yourself.**

**Data:** BraTS 2021 segmentation data from TCIA, listed as CC BY 4.0. Confirm the license and the attribution requirements before displaying any case publicly.

**Rigor requirement (important):** BraTS 2021 includes cases from earlier BraTS years. If the pretrained model saw a case during training, evaluating on that case is data leakage. The plan must use the BraTS-to-TCIA ID crosswalk (or equivalent) to evaluate **only on cases the model never trained on**, and must state how this was checked.

**Metrics:** Dice and HD95 per region (WT/TC/ET), reported as mean ± SD across the held-out set, plus at least 2 shown failure cases with an honest explanation.

**Website features:**
- 5–10 curated cases, segmentations computed in advance (static hosting, no inference server).
- 3D rendering of the brain and the tumor, which you can rotate and zoom.
- Slice "peeling" through axial, coronal and sagittal planes.
- Toggles for each tumor sub-region (WT/TC/ET) with plain-language explanations.
- **AI vs expert comparison**: switch between or overlay the AI outline and the ground-truth outline, with that case's Dice shown.
- A "Results & Methods" page: dataset, model, leakage check, metrics, limitations, citations.
- An "About" page: who built it, why, and what was AI-assisted.
- A not-for-diagnosis disclaimer that is visible without scrolling.

**Nice-to-have (not required):** usable on a phone.

**UI pattern to borrow** (from the "3D CT anatomy explorer" reel in my research export): the 3D view and the three slice views stay in sync. Clicking a region highlights it in every view, and scrolling one view moves the others. Get the left-right orientation right, because radiology convention shows the patient's left on the screen's right. That reel's build got this wrong at first.

**Tooling to consider** (from my research export): 3D Slicer (free desktop app) to check segmentations slice by slice before they go on the site; nibabel/SimpleITK for reading NIfTI files; nnU-Net as the strongest out-of-the-box BraTS baseline, kept as the benchmark to compare against later rather than built in v1.

## Deliverables by January

1. Live website link (free static hosting; a custom domain is optional within budget).
2. Public GitHub repo with a README covering setup, methods, results, license and attribution.
3. A notebook (Colab) that reproduces the inference and metrics end-to-end.
3b. A 1–2 page write-up: clinical motivation, dataset and license, method in plain language, results, failure cases, limitations, next steps, and what building it taught me about reading brain MRI. Use modest wording ("a model that achieved X on a public dataset"), never "an AI that diagnoses".
4. A final **Fable review session** before anything goes public: a critical review of the whole project, checking that the evaluation cases were truly held out, the metrics are correct, left and right orientation is correct, and the write-up doesn't overclaim.
4b. Review by a UTM prof or TA I know **before** the cold emails go out.
5. Cold emails to 5–10 UofT labs.

## Later versions (not in January scope, but the design should leave room for them)

- **v2:** fine-tune or train my own model on BraTS 2021 in Colab and compare it head-to-head with the pretrained baseline (a real "what I did" result). One way to frame it is the "reproduce a research paper" workflow: reproduce the Myronenko 2018 SegResNet results, then extend them.
- **Optional warm-up before or alongside v2:** a one-afternoon MedMNIST training loop, to learn what training actually involves on a tiny dataset.
- **v3 (trauma angle):** a module for head-trauma bleeds (intracranial hemorrhage) on CT, using the same viewer. This connects the project to my trauma-surgery goal. Dataset and license still to be researched.

## Questions the plan must answer

1. Which browser 3D/medical viewer to use (e.g. NiiVue, vtk.js, three.js), judged on 3D overlay support, mobile performance and how easy the code is for a beginner to understand.
2. How large the volumes are, and how to compress and host them on free static hosting.
3. Whether pretrained inference fits on a free Colab GPU, and what the fallback is if it doesn't.
4. How to select cases: which ones count as truly held out, and which 5–10 make the best demos.
5. A week-by-week schedule of roughly 3-hour sessions from now to January, with a realistic note on the December exam period and the trip. Each session ends in something that works.
6. The biggest risks and the cut list: what gets dropped first if time runs short.
7. Where the explain-back checkpoints go, and what I should be able to explain at each one.
8. What should be written in CLAUDE.md for the build sessions.
9. Data access: my research export says BraTS requires Synapse registration and a data-use agreement, but TCIA lists the BraTS 2021 segmentation data as CC BY 4.0. Work out which route to use and what that route allows me to display publicly.

## Cold-email approach (January)

From my research export: find labs with active funding and recent papers, email the grad students and postdocs as well as the PI, mention one specific method or figure from their latest paper, say concretely what I can help with (imaging, coding, data work), and link the live site and attach a one-page CV.

## Suggested prompt for the planning session

> Read PROJECT_BRIEF.md. Before planning, ask me any clarifying questions you still have. Then produce a detailed implementation plan that answers every item under "Questions the plan must answer", verifies the factual claims in the brief (model, Dice numbers, license, leakage), and is broken into ~3-hour sessions a beginner can follow with Claude Code. Flag anything in the brief you think is unrealistic.

## Workflow and files the planning session must produce

- **Model split:** planning and the final review run on Fable 5.2. Build sessions run on Opus 5.5, switching to Fable only when stuck on something hard.
- **PLAN.md:** numbered sessions with a checkbox per task, so each build session can start with "Do session N from PLAN.md" and tick off what's done at the end. Include an explain-back checkpoint at the end of each session and the final Fable review session.
- **CLAUDE.md:** standing rules for every build session: who I am and my coding level, plain-English comments in every file, run the explain-back checkpoint before ending a session, update PLAN.md checkboxes, research/education-only framing, never commit patient data or large scan files to Git, and the model split above.
- My setup (already installed and working): Windows 11, Git 2.56, Node 26 LTS, Python 3.12.10, GitHub account, and Synapse, Kaggle and Google Colab accounts. The project folder is on OneDrive, so large scan files should not be stored inside it.
