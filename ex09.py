import openpyxl as op
wb = op.load_workbook("test.xlsx")
ws = wb["업"]
for row_rng in ws.rows:
    print(row_rng)

for col_rng in ws.columns:
    print(col_rng)

for row_rng in ws.rows:
    for cell in row_rng:
        print(cell.value, end=" ")
    print()