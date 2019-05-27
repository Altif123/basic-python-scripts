import xlrd
workbook = xlrd.open_workbook('APD grades.xls')
worksheet = workbook.sheet_by_index(0)
print(worksheet.nrows)
print(worksheet.ncols)
print('total: ' + str(worksheet.cell_value(21, 7)))
print(worksheet.cell_value(21, 7))
