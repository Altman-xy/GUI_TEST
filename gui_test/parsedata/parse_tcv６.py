from thrid_session.gui_test.parsedata.datadealｖ６ import Readexcel
from thrid_session.gui_test.test_plan.testcase_v６ import TestcaseX


class ParseTc:
    def __init__(self,filename,sheet_name):   #初始化表，默认页='adduserstory'
        self.parsexls=Readexcel(filename)
        self.sheet=self.parsexls.gettable(sheet_name)
        self.tc=None

    def parseData(self):
        tmplist=[]
        for i in range( 1 ,self.parsexls.getrow()):  #遍历表格每行内容
            flag=False
            rowdata=self.parsexls.getrowData(i)
            if 'testcase' in str(rowdata[0]):   #如果每行首格含有testcase，把相对应的内容放入用例库中
                self.tc=TestcaseX()
                self.tc.tcid=rowdata[0]
                self.tc.tcname=rowdata[1]
                self.tc.predo.append(rowdata[2])
                flag=True
            elif len(str(rowdata[0])) > 0 and len(str(rowdata[0])) <= 4:   #如果每行首格长度小于等于4位则认为该行内容为执行步骤，同样加入到列表中放入用例库
                self.tc.step.append([rowdata[1],rowdata[2],rowdata[3],rowdata[4]])
            if flag:
                tmplist.append(self.tc)
        return tmplist


if __name__ == '__main__':
    pa=ParseTc('testcasev6.xlsx','Web')
    pa.parseData()
    # print(op)
    # for one in pa.parseData():
    #     # print(one.tcid)
    #     print(one)