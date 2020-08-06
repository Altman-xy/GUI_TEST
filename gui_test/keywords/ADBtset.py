import time,os
from thrid_session.gui_test.common.adbframe import AdbFrame
from thrid_session.gui_test.common.set_report import Setreport
import logging


class AdbTest:
    # udid='127.0.0.1:5037'
    udid='28PNW18227003305'
    adb=AdbFrame('E:\ADBF\window_dump.xml')
    sr1 = Setreport()

    def __init__(self):
        pass

    # def click_by_id(self,id):
    #     x,y=self.adb.find_by_id(id)
    #     print('根据id值:%s,找到对应的坐标位置：[%d,%d]'%(id,x,y))
    #     os.system('adb -s %s shell input tap %d %d '%(self.udid,x,y))
    #
    # def click_by_xpath(self,xpath):
    #     x,y=self.adb.find_by_xpath(xpath)
    #     print(x,y)
    #     os.system('adb -s %s shell input tap %d %d '%(self.udid,x,y))
    @classmethod
    def click_xx(cls,planid,tc,tem):
        try:
            logging.info(('tem',tem))
            x,y=AdbTest.adb.find_by_xx(tem[1],tem[2])
            print('根据定位元素:%s,找到对应的坐标位置：[%d,%d],并点击' % (tem[1], x, y))
            os.system('adb -s %s shell input tap %d %d ' % (AdbTest.udid, x, y))
        except Exception as e:
            AdbTest.sr1.write_report('App', planid, 'GUI', tc.tcid, tc.tcname, '错误',"'%s'"%(e), AdbTest.adb.app_cutscreen())

    @classmethod
    def input_xx(cls,planid,tc,tem):
        try:
            x, y = AdbTest.adb.find_by_xx(tem[1],tem[2])
            print('根据定位元素:%s,找到对应的坐标位置：[%d,%d],并输入值。' % (tem[1], x, y))
            os.system('adb -s %s shell input tap %d %d ' % (AdbTest.udid, x, y))
            os.system("adb shell am broadcast -a ADB_INPUT_TEXT --es msg '%s' " % (tem[3]))
        except Exception as e:
            AdbTest.sr1.write_report('App', planid, 'GUI', tc.tcid, tc.tcname, '错误',"'%s'"%(e), AdbTest.adb.app_cutscreen())

    @classmethod
    def start_app(cls,planid,tc,tem):
        try:
            os.system('adb shell am start -n %s/%s' % (tem[3].split(',')[0], tem[3].split(',')[1]))
            print('已经重新启动应用程序：%s' % tem[3].split(',')[0])
        except Exception as e:
            AdbTest.sr1.write_report('App', planid, 'GUI', tc.tcid, tc.tcname, '错误', "'%s'"%(e),
                                 AdbTest.adb.app_cutscreen())


    @classmethod
    def decide_app(cls,planid, tc,tem):
        if len(tem[2].split(',')) >= 2 and len(tem[3].split(',')) >= 2:   #如果有两个以上判断条件
            whats=tem[2].split(',')
            values=tem[3].split(',')
            #判断两个断言结果是否相等
            if AdbTest.adb.check_exist_by_xx(tem[1],whats[0]) == values[0] and AdbTest.adb.check_exist_by_xx(tem[1],whats[1]) == values[1]:
                logging.info(('tcid', tc.tcid))
                AdbTest.sr1.write_report('App', planid, 'GUI', tc.tcid, tc.tcname, '成功', '无', '无')
                print('测试用例执行成功,用例编号：%s,用例名称：%s,实际结果：%s与预期结果%s一致' % (tc.tcid, tc.tcname,
                [str(AdbTest.adb.check_exist_by_xx(tem[1],whats[0])),str(AdbTest.adb.check_exist_by_xx(tem[1],whats[1]))],
                                                                     values))
            else:  #断言失败
                logging.info(('tcid', tc.tcid))
                AdbTest.sr1.write_report('App',planid,'GUI',tc.tcid,tc.tcname,'失败','断言失败',
                                         AdbTest.adb.app_cutscreen())
                print('测试用例%s执行失败,实际结果：%s与预期结果%s不一致' % (tc.tcid,
                [str(AdbTest.adb.check_exist_by_xx(tem[1],whats[0])),str(AdbTest.adb.check_exist_by_xx(tem[1],whats[1]))], values))

        #what，value只有一个
        elif len(tem[2].split(',')) == 1 and len(str(tem[3]).split(',')) == 1 :
            logging.info(('tem',tem[2],tem[3]))
            if AdbTest.adb.check_exist_by_xx(tem[1],tem[2]) == tem[3]:
                print("测试用例执行成功,用例编号：'%s',用例名称：'%s',实际结果：'%s'与预期结果: '%s'一致" % (tc.tcid, tc.tcname,
                                                                               AdbTest.adb.check_exist_by_xx(tem[1],tem[2]), tem[3]))
                logging.info(('tcid', tc.tcid))
                AdbTest.sr1.write_report('App', planid, 'GUI', tc.tcid, tc.tcname, '成功', '无', '无')
            else:
                print("测试用例'%s'执行失败,实际结果：'%s'与预期结果 :'%s'不一致" % (tc.tcid,
                                                                AdbTest.adb.check_exist_by_xx(tem[1],tem[2]), tem[3]))
                logging.info(('tcid', tc.tcid))
                AdbTest.sr1.write_report('App',planid, 'GUI', tc.tcid, tc.tcname, '失败', '断言失败',
                                         AdbTest.adb.app_cutscreen())
        else:
            print('断言内容有误，请检查')
        # if AdbTest.adb.check_exist_by_xpath(tem[2]) == tem[3]:
        #     logging.info(('tcid',tc.tcid))
        #     AdbTest.sr1.write_report('2',tc.tcid , 'GUI', tc.tcid, tc.tcname, '成功', '无', '无')
        #     # print('测试用例执行成功,用例编号：%s,用例名称：%s,实际结果：%s等于预期结果: %s' % (tc.tcid, tc.tcname, tem[2], tem[3]))
        #     print('123')
        # else:
        #     print('nononon')

    @classmethod
    def sleep(cls,planid,tc,tem):
        time.sleep(tem[3])

    @classmethod
    def stop_app(cls,planid,tc,tem):
        os.system('adb shell am force-stop %s' % (tem[3].split(',')[0]))
        print('已经关闭该应用程序：%s' % tem[3].split(',')[0])

    @classmethod
    def click_act(cls,planid,tc,tem):
        os.system("adb shell input keyevent'%s'" % (int(tem[3])))

    @classmethod
    def long_touch(cls,planid,tc,tem):
        x, y = AdbTest.adb.find_by_xx(tem[1], tem[2])
        os.system("adb shell input swipe '%d' '%d' '%d' '%d' 1000 " % (x,y,x,y))

    @classmethod
    def swpie(cls,planid,tc,tem):
        os.system("adb shell input swipe 405 1451 405 674 2000")

# if __name__ == '__main__':
    # testx=AdbTest('127.0.0.1:62001','E:\ADBF\window_dump.xml')
    # AdbTest.start_app('com.mobivans.onestrokecharge','com.stub.stub01.Stub01')
    # testx.click_by_xpath("//node[@text='记一笔']")
    # testx.click_xx('xpath',"//node[@text='记一笔']")
    # time.sleep(2)
    # testx.click_by_xpath("//node[@text='彩票']")
    # time.sleep(2)
    # testx.click_by_id("com.mobivans.onestrokecharge:id/keyb_btn_6")
    # testx.click_by_id("com.mobivans.onestrokecharge:id/keyb_btn_finish")
    # if testx.adb.check_exist_by_xpath("//*[@text='一笔记账']"):
    #     print('操作成功')
    # # else:
    #     print('失败')
    # testx.decide_app("//*[@text='一笔记账']")
    # textx=AdbTest( '127.0.0.1:62001','E:\ADBF\window_dump.xml')
    # AdbTest.start_app(['','','','com.mobivans.onestrokecharge,com.stub.stub01.Stub01'])
    # AdbTest.click_xx(['','xpath',"//node[@text='记一笔']"])

