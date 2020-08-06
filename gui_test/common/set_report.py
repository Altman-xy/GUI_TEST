import os
import time
from thrid_session.gui_test.common.connect_DB import DBtools


class Setreport:
    def __init__(self):
        self.db=DBtools()

    def write_report(self,version,planid,testtype,caseid,casetitle,result,error,screenshot):
        testtime=time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))
        args=(version,planid,testtype,caseid,casetitle,
                  result,testtime,error,screenshot)
        sql_write="insert into report(version,planid,testtype,caseid,casetitle,result,testtime,error,screenshot)" \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # print(sql_write)
        self.db.cursor.execute(sql_write,args)
        self.db.db.commit()
        # self.db.cursor.close()
        # self.db.db.close()


    def read_report(self,version):
        sql_all="select * from report where version = '%s'"%(version)
        self.db.cursor.execute(sql_all)
        results=self.db.cursor.fetchall()   #返回全部数据，一个二维列表
        if len(results)==0:
            print('提示：本次测试没有测试结果产生')
            return
        #打开模板文件并读取内容，定位到当前文件的绝对路径
        tempate_path=os.path.abspath('..')+'\\gui_test\\main\\HTML_report.html'
        tempate=open(tempate_path,mode='r',encoding='utf-8')
        content=tempate.read()
      #获取版本信息并替换模板变量
        version=results[0][1]
        content=content.replace('$test-version',version)

        #输入SQL语句获取用例数量
        sql_base="select count(*) from report where version = "

        #统计成功数量并替换模板变量
        sql_pass=sql_base + "'%s' and result='成功'" %(version)
        self.db.cursor.execute(sql_pass)
        pass_count=self.db.cursor.fetchone()[0]    #fetchone返回元组
        content=content.replace('$pass-count',str(pass_count))

        #统计失败数量并替换模板变量
        sql_fail=sql_base + "'%s' and result = '失败'" %(version)
        self.db.cursor.execute(sql_fail)
        fail_count=self.db.cursor.fetchone()[0]
        content=content.replace('$fail-count',str(fail_count))
        #统计错误数量并替换模板变量
        sql_error=sql_base + "'%s' and result = '错误'"%(version)
        self.db.cursor.execute(sql_error)
        error_count=self.db.cursor.fetchone()[0]
        content=content.replace('$error-count',str(error_count))

        #取得最后一个用例的执行时间并替换模板变量
        sql_last_time="select testtime from report where version = '%s' order by id desc limit 0,1"%(version)
        self.db.cursor.execute(sql_last_time)
        last_time=self.db.cursor.fetchone()[0]
        content=content.replace('$last-time',str(last_time))
        content=content.replace('$test-date',str(last_time))

        #取得所有执行结果数据并替换掉变量模板的$result
        test_result=''

        #循环遍历每一条结果记录，并最终生成HTML源码
        for record in results:   #results是二维元组
            test_result+="<tr height='40'>"
            test_result+="<td width='7%'>" + str(record[0]) + "</td>"     #报告编号record[0]第一列
            test_result += "<td width='9%'>" + record[2] + "</td>"        #计划编号record[2]的第三列
            test_result += "<td width='9%'>" + record[3] + "</td>"       #测试类型record[3]的第四列
            test_result += "<td width='7%'>" + record[4] + "</td>"        #用例编号record[4]的第五列
            test_result += "<td width='20%'>" + record[5] + "</td>"       #用例描述record[5]的第六列

            #根据不同测试结果生成不同颜色
            if record[6]=='成功':
                test_result += "<td width='7%' bgcolor='#A6FFA6'>" + record[6] + "</td>"
            elif record[6]=='失败':
                test_result += "<td width='7%' bgcolor='#FF9797'>" + record[6] + "</td>"
            elif record[6]=='错误':
                test_result += "<td width='7%' bgcolor='#FFED97'>" + record[6] + "</td>"
            test_result+="<td width='16%'>" + str(record[7]) + "</td>"     #执行时间record[7]第一列
            test_result += "<td width='15%'>" + record[8] + "</td>"        #错误信息record[8]的第一列
            if record[9]=='无' or record[9] == '请检查用例库':     #现场截图record[9]第一列
                test_result += "<td width='10%'>" + record[9] + "</td>"
            else:
                test_result += "<td width='10%'><a href='" + record[9] + "'>查看截图</a></td>"
            test_result+="</tr>\r\n"
        content=content.replace('$test-result',test_result)

        #将最终测试结果报告写入目录的文件中
        nowtime=time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
        report_path=os.path.abspath('..')+'\\gui_test\\screen\\'+nowtime+'_report.html'
        report=open(report_path,mode='w',encoding='utf-8')
        report.write(content)

        #关闭相关的文件和数据库连接
        report.close()
        self.db.cursor.close()
        self.db.db.close()


if __name__ == '__main__':
    tctest=Setreport()
    tctest.write_report('pc端','None','GUI','None','None','错误','找不到用例','无')
    # tctest.read_report('1.01')
    tctest.read_report('pc端')





















