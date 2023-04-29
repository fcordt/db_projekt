import xlrd

book = xlrd.open_workbook("data/plz_list.xls")
sh = book.sheet_by_index(0)
with open('sql/V3.1__insert_ort.sql', 'w') as file:
    for rx in range(1, sh.nrows):
        file.write(f"INSERT INTO DBUSER.ORT(PLZ, NAME) VALUES ('{sh.cell_value(rx, 0)}', '{sh.cell_value(rx, 1)}');\n")
