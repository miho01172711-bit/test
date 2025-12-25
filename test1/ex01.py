import openpyxl as op
wb = op.Workbook()
print(wb)
wb.save("openpyxl_test.xlsx")

wb = op.load_workbook("openpyxl_test.xlsx")
print(wb)