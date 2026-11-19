# 04_count_by_earliest_year.py
#
# What this file is for: for every BraTS 2021 training case in the mapping file, it finds the
# first BraTS year the same scan appeared in (2017, 2018, 2019, 2020, or "new in 2021"),
# and prints how many cases fall in each group. It only reads and prints; it saves nothing.
#
# How it fits the project: Session 4 (Leakage check A). The pretrained model was trained on the
# BraTS 2018 training cases, so these counts show how much of BraTS 2021 the model may already
# have seen. The next script uses the same reading to label every case.
#
# How to run it, from the project folder:
#     .\.venv\Scripts\python.exe scripts\04_count_by_earliest_year.py

import pandas as pd

MAPPING_FILE = r"C:\BrainTumorData\meta\BraTS2023_2017_GLI_Mapping.xlsx"

# The earlier-year columns, oldest first. The order matters: we look for the FIRST year that has a name.
YEAR_COLUMNS = ["BraTS2017", "BraTS2018", "BraTS2019", "BraTS2020"]

# Read every cell as plain text, and do not let pandas turn "N/A" into "missing" (see 04_look_at_mapping.py).
mapping = pd.read_excel(MAPPING_FILE, dtype=str, keep_default_na=False)

# Keep only the rows that are BraTS 2021 cases. The file also has 4 rows of BraTS 2020 cases that
# were not carried into 2021; they have "N/A" in the BraTS2021 column, so they are dropped here.
cases = mapping[mapping["BraTS2021"] != "N/A"]
print("BraTS 2021 cases in the file:", len(cases))
print("Each case listed once?", cases["BraTS2021"].is_unique)
print()

# Safety check: every cell in the year columns should be either "N/A" or a real name.
# An empty cell would be ambiguous (missing? or not in that year?), so we count them.
for column in YEAR_COLUMNS:
    empty_cells = (cases[column].str.strip() == "").sum()
    print(column, "| empty cells:", empty_cells)
print()

# For one case (one row), return the first year it appeared in.
def earliest_year(row):
    for column in YEAR_COLUMNS:          # 2017, then 2018, then 2019, then 2020
        if row[column] != "N/A":         # a real name means the scan was in that year
            return column[-4:]           # the last 4 characters of "BraTS2018" are "2018"
    return "new in 2021"                 # no earlier year had it

# Apply that to every row. axis=1 means "one row at a time".
earliest = cases.apply(earliest_year, axis=1)

print("Cases by the first year they appeared in:")
counts = earliest.value_counts().sort_index()
for group, count in counts.items():
    print(" ", group, "|", count)
print("  total |", counts.sum())
print()

# Which combination of years does each case appear in? "Y" = in that year, "." = not.
# This shows whether any case skips a year (for example in 2017 and 2019 but not 2018).
pattern = cases[YEAR_COLUMNS].apply(lambda row: " ".join("Y" if value != "N/A" else "." for value in row), axis=1)
print("Year patterns (2017 2018 2019 2020) and how many cases have each:")
for combination, count in pattern.value_counts().items():
    print(" ", combination, "|", count)
print()

# The number the leakage check cares about most: cases with a name in the 2018 column.
in_2018 = (cases["BraTS2018"] != "N/A").sum()
print("Cases that were in BraTS 2018 (the model's training year):", in_2018)
