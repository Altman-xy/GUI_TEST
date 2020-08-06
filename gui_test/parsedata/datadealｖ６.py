import xlrd

class Readexcel:

    def __init__(self,filename):
        self.filename=filename
        self.book=xlrd.open_workbook(self.filename)

    def gettable(self,sheetname='adduserstory'):
        self.table=self.book.sheet_by_name(sheetname)

    def getrow(self):
        return self.table.nrows

    def getrowData(self,rowx=0):
        return self.table.row_values(rowx)


# if __name__ == '__main__':
#     ts=Readexcel('testcase_v4.xls')
#     ts.gettable()
#     print(ts.getrow())




