__author__ = 'Konrad Kopciuch'

import xlrd

class NDBResultParser:

    @staticmethod
    def get_pdb_ids(path):
        with xlrd.open_workbook(path) as workbook:
            sheet = workbook.sheet_by_index(0)
            for row_id in range(1,sheet.nrows,1): #pomijamy pierwszy wiersz z opisem kolumn
                pdb_id = sheet.cell_value(row_id, 1)
                if pdb_id:
                    yield pdb_id
