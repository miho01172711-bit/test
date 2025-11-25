import openpyxl as op
wb = op.load_workbook("test.xlsx")
ws = wb.active
wb.remove(ws)

wb.save("delete_result.xlsx")        