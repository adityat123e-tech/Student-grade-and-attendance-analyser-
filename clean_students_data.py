
import pandas as pd
import numpy as np

# 1. Read dataset
df = pd.read_csv("StudentsPerformance_messy.csv")

# 2. Standardize column names
df.columns = (
    df.columns.astype("string")
    .str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

# 3. Remove unnecessary spaces from text columns
text_columns = df.select_dtypes(include=["object", "string"]).columns

for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

# 4. Handle missing and blank values
df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

# 5. Clean admission numbers
df["admission_no"] = (
    df["admission_no"]
    .astype("string")
    .str.upper()
    .str.replace(r"\s+", "", regex=True)
)

# 6. Remove records with missing admission numbers
df["admission_no"] = df["admission_no"].replace("", np.nan)
df.dropna(subset=["admission_no"], inplace=True)

# 7. Convert marks into numeric format
score_columns = [
    "math_score",
    "reading_score",
    "writing_score"
]

for col in score_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 8. Handle invalid marks
for col in score_columns:
    df.loc[~df[col].between(0, 100), col] = np.nan

# 9. Remove duplicate admission numbers
df.drop_duplicates(
    subset=["admission_no"],
    keep="first",
    inplace=True
)

# 10. Reset index
df.reset_index(drop=True, inplace=True)

# 11. Export cleaned dataset
df.to_csv("StudentsPerformance_cleaned.csv", index=False)

# 12. Display final results
print("DATA CLEANING COMPLETED")

print("Total records:", len(df))

print("Duplicate admission numbers:",
      df["admission_no"].duplicated().sum())

print("Missing admission numbers:",
      df["admission_no"].isna().sum())

print("\nCleaned dataset:")
print(df.head())
