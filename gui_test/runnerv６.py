import sys
from thrid_session.gui_test.test_plan.test_planv６ import TestPlan


class Runnerv3:
    def __init__(self):
        pass
    def runner(self,filename,filename1,sheetname):
        tp = TestPlan(filename,filename1,sheetname)
        tp.run_plan(tp.get_planid())



if __name__ == '__main__':
    rn=Runnerv3()
    rn.runner('../test_plan/testcasev6.xlsx','../test_plan/text_planv6.xlsx','Web')
    rn.runner('./test_plan/testcasev6.xlsx', './test_plan/text_planv6.xlsx', 'App')