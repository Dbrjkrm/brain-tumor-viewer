# 04_look_at_mapping.py
#
# What this file is for: it opens the BraTS ID mapping spreadsheet and shows what is inside,
# so we can understand every column before we use it for the leakage check.
# It only reads and prints. It changes nothing and saves nothing.
#
# How it fits the project: Session 4 (Leakage check A). The mapping file lists every BraTS 2021
# case with its ID in each earlier BraTS year. A case with an ID in the 2018 column was in the
# data the pretrained model was trained on, so it cannot count as "unseen".
# The file came from Synapse (see docs/DATA_ACCESS.md section 8.3) and lives outside the project,
# in C:\BrainTumorData\meta, so it is never uploaded to GitHub.
#
# How to run it, from the project folder:
#     .\.venv\Scripts\python.exe scripts\04_look_at_mapping.py

import pandas as pd   # pandas: the library that reads tables. "pd" is the short name everyone uses for it.

# Where the file is. The r before the quotes tells Python to read the backslashes literally.
MAPPING_FILE = r"C:\BrainTumorData\meta\BraTS2023_2017_GLI_Mapping.xlsx"

# Make pandas print wide tables on one line instead of cutting them into pieces.
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", None)

# Read the spreadsheet into a table (a "DataFrame").
#   dtype=str              -> keep every cell as plain text, exactly as written in the file
#   keep_default_na=False  -> do NOT turn "N/A" or blank cells into "missing"; show them as they are
mapping = pd.read_excel(MAPPING_FILE, dtype=str, keep_default_na=False)

# How big is the table? .shape gives (number of rows, number of columns).
print("Rows and columns:", mapping.shape)
print()

# The column names, numbered, exactly as written in the header row.
# repr() puts quotes around each name, so a hidden space at the end becomes visible.
print("Columns:")
for number, name in enumerate(mapping.columns, start=1):
    print(" ", number, repr(name))
print()

# The first 10 rows. .head(10) means "the top 10 rows of the table".
print("First 10 rows:")
print(mapping.head(10).to_string())
