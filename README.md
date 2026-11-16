# Brain Tumor Viewer

> **Research and education only. Not for diagnosis.** Nothing in this project is medical advice, and it must not be used to make decisions about any person's care.

**Status: under construction.** The project started on November 16, 2026. There is no website and there are no results yet.

## What this will be

A free, open-source website where anyone can open a small set of real, public, de-identified brain MRI cases, see a pretrained AI model's outline of the tumor in slices and in 3D, and compare it with the expert-approved reference outline.

The model will be evaluated on cases it has never seen, and the results will be reported honestly, including the cases where it fails.

## What this is not

- It is not a diagnostic tool and has no clinical use.
- I did not train the model. It is a publicly available pretrained model (the MONAI `brats_mri_segmentation` bundle). My work is checking which cases the model has not seen, evaluating it on them, and building the viewer.

## Where things are

- [PLAN.md](PLAN.md): the session-by-session plan and the session log.
- [PROJECT_BRIEF.md](PROJECT_BRIEF.md): the original brief.
- [CLAUDE.md](CLAUDE.md): the standing rules for the AI-assisted build sessions.

## Data

This repository contains **no scan files**. The scans come from the public BraTS 2021 dataset. Full licence details and the required citations will be added in `docs/DATA_ACCESS.md` before any scan is shown.

## Licence

The code in this repository is under the [MIT License](LICENSE). That licence covers the code only, not the scans, which keep their own licence.

## Author

Debraj Karmaker. This is an independent personal project, built with AI assistance (Claude). The About page of the finished site will say exactly what was AI-assisted.
