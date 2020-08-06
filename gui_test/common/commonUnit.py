from selenium import webdriver
import os,time,logging
from thrid_session.gui_test.test_plan.testcase_v６ import TestcaseX
from thrid_session.gui_test.common.set_report import Setreport

class Commonunit:
    driver=None
    deres=None
    desired_caps = {}
    sr = Setreport()
    def __init__(self):
        pass

    @classmethod
    def get_driver(cls,browser='Chrome'):
        if Commonunit.driver ==None:
            if browser=='Chrome':
                #os.path.abspath作用：用于查找文件的绝对路径
                #定位到当前文件的绝对路径
                driver_path=os.path.abspath('..')+'\\browser_api\\chromedriver.exe'
                Commonunit.driver=webdriver.Chrome(executable_path=driver_path)
            elif browser=='firefox':
                driver_path=os.path.abspath('..')+'\\browser_api\\geckodriver.exe'
                fire_path=r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
                Commonunit.driver=webdriver.Firefox(executable_path=driver_path,firefox_binary=fire_path)
            else:
                driver_path=os.path.abspath('..')+'\\browser_api\\IEDriverServer.exe'
                Commonunit.driver=webdriver.Ie(executable_path=driver_path)
        return Commonunit.driver
    # @classmethod
    # def get_appdriver(cls):
    #     if Commonunit.desired_caps=={}:
    #         Commonunit.desired_caps['platformName'] = 'Android'
    #         Commonunit.desired_caps['platformVersion'] = '4.4.2'  # 获取手机版本
    #         Commonunit.desired_caps['deviceName'] = '127.0.0.1:62001'  # 获取手机端口
    #         Commonunit.desired_caps['appPackage'] = 'com.mobivans.onestrokecharge'  # 获取包名
    #         Commonunit.desired_caps['appActivity'] = 'com.stub.stub01.Stub01'  # 程序启动app
    #         Commonunit.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', Commonunit.desired_caps)
    #     return Commonunit.driver
    # @classmethod
    # def is_element_exits(cls,how,what):
    #     try:
    #        xelement= Commonunit.driver.find_element(by=how,value=what)  #by是一个对象，名字叫By；value就是by的类型，id，class等
    #     except NoSuchElementException as e:
    #         return False,None
    #     return True,xelement

    @classmethod
    def get_nowtime(cls):
        nowtime = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        return nowtime

    @classmethod
    def wait_element_load(cls,how,what,timeout=6):
        for i in range(int(timeout)):
            try:
                xelement=Commonunit.driver.find_element(by=how,value=what)
                return True,xelement
            except:
                time.sleep(1)
        return False,None

    @classmethod
    def close_win(cls):
        Commonunit.driver.close()

    @classmethod
    def cut_screen(cls):
        filepath=os.path.abspath('..')+'\\screen\\'
        fimename=time.strftime('%Y%m%d_%H%M%S.png')
        Commonunit.driver.save_screenshot(filepath+fimename)
        return fimename


    @classmethod
    def assret_equal(cls,case,actual,excepted):
        ass=[]
        if excepted in actual :
            print('%s 测试用例成功！实际结果:%s ,预期结果:%s'%(case,actual,excepted))
            Commonunit.deres=TestcaseX()
            Commonunit.deres.result = '成功'
            Commonunit.deres.error = '无'
            Commonunit.deres.scr = '无'
            ass.append([Commonunit.deres.result,Commonunit.deres.error,Commonunit.deres.scr])
            return ass
        else:
            print('%s 测试用例失败！实际结果:%s 不等于预期结果:%s'%(case,actual,excepted))
            Commonunit.deres = TestcaseX()
            Commonunit.deres.result = '失败'
            Commonunit.deres.error = '测试用例失败'
            Commonunit.deres.scr = Commonunit.cut_screen()
            ass.append([Commonunit.deres.result, Commonunit.deres.error, Commonunit.deres.scr])
            return ass


    @classmethod
    def log_text(cls):
        logformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO,format=logformat,filename='../AppimXpath/test.log')
# if __name__ == '__main__':
#     Commonunit.get_driver('Chrome')
#     Commonunit.driver.get('http://192.168.4.199/Agileone/index.php')