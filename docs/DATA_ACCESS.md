# Data access: where the scans come from and what we may do with them

**What this file is for.** It records, with exact wording and links, the licence and rules that cover the brain scans this project uses, the route the data takes from its source to the website, and everything that is still unconfirmed. Every attribution on the site, the README and the data repo must follow this file exactly.

**How it fits the project.** Nothing may be published in the `brain-tumor-viewer-data` repo until the open items in section 9 that are marked "blocks publishing" are closed.

**Last checked:** Nov 16, 2026 (Session 2). Every source in this file was read on that date. Web pages change, so re-check before launch (Session 33). Section 8.4 (the Kaggle copy) was added later the same day, in Session 3.

**How to read the status labels.**

- **CONFIRMED** means we read it ourselves at the primary source on the date above.
- **UNCONFIRMED** means we have not been able to check it yet. Section 9 lists every such item.
- **OUR READING** means it is our interpretation, not a statement made by the source.

Quotes are copied exactly from the source, including their spelling.

---

## 1. The route in plain words

The same BraTS 2021 scans can be obtained through three "doors". Each door has its own terms, and the terms that apply to a copy are the terms of the door it came through.

| Door | What it is | Licence or terms | What we use it for |
|---|---|---|---|
| TCIA (The Cancer Imaging Archive) | The public archive run for the US National Cancer Institute | CC BY 4.0 | **The licence we rely on for showing scans publicly** |
| Synapse (Sage Bionetworks) | The platform that ran the BraTS challenge | CC BY-NC (non-commercial), accepted by clicking through with an account | One small spreadsheet only (the ID mapping file). Never for scans we display |
| Kaggle | A cloud notebook platform where another user has uploaded a copy of the BraTS 2021 training data (section 8.4) | Kaggle licence field: "Data files © Original Authors", which is not an open licence. The page repeats the 2021 Synapse challenge conditions. It never mentions TCIA's CC BY 4.0 | Where the model runs, because the laptop cannot hold the data. Never the licence basis for anything shown |

The route, agreed by Debraj on Nov 16, 2026:

1. **Display.** The only scan files that ever go on the website are TCIA's files, or files proven identical to TCIA's by checksum. A checksum is a short fingerprint computed from a file's contents: two files with the same fingerprint are the same file.
2. **Compute.** The model runs in the cloud on the Kaggle-hosted copy. That copy must be shown to match TCIA's files using TCIA's own checksum list (section 8.2) before any case from it is displayed.
3. **Synapse** is used only to get the file that maps BraTS 2021 case IDs to earlier BraTS years, which the leakage check needs.
4. **The 8 demo cases** are converted to 8-bit and compressed for the web. That is a change to the original files, and CC BY 4.0 requires us to say so (section 2.2).

---

## 2. The licence we rely on: CC BY 4.0, as released by TCIA

### 2.1 What TCIA says (CONFIRMED)

Source: TCIA collection page "RSNA-ASNR-MICCAI-BraTS-2021", Version 1, updated 2023/08/25.
https://www.cancerimagingarchive.net/analysis-result/rsna-asnr-miccai-brats-2021/

- The Data Access table lists the package "Challenge data both tasks" (Segmentation and MR, DICOM and NIfTI, 142 GB, 1,480 subjects, 7,131 series, 407,245 images) with the licence **"CC BY 4.0"**. The ID crosswalk spreadsheet is listed with the same licence.
- The package includes the label files. The page says the group "provides brain-extracted Segmentation task BraTS 2021 challenge TRAINING and VALIDATION set data in NIfTI that do not pose DUA-level risk of potential facial reidentification, and segmentations to go with them."
  - "Brain-extracted" means the skull and face have been removed from the images, so a face cannot be rebuilt from them. "DUA" means data use agreement.
- On where the scans came from, the page says they are "a collection of data from existing TCIA collections, but also cases provided by individual institutions and willing to share with a cc-by license."
- The segmentation-task NIfTI part is much smaller than the whole package: "Segmentation task nifti: Number of Images  7,131 (Seg) , Images Size (GB)12 (Seg)".
- The page carries a note dated April 2026 saying that updates to the source data manifests do not affect the challenge downloads.

### 2.2 What CC BY 4.0 allows and requires (CONFIRMED from the deed)

Source: Creative Commons, "Attribution 4.0 International" deed.
https://creativecommons.org/licenses/by/4.0/

The deed is Creative Commons' own plain-language summary. It says of itself that it "is not a license and has no legal value". The binding text is the legal code at https://creativecommons.org/licenses/by/4.0/legalcode (not read in full; see section 9).

Allowed:

- "Share — copy and redistribute the material in any medium or format for any purpose, even commercially."
- "Adapt — remix, transform, and build upon the material for any purpose, even commercially."

Required in return:

- "Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use."
- "No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits."

A limit the deed states plainly: "The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material."

What this means for us (OUR READING):

