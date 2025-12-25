import openpyxl as op
wb = op.load_workbook("test.xlsx")
print(wb)

ws_list = wb.sheetnames
print(ws_list)
for ws_name in ws_list:
    print(ws_name)
    ws = wb[ws_name]
    print(ws)