import openpyxl as op
wb = op.load_workbook("test.xlsx")
ws = wb["업"]
ws["A4"].value = "=SUM(A1:A3)"
wb.save("result.xlsx")