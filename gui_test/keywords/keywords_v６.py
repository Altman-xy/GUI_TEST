import time
from thrid_session.gui_test.common.set_report import Setreport
from thrid_session.gui_test.common.commonUnit import Commonunit
from selenium.webdriver.support.ui import Select


class XTestcase:
    # driver=webdriver.Chrome()
    sr1=Setreport()
    def __init__(self):
        pass

    @classmethod
    def input_text(cls,planid,one,dr,tem):
        try:
            Commonunit.wait_element_load(tem[1],tem[2])[1].send_keys(tem[3])
        except Exception as e:
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, '错误',"'%s'"%(e), Commonunit.cut_screen() )


    @classmethod
    def button_click(cls,planid,one,dr,tem):
        try:
            Commonunit.wait_element_load(tem[1],tem[2])[1].click()
        except Exception as e:
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname,'错误', "'%s'"%(e), Commonunit.cut_screen())


    @classmethod
    def select_click(cls,planid,one,dr,tem):
        try:
            Select(Commonunit.wait_element_load(tem[1],tem[2])[1]).select_by_value(tem[3])
        except Exception as e:
            print(e)
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, '错误',"'%s'"%(e), Commonunit.cut_screen() )

    @classmethod
    def swin_ifram(cls,planid,one,dr,tem):
        try:
            dr.switch_to.frame(Commonunit.wait_element_load(tem[1],tem[2])[1])
        except Exception as e:
            print(e)
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, '错误',"'%s'"%(e), Commonunit.cut_screen() )

    @classmethod
    def swout_ifram(cls,planid,one,dr,tem):
        try:
            dr.switch_to_default_content()
        except Exception as e:
            print(e)
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, '错误',"'%s'"%(e), Commonunit.cut_screen() )

    @classmethod
    def getres(cls,planid,one,dr,tem):
        try:
            exist,ele=Commonunit.wait_element_load(tem[1],tem[2])
            if exist:
                return ele.text
            else:
                return None
        except Exception as e:
            print(e)
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, '错误',"'%s'"%(e), Commonunit.cut_screen() )

    @classmethod
    def open_url(cls,planid,one,dr,tem):
        try:
            dr.get(tem[3])
        except Exception as e:
            print(e)
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, '错误',"'%s'"%(e), Commonunit.cut_screen() )

    @classmethod
    def closeit(cls,planid,one,dr,tem):
        try:
            Commonunit.close_win()
        except Exception as e:
            print(e)
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, '错误',"'%s'"%(e), Commonunit.cut_screen() )

    @classmethod
    def decide(cls,planid,one,dr,tem):
        try:
            comm=Commonunit.wait_element_load(tem[1],tem[2])[1].text
            # Commonunit.assret_equal(one.tcid,comm,tem[3])
            sr=Commonunit.assret_equal(one.tcid,comm,tem[3])
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, sr[0][0], sr[0][1], sr[0][2])
            # print(sr)
        except Exception as e:
            print(e)
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, '错误',"'%s'"%(e), Commonunit.cut_screen() )


    @classmethod
    def sleep(cls,planid,one,dr,tem):
        try:
            time.sleep(int(tem[3]))
        except Exception as e:
            print(e)
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, '错误',"'%s'"%(e), Commonunit.cut_screen() )

    @classmethod
    def sw_alert(cls,planid,one,dr,tem):

        res=dr.switch_to.alert
        if tem[3] == '确定':
            res.accept()
        elif tem[3] == '取消':
            res.dismiss()

    @classmethod
    def clear_text(cls,planid,one,dr,tem):
        try:
            Commonunit.wait_element_load(tem[1],tem[2])[1].clear()
        except Exception as e:
            XTestcase.sr1.write_report('Web', planid, 'GUI', one.tcid, one.tcname, '错误',"%s"%(e), Commonunit.cut_screen() )


