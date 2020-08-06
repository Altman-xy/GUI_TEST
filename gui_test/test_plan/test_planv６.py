import sys
sys.path.append('E:\python1\venv\Lib\site-packages')
import xlrd,os,logging
from thrid_session.gui_test.keywords.keywords_v６ import XTestcase
from thrid_session.gui_test.keywords.ADBtset import AdbTest
from thrid_session.gui_test.common.set_report import Setreport
from thrid_session.gui_test.common.commonUnit import Commonunit
from thrid_session.gui_test.parsedata.parse_tcv６ import ParseTc


class TestPlan:

    def __init__(self,filename,filename1,sheetname):
        self.stname=sheetname
        self.parsev4=ParseTc(filename,self.stname)        #读取测试用例表
        self.book=xlrd.open_workbook(filename1)    #打开测试计划表
        self.table = self.book.sheet_by_name(self.stname)   #设定打开的表页
        self.sr=Setreport()
        self.planid=''
        self.tc=None

    # 读取计划表，把用到的数据放进测试计划列表中
    def get_planid(self):
        planid=[]
        for i in range(2,self.table.nrows):    #循环列表行数
            rowdata=self.table.row_values(i)
            if 'testcase' in str(rowdata[3]):  #在每行的第四列寻找 含有‘testcase’的数据，找到就放入列表
                planid.append([rowdata[2],rowdata[3],rowdata[4]])
        return planid

    def get_prestep(self,tcsid):  #根据输入的前置用例编号获取前置用例步骤
        pres=[]
        for tc in self.parsev4.parseData():
            self.tc=tc   #给初始化的tc赋值
            for ele in self.tc.step:    #遍历步骤
                if self.tc.tcid==tcsid and 'decide' not in ele[0]:    #找出步骤中的断言步骤并移除
                    pres.append(ele)
        if pres:     #判断列表是否为空，空说明该用例不存在，没有操作步骤
            self.run_prestep(pres)
            print('前置用例：%s执行成功！' % (tcsid))
        else:
            print('前置用例不存在！')
            self.sr.write_report(self.stname,self.planid[0],'GUI',self.planid[1],'None','错误','前置用例%s不存在！'%(self.planid[2]),'请检查用例库')
            return False


    def run_one(self,tcsid):   #执行正式用例
        for tc in self.parsev4.parseData():  #遍历用例库，如果用例编号等于输入的用例编号则运行用例
            if tc.tcid==tcsid :
                print('开始测试用例，用例编号为：%s,用例名字为：%s' % (tc.tcid, tc.tcname))
                self.run_step(tc)
                return True
        else:    #如果传入的用例编号没找到则说明用例不存在
            self.sr.write_report(self.stname,self.planid[0],'GUI',self.planid[1],'None','错误','用例%s不存在！'%(self.planid[2]),'请检查用例库')
            return False


    def run_prestep(self,pres):   #执行前置用例的步骤
        for one in pres:
            if self.stname=='App':     #根据输入的页名决定执行的方法
                if hasattr(AdbTest, one[0]):
                    getattr(AdbTest, one[0])(self.planid[0],self.tc,one)
            else:
                dr = Commonunit.get_driver()
                if hasattr(XTestcase,one[0]):
                    getattr(XTestcase,one[0])(self.planid[0],self.tc,dr,one)

    def run_step(self,tc):   #运行用例
        for ele in tc.step:     #遍历用例步骤，根据页名执行对应的操作
            if self.stname=='App':
                logging.info(('tcid',tc.tcid))
                if hasattr(AdbTest, ele[0]):
                    getattr(AdbTest, ele[0])(self.planid[0],tc,ele)
            else:
                dr = Commonunit.get_driver()
                if hasattr(XTestcase, ele[0]):
                    getattr(XTestcase, ele[0])(self.planid[0],tc, dr, ele)

    #plan:[[plan001,testcase001,testcase002],.....]
    def run_plan(self,plan):   #执行测试计划
        logging.info(('plan',plan))
        if plan == [] or self.parsev4.parseData() == []:   #如果测试计划表的正式用例为空或用例表为空，则不执行下面
            print('用例库为空或计划表为空！')
            self.sr.write_report(self.stname,'None','GUI','None','None','错误','没有找到用例！','请检查用例库')
        else:
            for planid in plan:    #遍历测试计划表
                self.planid = planid
                logging.info(('planid=',self.planid))
                flag=False
                if self.planid[2] != ''and len(self.planid[2].split(',')) >= 1 :    #如果有一个以上的前置用例，全部执行完
                    for ele in planid[2].split(','):
                        print('正在执行前置用例：%s' %(ele))
                        if self.get_prestep(ele) == False:   #如果为false，说明用例步骤为空，即用例不存在
                            flag = True
                if self.stname == 'Web' and flag == False and self.run_one(self.planid[1]):   #判断是什么端的测试，前置用例与正式用例是否存在
                    try:
                        Commonunit.wait_element_load('id', 'username')[1].clear()
                        Commonunit.wait_element_load('id', 'password')[1].clear()
                        Commonunit.get_driver().delete_all_cookies()
                    except:
                        Commonunit.wait_element_load('link text', '注销')[1].click()    #每次执行完用例进行注销
                        Commonunit.get_driver().delete_all_cookies()
                elif self.stname == 'App' and flag == False and self.run_one(self.planid[1]):
                    print('用例执行完成，正在关闭应用程序')
                    os.system('adb shell am force-stop %s' %('com.mobivans.onestrokecharge'))
                else:
                    print('用例不存在或出现异常！')
        self.sr.read_report(self.stname)





if __name__ == '__main__':
    Commonunit.log_text()
    tp=TestPlan('testcasev6.xlsx','text_planv6.xlsx','Web')
    tp.run_plan(tp.get_planid())
    # print(tp.get_prodo())
    # tp.get_prestep('testcase0020')
    # print(tp.get_planid())