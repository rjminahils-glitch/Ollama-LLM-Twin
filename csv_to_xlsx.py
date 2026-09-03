import csv
from openpyxl import Workbook

wb = Workbook()
wb.remove(wb.active)

for name in ["knowledge", "instructions"]:
    ws = wb.create_sheet(name)
    with open(f"data/raw/{name}.csv", encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            ws.append(row)

wb.save("data/raw/NUML_data_collection_template.xlsx")
print("Wrote data/raw/NUML_data_collection_template.xlsx")