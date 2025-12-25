import openpyxl as op
wb = op.load_workbook("test.xlsx")
ws = wb.active
rng = ws["A1:C3"]
print(rng)
for row_data in rng:
    for data in row_data:
        if(data.value % 2 == 0):
            data.value=" "
wb.save("delete_result.xlsx")        