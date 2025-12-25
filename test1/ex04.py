import openpyxl as op
wb = op.load_workbook("test.xlsx")
print(wb)
ws = wb.active
num = 1
for col in range(1, 4):
    for row in range(1, 4):
        ws.cell(row=row, column=col, value=num)
        num +=1
wb.save("test.xlsx")
    