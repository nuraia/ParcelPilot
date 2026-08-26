import pandas as pd

file_path = "data/ParcelPilot_Assessment_Data.xlsx"

excel_file = pd.ExcelFile(file_path)

print("=" * 60)
print("SHEETS")
print("=" * 60)

print("Sheet names:", excel_file.sheet_names)

for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    print("\n")
    print("=" * 60)
    print(f"SHEETS: {sheet_name}")
    print("=" * 60)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))  

    print("\n First 3 rows:")
    print(df.head(3).to_string(index=False))