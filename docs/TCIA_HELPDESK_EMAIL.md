# Email to the TCIA helpdesk

**What this file is for.** It holds the email Debraj sent to The Cancer Imaging Archive (TCIA) helpdesk to confirm that the way this project shows 8 demo cases follows TCIA's rules. The background is in `docs/DATA_ACCESS.md`, sections 4 and 9.

**Status: sent Nov 18, 2026** by Debraj, from his university email account, to the TCIA helpdesk address. Waiting on a reply. When it arrives, record its date and exact wording in section 10 of `docs/DATA_ACCESS.md`.

**The sent version is not word-for-word the draft below.** Before sending, Debraj made small edits: the wording about converting the cases to 8-bit ("converted to 8-bit"), and the numbering of the three questions. The exact sent text is in his sent mail; the draft below is kept as written on Nov 16, 2026, so this file does not guess at his wording. The three questions are the same.

---

**Subject:** RSNA-ASNR-MICCAI-BraTS-2021 (DOI 10.7937/jc8x-9874): showing 8 cases on a small educational website

Hello,

I am a first-year undergraduate student working on an independent, non-commercial education project. It is a free website where a visitor can open a few brain MRI cases and compare a pretrained segmentation model's tumor outline with the expert-approved reference outline. It is for research and education only and states clearly that it is not for diagnosis.

I would like to use 8 cases from the segmentation-task NIfTI training data in the RSNA-ASNR-MICCAI-BraTS-2021 collection, which your page lists under CC BY 4.0. I have three questions.

1. To load quickly in a browser, I would convert the 8 cases to 8-bit, compress them, and host them in a public GitHub repository, alongside the model's output. Every page would carry the full data citation with its DOI, the related publications and dataset citations from your page, the TCGA acknowledgement sentence, a link to CC BY 4.0, a statement of what I changed, and a link to your Data Usage Policies and Restrictions with a request that anyone reusing the files does the same. Is this consistent with your policy? Does it count as "mirroring" or as a Data Analysis Center, and is there anything else you would like me to include?

2. I run the model in the cloud on a copy of the BraTS 2021 training data hosted on Kaggle, because my laptop cannot hold the full package. Before showing any case, I want to prove it is identical to your file. Is the file `RSNA-ASNR-MICCAI-BraTS-2021.sums` in the Aspera package the right thing to compare against, and which checksum type does it use?

3. Your page lists IvyGAP, CPTAC-GBM and ACRIN-FMISO-Brain as related collections, but they are not among the dataset citations given in the publications section. If one of my 8 cases comes from one of these collections, should I cite that collection as well?

Thank you for your time, and for making this data available.

Debraj Karmaker
Project repository: https://github.com/Dbrjkrm/brain-tumor-viewer