- We may host the 8 demo cases publicly and may convert them for the web.
- We must give credit (section 3), link to the licence, and state that the files were changed (converted to 8-bit, compressed, and combined with a model's output).
- We must not word anything so that it looks as if TCIA, the BraTS organisers or the hospitals endorse this project.
- We must not add restrictions of our own to the demo files. The data repo therefore carries CC BY 4.0, not a stricter licence.

---

## 3. What we owe: the exact attribution

Source for all of section 3: the "Citations & Data Usage Policy" and "Related Publications" parts of the TCIA collection page (link in 2.1). CONFIRMED.

The page says: "Data Citation Required: Users must abide by the TCIA Data Usage Policy and Restrictions. Attribution must include the following citation, including the Digital Object Identifier".

### 3.1 The data citation (required, with DOI)

> Baid, U., Ghodasara, S., Mohan, S., Bilello, M., Calabrese, E., Colak, E., Farahani, K., Kalpathy-Cramer, J., Kitamura, F. C., Pati, S., Prevedello, L., Rudie, J., Sako, C., Shinohara, R., Bergquist, T., Chai, R., Eddy, J., Elliott, J., Reade, W., Schaffter, T., Yu, T., Zheng, J., Davatzikos, C., Mongan, J., Hess, C., Cha, S., Villanueva-Meyer, J., Freymann, J. B., Kirby, J. S., Wiestler, B., Crivellaro, P., Colen, R. R., Kotrotsou, A., Marcus, D., Milchenko, M., Nazeri, A., Fathallah-Shaykh, H., Wiest, R., Jakab, A., Weber, M-A., Mahajan, A., Menze, B., Flanders, A E., Bakas, S., (2023) RSNA-ASNR-MICCAI-BraTS-2021 Dataset. The Cancer Imaging Archive DOI: 10.7937/jc8x-9874

DOI link: https://doi.org/10.7937/jc8x-9874

### 3.2 The acknowledgement sentence (required)

> "The results <published or shown> here are in whole or part based upon data generated by the TCGA Research Network: http://cancergenome.nih.gov/."

We choose one of "published" or "shown" when we use it. TCGA is The Cancer Genome Atlas, the source of two of the collections.

### 3.3 The three papers

The page says: "You are free to use and/or refer to the BraTS datasets in your own research. In addition, please be specific and also cite the 6 datasets that were part of this Challenge."

1. Baid, U., et al. (2021). The RSNA-ASNR-MICCAI BraTS 2021 Benchmark on Brain Tumor Segmentation and Radiogenomic Classification (Version 2). arXiv. DOI: 10.48550/arXiv.2107.02314
   - The TCIA page prints the full author list (about 100 names). The short "et al." form above is the form the BraTS organisers themselves use on Synapse. Where the site has room, copy the full list from the TCIA page rather than retyping it.
2. Menze, B. H., Jakab, A., Bauer, S., Kalpathy-Cramer, J., Farahani, K., Kirby, J., Burren, Y., Porz, N., Slotboom, J., Wiest, R., Lanczi, L., Gerstner, E., Weber, M.-A., Arbel, T., Avants, B. B., Ayache, N., Buendia, P., Collins, D. L., Cordier, N., … Van Leemput, K. (2015). The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS). In IEEE Transactions on Medical Imaging (Vol. 34, Issue 10, pp. 1993–2024). Institute of Electrical and Electronics Engineers (IEEE). DOI: 10.1109/tmi.2014.2377694
3. Bakas, S., Akbari, H., Sotiras, A., Bilello, M., Rozycki, M., Kirby, J. S., Freymann, J. B., Farahani, K., & Davatzikos, C. (2017). Advancing The Cancer Genome Atlas glioma MRI collections with expert segmentation labels and radiomic features. In Scientific Data (Vol. 4, Issue 1). https://doi.org/10.1038/sdata.2017.117

### 3.4 The six dataset citations

Copied from the TCIA page, where they sit under "please be specific and also cite the following datasets that were part of this Challenge".

