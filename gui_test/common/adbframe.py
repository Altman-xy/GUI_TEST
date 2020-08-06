import time
from lxml.html import etree
import os,logging


class AdbFrame:
    def __init__(self,path):
        self.path=path
        self.rep=[]

    #把手机内的文件传到电脑指定位置
    def capture(self):
        os.system('adb shell uiautomator dump')
        os.system('adb pull /sdcard/window_dump.xml %s' % self.path)
        # os.system('adb pull storage/emulated/legacy/window_dump.xml %s' % self.path)  #pull为传输

    #根据bounds属性[x1,y1][x2,y2]解析并计算中心点坐标
    def get_position(self,bounds):
        bounds=bounds.replace('[','',1)       #x1,v1][x2,v2]
        bounds=bounds.replace('][',',',1)     #x1,v1,x2,v2]
        bounds=bounds.replace(']','')     #x1,v1,x2,v2
        left_top_x=int(bounds.split(',')[0])   #['x1','v1','x2','v2']    'x1'
        left_top_y=int(bounds.split(',')[1])   #'v1'
        bottom_right_x=int(bounds.split(',')[2])
        bottom_right_y=int(bounds.split(',')[3])
        position_x=int((bottom_right_x-left_top_x)/2)+left_top_x    # (x2-x1)/2 + x1
        position_y=int((bottom_right_y-left_top_y)/2)+left_top_y    # (v2-v1)/2 + v1
        return position_x,position_y   #中心点坐标

    def find_by_xx(self,how,what):
        self.capture()
        tree = etree.parse(self.path)
        # for i in range(int(5)):
        # try:
        if how == 'id':
            nodo_list = tree.xpath("//node[@resource-id='%s']" % what)
            logging.info(('nodo', nodo_list))
        elif how == 'xpath':
            nodo_list = tree.xpath(what)
        elif how == 'text':
            nodo_list = tree.xpath("//node[@text='%s']" % what)
        elif how == 'description':
            nodo_list = tree.xpath("//node[@content-desc='%s']" % what)
        elif how == 'class name':
            nodo_list = tree.xpath("//node[@class='%s']" % what)
        bounds =nodo_list[0].get('bounds')
        x , y = self.get_position(bounds)
        return x , y
            # except:
            #     time.sleep(1)

    #获取某个节点的元素值，用于断言
    def get_value_by_xpath(self,xpath,attribute):
        self.capture()
        tree = etree.parse(self.path)
        nodo_list = tree.xpath(xpath)
        bounds = nodo_list[0].get('bounds')
        value = self.get_position(attribute)
        return value

    #查找某个元素是否存在，或多于2个元素，用于断言或判断元素
    def check_exist_by_xx(self,how,what):
        self.capture()
        tree = etree.parse(self.path)
        if how == 'xpath':
            nodo_list = tree.xpath(what)
            logging.info(('aaa',nodo_list))
        elif how == 'id':
            nodo_list = tree.xpath("//node[@resource-id='%s']" % what)
        if len(nodo_list) == 0  :   #or len(nodo_list) > 1
            # raise Exception（'元素不存在或找到多个！'）  #也可以使用抛出异常的方式
            return None
        else:
            return nodo_list[0].get('text')

    def app_cutscreen(self):
        nowtime=time.strftime('%Y%m%d_%H%M%S')
        filename=str(nowtime) + '.png'
        # print(filename)
        os.system('adb shell /system/bin/screencap -p /sdcard/%s'%(filename))
        os.system('adb pull /sdcard/%s ../gui_test/screen'%(filename))
        return filename

# if __name__ == '__main__':
#     woniu=AdbFrame('E:\ADBF\window_dump.xml')
#     woniu.capture()
#     # x,y=woniu.find_by_xx('id','com.miui.calculator:id/btn_7',4)
#     x,y=woniu.find_by_xx('text','记一笔',5)
#     print(woniu.check_exist_by_xx("//node[@text='记一笔']"))
#     print(x,y)