1. Bakas, S., Akbari, H., Sotiras, A., Bilello, M., Rozycki, M., Kirby, J., Freymann, J., Farahani, K., & Davatzikos, C. (2017). Segmentation Labels for the Pre-operative Scans of the TCGA-GBM collection [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/K9/TCIA.2017.KLXWJJ1Q
2. Bakas, S., Akbari, H., Sotiras, A., Bilello, M., Rozycki, M., Kirby, J., Freymann, J., Farahani, K., & Davatzikos, C. (2017). Segmentation Labels for the Pre-operative Scans of the TCGA-LGG collection [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/K9/TCIA.2017.GJQ7R0EF
3. Scarpace, L., Mikkelsen, T., Cha, S., Rao, S., Tekchandani, S., Gutman, D., Saltz, J. H., Erickson, B. J., Pedano, N., Flanders, A. E., Barnholtz-Sloan, J., Ostrom, Q., Barboriak, D., & Pierce, L. J. (2016). The Cancer Genome Atlas Glioblastoma Multiforme Collection (TCGA-GBM) (Version 4) [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/K9/TCIA.2016.RNYFUYE9
4. Pedano, N., Flanders, A. E., Scarpace, L., Mikkelsen, T., Eschbacher, J. M., Hermes, B., Sisneros, V., Barnholtz-Sloan, J., & Ostrom, Q. (2016). The Cancer Genome Atlas Low Grade Glioma Collection (TCGA-LGG) (Version 3) [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/K9/TCIA.2016.L4LTD3TK
5. Calabrese, E., Villanueva-Meyer, J., Rudie, J., Rauschecker, A., Baid, U., Bakas, S., Cha, S., Mongan, J., & Hess, C. (2022). The University of California San Francisco Preoperative Diffuse Glioma MRI (UCSF-PDGM) (Version 1) [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/tcia.bdgf-8v37
6. Bakas, S., Sako, C., Akbari, H., Bilello, M., Sotiras, A., Shukla, G., Rudie, J. D., Flores Santamaria, N., Fathi Kazerooni, A., Pati, S., Rathore, S., Mamourian, E., Ha, S. M., Parker, W., Doshi, J., Baid, U., Bergman, M., Binder, Z. A., Verma, R., … Davatzikos, C. (2021). Multi-parametric magnetic resonance imaging (mpMRI) scans for de novo Glioblastoma (GBM) patients from the University of Pennsylvania Health System (UPENN-GBM) (Version 2) [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/TCIA.709X-DN49

A gap we noticed (UNCONFIRMED, see section 9): the same page lists seven related collections. Three of them (IvyGAP, CPTAC-GBM and ACRIN-FMISO-Brain) have no citation in this list of six.

---

## 4. TCIA's own rules, on top of the licence

Source: TCIA, "Data Usage Policies and Restrictions". CONFIRMED.
https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/

The collection page says users "must abide by" this policy, so it applies as well as CC BY 4.0.

1. **No identifying patients.** Any user must agree to "Not use the requested datasets, either alone or in concert with any other information, to identify or contact individual participants". Users also agree not to generate facial images or anything similar that could reveal who a participant is.
2. **Always name the dataset and the archive.** Users must acknowledge, in all presentations and publications, the specific dataset and the repository it came from.
3. **Always cite the DOI.** Each dataset has a data citation with a DOI "that must be cited or attributed any time the data are used". The policy says to use the full data citation and DOI link, not just the web page address.
4. **Extra duties if we host a copy.** This is the rule PLAN.md did not know about:
   > "If you are considering mirroring a copy of our publicly available datasets or providing direct access to any of our data via another tool or website please review our Data Analysis Centers (DACs) page for more information. DACs must provide attribution of each individual dataset they facilitate access to, and link to this TCIA data usage policy.  They must also require downstream users to do the same."

   The DACs page (https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22515655, which redirects to https://www.cancerimagingarchive.net/tcia-data-analysis-center/) describes a DAC as "a tool or website which provides additional capabilities for downloading, visualizing or analyzing TCIA data", and asks people who have built one to contact the helpdesk.

What this means for us (OUR READING):

- Our data repo hosts 8 cases derived from TCIA data, and our site visualises them. Whether that makes us a "DAC" is UNCONFIRMED. We act as if it does, because the duties are cheap and reasonable.
- So the data repo's ATTRIBUTION file and the site's Methods page must: give the data citation and DOI; link to the TCIA data usage policy; and ask anyone who reuses the 8 demo files to do the same.
- We ask the TCIA helpdesk to confirm (section 10).

TCIA's site disclaimer (https://www.cancerimagingarchive.net/disclaimer/) adds that the archive's operators do not guarantee the accuracy or completeness of the data, and repeats that users must "make no attempt to identify individuals".

---

## 5. The Synapse copy and its terms

We do **not** rely on these terms for anything shown on the website. They matter because Debraj accepts them with his own account to download one spreadsheet.

### 5.1 The BraTS 2021 page is archived (CONFIRMED)

Source: https://www.synapse.org/Synapse:syn25829067 (wiki last modified 08/15/2025)

The page says: "This challenge site is now archived. Data is no longer available for download here." It points to the BraTS 2023 Adult Glioma challenge instead. Its Files tab showed no content when viewed without signing in.

### 5.2 The data now lives in the BraTS 2023 project (CONFIRMED)

Source: https://www.synapse.org/Synapse:syn51156910/wiki/622351

- The BraTS 2023 page says its training and validation data "describe a total of 5,880 MRI scans from 1,470 brain diffuse glioma patients and are identical to the data curated for the RSNA-ASNR-MICCAI BraTS 2021 Challenge."
- But the files are not byte-for-byte the same as the 2021 release. The page says: "Note that starting this year, the label value for ET is "3" (compared to "4" in previous BraTS Challenges)." The archive names also show a new naming scheme (`ASNR-MICCAI-BraTS2023-GLI-Challenge-TrainingData.zip`).
- OUR READING: a label file where the enhancing tumor is stored as 3 cannot have the same checksum as TCIA's file where it is stored as 4. So the Synapse 2023 copy can never be proven identical to TCIA's by checksum. This is one reason it is not used for display.

### 5.3 The terms Debraj accepts (CONFIRMED)

Source: "Data Access/Download", section "Post-Challenge Terms and Conditions" (wiki last modified 11/05/2026).
https://www.synapse.org/Synapse:syn51156910/wiki/627000

- **Licence.** "CC-BY-NC License Restriction: The Data is subject to a CC-BY-NC license." and "Data can be used for non-commercial use only." The terms link to https://creativecommons.org/licenses/by-nc/4.0/
- **Attribution statement.** "Research publications must acknowledge the BraTS challenge organizing members as follows: "Data used in this publication were obtained as part of the Brain Tumor Segmentation (BraTS) Challenge project through Synapse ID: syn51156910.""
- **Citations.** The same three papers as in section 3.3, plus a MedPerf paper listed for "Any dataset and/or MedPerf client": Karargyris, A., et al. "Federated benchmarking of medical artificial intelligence with MedPerf". Nature Machine Intelligence 5:799–810 (2023). https://doi.org/10.1038/s42256-023-00652-2
- **Download activity is shared.** By accepting and downloading, the user consents to Sage Bionetworks "sharing your download activity and user information with the Challenge organizers to evaluate use of the Data, if requested for purposes related to the Data." The terms say this lets Sage disclose the user's Synapse username and anything in their user profile, and that organisers may contact the user through that username about the data.

### 5.4 What the Synapse terms say about redistribution and public display

- The post-challenge terms contain no sentence about redistribution or public display beyond naming the licence. CONFIRMED by reading the whole section.
- The CC BY-NC 4.0 deed (https://creativecommons.org/licenses/by-nc/4.0/) allows "Share — copy and redistribute the material in any medium or format" with the same attribution duty as CC BY, plus: "NonCommercial — You may not use the material for commercial purposes." CONFIRMED.
- OUR READING: the Synapse licence would not forbid a free, non-commercial site from showing the scans. We still do not use it for display, for three reasons: it is narrower than TCIA's licence and would force a non-commercial restriction onto anyone reusing our demo files; it is a click-through agreement tied to one person's account; and the files have been altered (5.2), so they cannot be matched to TCIA's.
- Synapse's general governance documents and terms of service, which every account holder has already accepted, were not re-read today (UNCONFIRMED, section 9).

### 5.5 A small mismatch between sources (UNCONFIRMED)

The TCIA page's acknowledgement names "Synapse ID (syn25829067)". The Synapse 2021 "Rules & Resources" page (https://www.synapse.org/Synapse:syn25829067/wiki/626944) words the same acknowledgement with "(syn25829070)". We follow the TCIA page, because TCIA is the door we rely on.

---

## 6. How the reference outlines were made

Source: Baid et al., "The RSNA-ASNR-MICCAI BraTS 2021 Benchmark on Brain Tumor Segmentation and Radiogenomic Classification", arXiv:2107.02314, version 2 (12 Sep 2021), read in arXiv's own HTML rendering. The paper is itself released under CC BY 4.0. CONFIRMED.
https://arxiv.org/abs/2107.02314 and https://arxiv.org/html/2107.02314v2

### 6.1 The exact wording

Section 2.1, "Data":

> "Ground truth annotations of every tumor sub-region for task 1 were approved by expert neuroradiologists"

Section 2.1.1, "Imaging Data Description":

> "all imaging volumes have then been segmented using the STAPLE [25] fusion of previous top-ranked BraTS algorithms, namely, nnU-Net [26], DeepScan [27], and DeepMedic [28]. These fused labels were then refined manually by volunteer neuroradiology experts of varying rank and experience, following a consistently communicated annotation protocol. The manually refined annotations were finally approved by experienced board-certified attending neuro-radiologists, with more than 15 years of experience working with gliomas."

Section 2.1.4, "Tumor Annotation Protocol":

> "To facilitate the annotation process for BraTS 2021, initial automated segmentations were generated by fusing previously top-performing BraTS methods. The specific methods fused were the DeepMedic [28], DeepScan [27], and nnU-Net [26], all trained on the BraTS 2020 dataset [11, 12, 13]."

> "Once the automated segmentations were refined by the annotators, two senior attending board-certified neuroradiologists with more than 15 years of experience each, reviewed the segmentations. Depending upon correctness, these segmentations were either approved or returned to the individual annotator for further refinements."

### 6.2 In plain words

1. Three earlier computer methods each outlined the tumor. Their outlines were merged into one draft (STAPLE is the name of the merging method).
2. Volunteer neuroradiology experts corrected the draft by hand.
3. Two senior neuroradiologists reviewed each corrected outline and either approved it or sent it back, repeating until it was acceptable.

### 6.3 The wording this project uses

- We say **"expert-approved reference outline"**. The paper supports this directly.
- We do **not** say "drawn by hand by an expert" or "ground truth drawn by an expert". The paper does not support it: the outlines began as computer output and were then corrected.
- Other pages use looser wording. The TCIA page says "manually generated ground truth labels", and the Synapse pages say annotations "are created and approved by expert neuroradiologists". The paper is the most detailed account and was written by the people who made the labels, so we follow the paper.

### 6.4 A limitation to state on the Methods page (OUR READING)

Because the outlines started from computer output, the reference may sit closer to what segmentation programs tend to draw than a fully hand-drawn outline would. That could make any model's score look slightly better than it would against independent hand-drawn outlines. The paper does not measure this, so we state it as a possibility, not a finding.

### 6.5 Other facts from the paper that the project uses (CONFIRMED)

- All scans were converted to NIfTI, aligned to one anatomical template (SRI24), resampled to 1 mm³ and skull-stripped (section 2.1.1).
- Label values in the 2021 release: 1 for necrotic core, 2 for edema, 4 for enhancing tumor (sections 2.1.1 and 2.2.1). The TCIA page says the same.
- Case counts in the paper's Table 1: BraTS 2021 has 2,040 cases in total, split into 1,251 training, 219 validation and 570 testing. BraTS 2018 had 285 training cases.
- The paper says a name mapping between earlier challenges and this one "will be provided". That is the file in section 8.3.

---

## 7. What is and is not allowed, in one list

Allowed, with the conditions below:

- Showing the 8 demo cases publicly on the website and hosting them in the `brain-tumor-viewer-data` repo.
- Converting them for the web (8-bit, compressed) and showing a model's outline on top.
- Publishing metrics, tables and figures computed from the data.

Conditions we must meet every time:

- The data citation with its DOI, the acknowledgement sentence, the three papers and the six dataset citations (section 3).
- A link to the CC BY 4.0 licence and a plain statement of what we changed (section 2.2).
- A link to the TCIA data usage policy, and a request that anyone reusing the demo files does the same (section 4).
- The displayed files are TCIA's, or proven identical to TCIA's by checksum (section 1).

Not allowed:

- Trying to work out who any patient is, or producing anything that could help someone else do so.
- Wording that suggests TCIA, the BraTS organisers, the hospitals or any university endorse this project.
- Displaying or redistributing scan files obtained through Synapse.
- Adding our own restrictions to the demo files.
- Putting any scan file in the code repo, or using patient data from any other source (project rule, CLAUDE.md).

---

## 8. The files

### 8.1 Two small TCIA files, downloaded Nov 16, 2026 (CONFIRMED)

Both are linked from the TCIA collection page and saved in `C:\BrainTumorData\meta` (outside the repo). The SHA-256 value is the file's fingerprint, computed on the laptop with PowerShell's `Get-FileHash`. If the file is ever downloaded again, the fingerprint tells us whether TCIA changed it.

| File | Size in bytes | SHA-256 | Link |
|---|---|---|---|
| `BraTS2021_MappingToTCIA.xlsx` | 80,000 | `223243C5821C282E90DA980BA38D860AB2D2A597D1F4F1800EBE227329A2DC0B` | https://www.cancerimagingarchive.net/wp-content/uploads/BraTS2021_MappingToTCIA.xlsx |
| `NotPreviouslyInTCIA.csv` | 238,835 | `363D410CD3DB19F41896DFD7AE6A4C2E74B70B5A00195B4634D620FC4E9F9010` | https://www.cancerimagingarchive.net/wp-content/uploads/NotPreviouslyInTCIA.csv |

- The server reported both files as last modified on Sep 14, 2023. The downloaded sizes match the sizes the server reported.
- TCIA describes the first as a "Manifest of case identifiers between BraTS and TCIA" and the second as a "Spreadsheet list of new (NIfTI) series files with no TCIA DICOM equivalent".
- `NotPreviouslyInTCIA.csv` has no header row. It has 1,967 lines, and each line is the path of one file inside the TCIA package, for example a line ending `new-not-previously-in-TCIA/BraTS2021_00118/BraTS2021_00118_flair.nii.gz`. Both training-set and validation-set paths appear.
- `BraTS2021_MappingToTCIA.xlsx` has not been opened yet. Its columns are recorded in Session 4 or 5 (UNCONFIRMED until then).

### 8.2 The TCIA package and its checksum list (listing CONFIRMED, transfer UNCONFIRMED)

Source: the "DOWNLOAD (142GB)" link on the TCIA collection page, which opens an IBM Aspera page. Viewed Nov 16, 2026. Nothing was downloaded.

- The package note says: "Data are 142GB about 1,479 individual participants in 407,245 files in .nii.gz or .dcm format". The package was sent on November 11, 2023.
- The package can be browsed folder by folder, and every folder and file has its own selection box. So single cases can be selected. Top level:
  - `RSNA-ASNR-MICCAI-BraTS-2021.sums`, 47.54 MB. By its name this is a list of checksums for the package. Its format and checksum type are UNCONFIRMED until it is opened.
  - `RSNA-ASNR-MICCAI-BraTS-2021/`, containing `BraTS2021_TrainingSet`, `BraTS2021_TrainingSet_dcm`, `BraTS2021_ValidationSet` and `BraTS2021_ValidationSet_dcm`.
- Inside `BraTS2021_TrainingSet` the cases are sorted by where they came from: `ACRIN-FMISO-Brain`, `CPTAC-GBM`, `IvyGAP`, `TCGA-GBM`, `TCGA-LGG`, `UCSF-PDGM`, `UPENN-GBM` and `new-not-previously-in-TCIA`. This helps leakage Check B in Session 5.
- One case, as listed (`new-not-previously-in-TCIA/BraTS2021_00118`): `_flair.nii.gz` 1.79 MB, `_seg.nii.gz` 125.45 KB, `_t1.nii.gz` 1.85 MB, `_t1ce.nii.gz` 1.81 MB, `_t2.nii.gz` 1.99 MB. About 7.6 MB for the whole case.
- The TCIA page says "Download requires IBM-Aspera-Connect plugin". We have not installed it, so we have not tested whether a single-file transfer actually completes.

Change from PLAN.md, agreed Nov 16, 2026: instead of downloading the 8 demo cases from TCIA and comparing them by hand, we plan to fetch the checksum list and compare it against the Kaggle copy. That can cover every case in the locked test set, not only the 8. It needs the Aspera client, so it is scheduled for a later session together with a one-file test download.

### 8.3 The Synapse mapping file (CONFIRMED)

- Name: `BraTS2023_2017_GLI_Mapping.xlsx`
- Synapse ID: syn51615438, version 1. https://www.synapse.org/Synapse:syn51615438
- Location: BraTS 2023 Challenge project (syn51156910), Files, `Data` (syn64952532), `BraTS-GLI` (syn51514105).
- Created 5/31/2023, last modified 6/5/2025, as shown on its page.
- It is **not** in the BraTS 2021 project, which PLAN.md assumed. The name `BraTS21-17_Mapping.csv`, which PLAN.md gave as the other possibility, was not found.
- Downloading it needs a signed-in account that has accepted the terms in section 5.3. Debraj signed in, accepted those terms and downloaded it himself on Nov 16, 2026.
- Saved in `C:\BrainTumorData\meta`. Size 86,360 bytes. SHA-256 `ABBD36AD733E66DFC4C4BA036F12BA8B6E2B554BCCA80CC7574863CF61482BA4`.
- It has one sheet, `Sheet1`. **Corrected Nov 18, 2026 (Session 4):** it has 1,256 rows with content: 1 header row and 1,255 data rows. Of these, **1,251 are BraTS 2021 training cases** (IDs `BraTS2021_00000` to `BraTS2021_01666`, each listed once), the same count and ID range as the Kaggle copy (section 8.4). The other 4 are IvyGAP cases from the BraTS 2020 training set that were not carried into BraTS 2021 (`N/A` in the `BraTS2021` column). The file lists no validation or test cases.
  - What went wrong in Session 2: the sheet is formatted down to row 2,041, and Session 2 counted that formatted area instead of the rows that hold data. 2,040 happened to equal the paper's total for all of BraTS 2021, so it looked like a confirmation. The file itself is unchanged: its SHA-256 still matches the value below.
- Columns, exactly as written in the header row:
  1. `BraTS2023` (example: `BraTS-GLI-00000-000`)
  2. `BraTS2021` (example: `BraTS2021_00000`)
  3. `BraTS2020`
  4. `BraTS2019`
  5. `BraTS2018`
  6. `BraTS2017`
  7. `Cohort Name (if publicly available)` (example: `Private Collection`)
  8. `Site No (represents the originating institution)` (example: `18`)
  9. `Local ID ` (the header has a trailing space)
- It does list cases by their BraTS 2021 IDs, so it can be joined to the TCIA files and the Kaggle copy by that column.
- A case that was not in an earlier year has the text `N/A` in that year's column. Note for Session 4: pandas, the Python table library, treats the text `N/A` as "missing" by default when it loads a file, so we must decide deliberately how to read these cells and check the counts by hand.
- Counted in Session 4 (Nov 18, 2026, `scripts/04_count_by_earliest_year.py`), for the 1,251 training cases: 285 first appeared in 2017 and are in every year from 2017 to 2020, including 2018; 50 first appeared in 2019 (and are in 2020); 30 appeared only in 2020; 886 are in no earlier year. No case skips a year, and the year columns have no empty cells. 285 equals the number of BraTS 2018 training cases the model was trained on (PLAN.md section 3).
- **Repeat scans (naming CONFIRMED; same patient is a strong inference, not a patient-ID match).** In the `BraTS2023` names (`BraTS-GLI-<5 digits>-<3 digits>`), 1,133 cases end in `-000` with the same 5 digits as their own BraTS 2021 number. The other 118 end in `-001` and share their 5 digits with another case ending in `-000` (example: `BraTS2021_01538` is `BraTS-GLI-00097-001`, and `BraTS2021_00097` is `BraTS-GLI-00097-000`). So 118 patients have two scans each (236 cases), and the BraTS 2021 data holds 1,133 patients in 1,251 cases.
  - The official meaning of the two number groups, from the BraTS 2023 "Submission Tutorial (Files)" wiki page (Synapse syn51156910, wiki 622349, read Nov 18, 2026 through Synapse's public API at https://repo-prod.prod.sagebase.org/repo/v1/entity/syn51156910/wiki/622349): "Filenames must end with the 5-digit case ID, followed by a dash, then by the 3-digit timepoint". CONFIRMED.
  - Checks in the mapping file (`scripts/04_check_repeat_scans.py`): both scans of every pair have the same Site No (all 18) and Cohort (all "Private Collection"). Their Local ID is `N/A` for all 236, so the Local ID **cannot** confirm or rule out the pairing: no patient ID is recorded for private cases. Among the 268 rows with a real Local ID, none is used twice and none appears under two patient numbers. 118 of the 119 BraTS 2021 IDs from `01538` to `01656` are second scans, a block added at the end.
  - None of the 236 scans is in any earlier BraTS year, so the patient-level leakage rule (Session 4) removes no case from the unseen pool. It matters for the split in Session 5: both scans of a patient go on the same side.
- This file came through the Synapse door, so it is covered by the CC BY-NC terms in section 5.3. We do not publish the file itself. What we may publish from it (our own lists of case IDs and their status) is OUR READING of those terms: derived ID lists with attribution, on a non-commercial project.

### 8.4 The Kaggle copy (identified Nov 16, 2026, Session 3)

This is the copy the model will run on. It is **not** an official release. It is one Kaggle user's upload of files taken from Synapse in 2021. Think of it as a photocopy of a library book made by a stranger: it may be perfect, but we check it against the original before trusting it.

Sources: the dataset page, https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1 (Data Card, expanded Metadata panel, Discussion tab), and Kaggle's own public record of the same dataset at https://www.kaggle.com/api/v1/datasets/view/dschettler8845/brats-2021-task1 and https://www.kaggle.com/api/v1/datasets/list/dschettler8845/brats-2021-task1 (these give exact byte counts and dates, where the page only says "13 GB" and "5 years ago"). Read without signing in. Nothing was downloaded.

#### What the page states (CONFIRMED)

| Item | Value, exactly as shown |
|---|---|
| Title | `BRaTS 2021 Task 1 Dataset` (with that capitalisation) |
| Subtitle | `RSNA-ASNR-MICCAI Brain Tumor Segmentation (BraTS) Challenge 2021` |
| Short name in the address | `dschettler8845/brats-2021-task1` |
| Uploader | Darien Schettler, Kaggle username `dschettler8845`. Listed as the only collaborator, with the role "Owner". The "Authors" field is empty |
| Kaggle dataset ID | 1541666 |
| Version | 1, with the note "Initial release", created 2021-08-19 at 21:59 UTC. It is the only version. "Expected update frequency: Never" |
| Total size | 13,417,502,720 bytes (the page shows "13.42 GB") |
| Licence field | "Data files © Original Authors" |
| Source field | `https://www.synapse.org/#!Synapse:syn25829067/wiki/610863` (the 2021 Synapse challenge page, now archived, section 5.1) |
| DOI field | Empty |
| Use, as counted by Kaggle on Nov 16, 2026 | 64,956 downloads, 249 notebooks, 378 votes |

The three files. A `.tar` file is an archive: many files packed into one, like a taped-up box. Kaggle does not show what is inside it ("Previews for binary data are not supported").

| File | Size in bytes | Added (UTC) |
|---|---|---|
| `BraTS2021_Training_Data.tar` | 13,396,408,320 | 2021-08-19 22:05 |
| `BraTS2021_00495.tar` | 10,321,920 | 2021-08-19 21:59 |
| `BraTS2021_00621.tar` | 10,772,480 | 2021-08-19 21:59 |

The three sizes add up to the total above exactly.

What the description says about the data. It is the 2021 Synapse challenge text, copied onto the Kaggle page:

- Label values: "the GD-enhancing tumor (ET — label 4), the peritumoral edematous/invaded tissue (ED — label 2), and the necrotic tumor core (NCR — label 1)".
- Conditions: "Challenge participants must abide by the guiding principles for responsible research use and data handling within the Synapse Commons Platform as described in the Synapse Governance documents and by the Challenges Official Rules."
- Use: "You are free to use and/or refer to the BraTS datasets in your own research, provided that you always cite the flagship manuscript (published or pre-published) resulting from the challenge as well as the following three manuscripts". The three are the papers in section 3.3. It also asks for the two TCGA segmentation-label citations (items 1 and 2 in section 3.4).
- Acknowledgement sentence, with "Synapse ID (syn25829067)", the same ID the TCIA page uses (section 5.5).

The Discussion tab has 5 topics. None reports missing, damaged or corrected files, and none explains the two single-case archives.

#### Not known until we look inside (UNCONFIRMED)

The page does not state any of these. They were the questions going into the Session 3 notebook; the answers are in the next part, "What the notebook found".

- **Case count.** The page gives no number. We expect 1,251 (the paper's training-set count, section 6.5). A size check that is only a hint (OUR READING): 13,396,408,320 bytes divided by 1,251 is about 10.7 MB per case, and the two single-case archives are 10.3 MB and 10.8 MB, so the size fits 1,251 cases.
- **File layout and file names** inside `BraTS2021_Training_Data.tar`.
- **The label values actually stored** in the label files. The description says 4 for enhancing tumor; Half B of Session 3 prints the real values.
- **Whether cases 00495 and 00621 are also inside the big archive**, and if so whether those copies differ from the two separate ones.

#### What the notebook found (Nov 16, 2026, Session 3)

Run in a private Kaggle notebook on Debraj's account (`debrajkarmaker/brain-tumor-viewer-01-first-look`), no GPU, no internet, dataset attached at `/kaggle/input/datasets/dschettler8845/brats-2021-task1/`. The notebook is in this repo as `notebooks/01_first_look.ipynb`. It is the file Debraj downloaded from Kaggle, with each cell's real text output kept and one thing removed: the picture of a scan slice drawn by the last cell, because scan images are never committed here.

How far to trust the numbers below: they were first read off the screen, then checked one by one against the text output saved in that notebook file. All of them matched. Two also check themselves: the four label counts add up to exactly 240 × 240 × 155 = 8,928,000 voxels, and case 00118's five sizes convert to exactly the five figures in TCIA's listing.

- **Case count: 1,251** (CONFIRMED by counting). Case IDs run from `BraTS2021_00000` to `BraTS2021_01666`, so the numbering has gaps.
- **Files: 6,255 scan files, exactly 5 per case**, plus one junk file, `./.DS_Store`. That is a file macOS creates when a folder is opened in Finder. It shows the archive was re-packed on a Mac, so it is not the organisers' own packaging. It holds no scan data.
- **Layout:** `./BraTS2021_00000/BraTS2021_00000_flair.nii.gz`, one folder per case. The five endings are `_flair`, `_seg`, `_t1`, `_t1ce`, `_t2`, the same file names TCIA uses (section 8.2). No renamed files were found. The folders are not sorted by source collection as TCIA's are.
- **Cases 00495 and 00621 are in the big archive as well as in their own archives.** All 10 files (5 per case) have the same SHA-256 fingerprint in both places, so they are plain duplicates, not two versions. Doubt D4 is closed. Why they were packed separately is still not stated anywhere.
- **Case 00495** (from its own archive, where the files sit loose with no folder): flair 2,503,035 bytes, seg 37,663, t1 2,652,585, t1ce 2,689,385, t2 2,428,304.
- **Case 00118**, the case whose sizes we recorded from TCIA's listing: flair 1,872,411 bytes, seg 128,462, t1 1,936,184, t1ce 1,896,946, t2 2,086,035. Divided by 1,048,576 (and the seg file by 1,024) these are 1.79 MB, 125.45 KB, 1.85 MB, 1.81 MB and 1.99 MB, which are exactly the five sizes TCIA's listing shows. So for this one case the files are the same size in both copies. Same size is good evidence but not proof of the same contents; only the checksum comparison in B1 can show that. Doubt D5 is much weaker but stays open.
- **Kaggle account:** the weekly quota shown is 30 hours of GPU and 20 hours of TPU, with none used. The account is not phone-verified, which Kaggle normally requires before GPU or internet can be switched on in a notebook.

One case opened with nibabel 5.4.2 (case 00495, chosen only because its archive is small and quick to unpack; it was unpacked to `/kaggle/temp`, a scratch folder that is wiped when the session ends):

- **All five files have the same grid:** 240 × 240 × 155 voxels, each voxel a 1 mm cube, orientation codes `('L', 'P', 'S')`. This matches the paper (section 6.5). The codes mean that counting up along the three axes moves towards the patient's left, the back of the head and the top of the head.
- **Number types:** the four scans are stored as `int16` (whole numbers); the label map as `uint16`. Every file's smallest value is 0. Largest values in this case: t1 6,402, t1ce 12,299, t2 2,508, flair 2,289. The scans have no fixed brightness scale, which is why the model's own normalisation step matters later (Session 7).
- **Label values present: 0, 1, 2 and 4. There is no 3.** Counts in this case: label 0 (not tumor) 8,828,698 voxels; label 1 (necrotic core) 20,808; label 2 (edema) 46,447; label 4 (enhancing tumor) 32,047. This is the 2021 convention, the same as TCIA's (doubt D9). It has been checked in **one case only**; every case used for results gets the same check when the model is run.
- A caution for later: this notebook looked at pictures of case 00495 before the locked test set exists. Looking at one case to learn the file format does not tune anything, but it is recorded here so it is not forgotten when the lists are made in Session 5.

#### What makes this copy doubtful as a match for the TCIA release

| # | Doubt | Why it matters | How it gets settled |
|---|---|---|---|
| D1 | **It came through the Synapse door, not TCIA's.** Its source field is the 2021 Synapse page and its conditions are the 2021 challenge rules | By the rule in section 1, a copy carries the terms of the door it came through. Nothing on this page gives CC BY 4.0. So this copy can be used for computing, never as the licence basis for display | Already handled by the route in section 1 |
| D2 | **The licence field is "Data files © Original Authors".** That is not an open licence. It says only that the rights belong to someone else | The page does not say the uploader had permission to redistribute the files. Our own use is research use with the citations the page asks for, which the copied conditions allow (OUR READING). The uploader's right to post it is UNCONFIRMED | Session 33 review (U13) |
| D3 | **A third party's upload, two years older than TCIA's release.** Uploaded 2021-08-19. TCIA's release is dated 2023/08/25 and its package was sent on November 11, 2023 (section 8.2) | Any file the organisers corrected between those dates would differ. We have no evidence either way | Checksum comparison in Buffer B1 (U5) |
| D4 | **Two cases sit in their own archives** (`BraTS2021_00495.tar`, `BraTS2021_00621.tar`) with no explanation | They could be corrected replacements for copies inside the big archive, or the only copies. Until we know, there may be two different versions of these two cases, and we cannot say which one TCIA holds | Closed Nov 16, 2026: both cases are also in the big archive and all 10 files are identical in both places |
| D5 | **The file sizes may not match TCIA's.** TCIA lists case 00118 at about 7.6 MB for its 5 files (section 8.2). The two single-case archives here are 10.3 MB and 10.8 MB | They are different cases, and tumor size changes how well a scan compresses, so this proves nothing yet. But if the same case is a different size in the two copies, the files are not byte-for-byte identical and their checksums cannot match, even if the pictures inside are the same. A `.nii.gz` file is a compressed file, and the same picture can be compressed into different bytes | Weaker since Nov 16, 2026: case 00118's five files are the same sizes as in TCIA's listing. Same size is not proof of the same bytes, so it stays open until B1 |
| D6 | **Archives, not loose files.** TCIA's checksum list is expected to cover individual files | A checksum of a `.tar` archive can never match anything in TCIA's list. Each file has to be taken out of the archive first and fingerprinted on its own | Done inside the cloud notebook in B1 |
| D7 | **Different folder layout is likely.** TCIA sorts cases into folders by source collection (section 8.2). This copy predates that | Files must be matched by case ID and file name, not by folder path. Any renamed file would break the match | Notebook listing |
| D8 | **Training cases only.** The title says "Task 1" and the big archive is named "Training_Data". TCIA's package also holds the validation set | Not a problem for us: we only use cases that have reference outlines. It does mean this copy cannot be compared with TCIA's whole package, only with its training part | Notebook listing |
| D9 | **The label 3 versus 4 question.** The description says enhancing tumor is label 4, matching TCIA and the paper (section 6.5), and the upload predates the 2023 change to label 3 (section 5.2) | If label 3 were found instead, this copy would be the altered 2023 version and could never match TCIA's checksums | Checked in one case on Nov 16, 2026: values 0, 1, 2 and 4, no 3. Every other case is checked when the model is run (U14) |
| D10 | **It can disappear.** A user's dataset can be deleted by its owner or by Kaggle | Our notebooks would stop running. Kaggle lists other uploads of the same data (for example one with 6,255 loose files, which is 1,251 × 5), but each is a copy of a copy and would need the same checks | Record the dataset ID and version (above) in every notebook. No action unless it happens |

What does not change: the display rule in section 1. If the checksums in B1 do not match TCIA's, the fallback is to download the 8 demo cases from TCIA itself (about 8 MB each as listed, so well under 100 MB in total) and display those files, and to compare the Kaggle copy with them by picture content rather than by compressed bytes.

---

## 9. Still unconfirmed

| # | Open item | Blocks publishing? | When it gets checked |
|---|---|---|---|
| U1 | Closed Nov 16, 2026. The mapping file was downloaded and its columns recorded in section 8.3. Still open from it: whether publishing ID lists derived from a CC BY-NC file needs anything beyond attribution | No | Session 33 review |
| U2 | Columns of `BraTS2021_MappingToTCIA.xlsx` | No | Session 4 or 5 |
| U3 | Whether a single-file Aspera transfer from the TCIA package works on this laptop | No | Aspera session (to be scheduled) |
| U4 | Format and checksum type of the `.sums` file | **Yes** | Aspera session (Buffer B1); also asked in the helpdesk email sent Nov 18, 2026 |
| U5 | Whether the Kaggle-hosted copy is identical to TCIA's files. Its name, uploader and stated licence were recorded on Nov 16, 2026 (section 8.4). Still open: the comparison itself, including whether the compressed files are byte-for-byte the same (doubts D3 and D5) | **Yes** | Buffer B1 (compare) |
| U6 | Whether hosting 8 derived cases makes this project a "Data Analysis Center" under TCIA's policy, and whether TCIA wants anything beyond section 4 | **Yes** (PLAN.md 5.9: launch waits on the answer, the build does not) | Helpdesk email, sent Nov 18, 2026; waiting on the reply (section 10) |
| U7 | Whether IvyGAP, CPTAC-GBM and ACRIN-FMISO-Brain need their own citations when a displayed case comes from one of them | **Yes**, if a demo case comes from one of them | Helpdesk email, sent Nov 18, 2026; waiting on the reply. If no answer, cite them anyway from their TCIA pages |
| U8 | Subject counts disagree: 1,480 (TCIA table), "about 1,479" (package note), 1,470 (Synapse 2023 page; 1,251 + 219 in the paper) | No | Count the cases ourselves in Sessions 4 and 5 |
| U9 | Synapse ID in the acknowledgement: syn25829067 (TCIA) or syn25829070 (Synapse rules page) | No | Follow TCIA; mention in the helpdesk email only if there is room |
| U10 | The CC BY 4.0 legal code was not read in full; only the deed was | No | Session 33 review |
| U11 | Synapse's general governance documents and terms of service were not re-read | No (not relied on for display) | Session 33 review |
| U12 | Closed Nov 16, 2026. The Kaggle archives hold 1,251 cases, 5 files each, with TCIA's file names; cases 00495 and 00621 are identical duplicates, not two versions (section 8.4) | No | Done |
| U13 | Whether the Kaggle uploader had permission to redistribute the files, given the licence field "Data files © Original Authors" (section 8.4, doubt D2) | No (the Kaggle copy is never the licence basis for display) | Session 33 review |
| U14 | The label values actually stored in the Kaggle copy's label files (expected 0, 1, 2, 4). Checked in one case on Nov 16, 2026: 0, 1, 2 and 4, no 3 (section 8.4). Still open for all other cases | **Yes** (label 3 would mean it is not the 2021 release) | Checked for every case when the model is run (Stage 2) |

---

## 10. Who was asked

| Date | Who | Question | Answer |
|---|---|---|---|
| Sent Nov 18, 2026 (drafted Nov 16; Debraj made small wording edits before sending) | TCIA helpdesk, by email from Debraj's university account | The three questions in `docs/TCIA_HELPDESK_EMAIL.md`: (1) is the planned hosting of 8 converted cases consistent with TCIA's policy, and is it "mirroring" or a Data Analysis Center (U6); (2) is `RSNA-ASNR-MICCAI-BraTS-2021.sums` the right file to compare the Kaggle copy against, and which checksum type it uses (U4, U5); (3) should IvyGAP, CPTAC-GBM or ACRIN-FMISO-Brain be cited if a demo case comes from one of them (U7) | **Waiting.** None yet |

Debraj sends the email himself. When a reply arrives, its date and exact wording are added to this table.

---

## 11. Sources, all read Nov 16, 2026

- TCIA collection page, RSNA-ASNR-MICCAI-BraTS-2021 (Version 1, updated 2023/08/25): https://www.cancerimagingarchive.net/analysis-result/rsna-asnr-miccai-brats-2021/
- TCIA Data Usage Policies and Restrictions: https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/
- TCIA Data Analysis Centers page: https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22515655
- TCIA site disclaimer: https://www.cancerimagingarchive.net/disclaimer/
- TCIA Aspera package page: reached through the "DOWNLOAD (142GB)" link on the collection page
- Creative Commons BY 4.0 deed: https://creativecommons.org/licenses/by/4.0/
- Creative Commons BY-NC 4.0 deed: https://creativecommons.org/licenses/by-nc/4.0/
- Synapse, BraTS 2021 Challenge (archived): https://www.synapse.org/Synapse:syn25829067 and its Rules & Resources page https://www.synapse.org/Synapse:syn25829067/wiki/626944
- Synapse, BraTS 2023 Adult Glioma: https://www.synapse.org/Synapse:syn51156910/wiki/622351
- Synapse, BraTS 2023 Data Access/Download and Post-Challenge Terms and Conditions: https://www.synapse.org/Synapse:syn51156910/wiki/627000
- Synapse, BraTS 2023 Data Conditions for Use: https://www.synapse.org/Synapse:syn51156910/wiki/622360
- Synapse, BraTS-GLI data folder: https://www.synapse.org/Synapse:syn51514105
- Baid et al. 2021, arXiv:2107.02314v2: https://arxiv.org/abs/2107.02314
- Kaggle, "BRaTS 2021 Task 1 Dataset" (read in Session 3, same date): https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1 and Kaggle's public records of it, https://www.kaggle.com/api/v1/datasets/view/dschettler8845/brats-2021-task1 and https://www.kaggle.com/api/v1/datasets/list/dschettler8845/brats-2021-task1
