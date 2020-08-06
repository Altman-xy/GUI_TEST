from __future__ import unicode_literals
from requests import get,post
from platform import system
from os import chdir
from random import choice
from threading import Thread
import configparser,time,sys
from wxpy import *




#获取名言
def get_message():
    r=get('http://open.iciba.com/dsapi/')
    note = r.json()['note']
    content = r.json()['content']
    return note,content

#发消息给朋友
def send_message(your_message):
    try:
        my_friend = bot.friends().search(my_lady_wechat_name)[0]    #配置文件中的微信名称
        my_friend.send(your_message)     #发信息给对方
    except:
        bot.file_helper.send(u"守护女友出问题了，赶紧去看看咋回事~")  #出现问题，发消息到信息助手

#在规定时间发送信息
def start_care():
    #待发送的信息，预设为空
    message = ''

    #24小时在线，发送信息
    while True:
        #在线提示
        print('守护中，时间：%s'%time.ctime())

        #每天定时问候，早上起床，中午吃饭，晚上吃饭，睡觉
        #获取时间，只获取时和分，对应的位置为倒数第13位到倒数第6位
        now_time = time.ctime()[-13:-8]
        if now_time == say_good_morning :
            #随机抽取一句问候语
            message = choice(str_list_good_morning)

            #是否加上随机表情
            if flag_wx_emoj :
                message = message + choice(str_list_emoj)

            send_message(message)  #发送信息
            print('提醒起床：%s'%time.ctime())

        elif now_time == say_good_lunch :
            message = choice(str_list_good_lunch)

            # 是否加上随机表情
            if flag_wx_emoj:
                message = message + choice(str_list_emoj)

            send_message(message)  # 发送信息
            print('提醒吃午饭：%s' % time.ctime())

        elif now_time == say_good_dinner :
            message = choice(str_list_good_dinner)

            # 是否加上随机表情
            if flag_wx_emoj:
                message = message + choice(str_list_emoj)

            send_message(message)  # 发送信息
            print('提醒吃晚饭：%s' % time.ctime())

        elif now_time == say_good_dream :

            #是否在结尾加上每日学英语
            if flag_learn_english :
                note , content = get_message()
                message = choice( str_list_good_dream ) + '\n\n' + '一起来学英语吧：\n' + '原文：' + content + '\n\n翻译：' + note
            else:
                message = choice(str_list_good_dream)

            # 是否加上随机表情
            if flag_wx_emoj:
                message = message + choice(str_list_emoj)

            send_message(message)  # 发送信息
            print('提醒睡觉：%s' % time.ctime())

        #节日问候语
        festival_month = time.strftime('%m',time.localtime())
        festival_day = time.strftime('%d',time.localtime())

        if festival_month == '02' and festival_day == '14' and now_time == '00:00' :
            send_message(str_Valentine)
            print('发送情人节祝福：%s'% time.ctime())

        elif festival_month == '03' and festival_day == '08' and now_time == '00:00' :
            send_message(str_Women)
            print('发送妇女节祝福：%s'% time.ctime())

        elif festival_month == '12' and festival_day == '24' and now_time == '00:00' :
            send_message(str_Christmas_Eve)
            print('发送平安夜祝福：%s'% time.ctime())

        elif festival_month == '12' and festival_day == '25' and now_time == '00:00' :
            send_message(str_Christmas)
            print('发送圣诞节祝福：%s'% time.ctime())

        elif festival_month == birthday_month and festival_day == birthday_day and now_time == '00:00' :
            send_message(str_birthday)
            print('发送生日祝福：%s'% time.ctime())


        #60秒检测一次
        time.sleep(60)

if __name__ == '__main__':
    # 启动微信机器人，自动根据操作系统执行不同的指令
    # windows系统或macOS Sierra系统使用bot = Bot()
    # linux系统或macOS Terminal系统使用bot = Bot(console_qr=2)
    if 'Windows' in system() :
        bot = Bot()

    elif 'Darwin' in system() :  #Mac
        bot = Bot()

    elif 'Linux' in system() :
        bot = Bot(console_qr=2,cache_path=True)

    else:
        print('未知的操作系统，请自己设置')

    #读取配置文件
    cf = configparser.ConfigParser()
    cf.read('./config.ini',encoding='UTF-8')

    #设置对方微信名称
    my_lady_wechat_name = cf.get('configuration','my_lady_wechat_name')

    #设置起床、午饭、晚饭、睡觉时间
    say_good_morning = cf.get("configuration", "say_good_morning")
    say_good_lunch = cf.get("configuration", "say_good_lunch")
    say_good_dinner = cf.get("configuration", "say_good_dinner")
    say_good_dream = cf.get("configuration", "say_good_dream")

    #设置生日时间
    birthday_month = cf.get("configuration", "birthday_month")
    birthday_day = cf.get("configuration", "birthday_day")

    # 读取早上起床时间，中午吃饭时间，下午吃饭时间，晚上睡觉时间的随机提示语
    # 一般这里的代码不要改动，需要增加提示语可以自己打开对应的文件修改
    #起床问候
    str_list_good_morning = ''
    with open('./remind_sentence/sentence_good_morning.txt', "r",encoding='UTF-8') as f :
        str_list_good_morning = f.readlines()
    print(str_list_good_morning)

    #午饭问候
    str_list_good_lunch = ''
    with open("./remind_sentence/sentence_good_lunch.txt", "r", encoding='UTF-8') as f:
        str_list_good_lunch = f.readlines()
    print(str_list_good_lunch)

    #晚饭问候
    str_list_good_dinner = ''
    with open("./remind_sentence/sentence_good_dinner.txt", "r", encoding='UTF-8') as f:
        str_list_good_dinner = f.readlines()
    print(str_list_good_dinner)

    #睡觉问候
    str_list_good_dream = ''
    with open("./remind_sentence/sentence_good_dream.txt", "r", encoding='UTF-8') as f:
        str_list_good_dream = f.readlines()
    print(str_list_good_dream)

    # 设置晚上睡觉问候语是否在原来的基础上再加上每日学英语精句
    if cf.get('configuration','flag_learn_english') == '1' :
        flag_learn_english = True

    else:
        flag_learn_english = False

    print(flag_learn_english)

    # 设置问候语是否加上表情
    str_emoj = "(•‾̑⌣‾̑•)✧˖°----(๑´ڡ`๑)----(๑¯ิε ¯ิ๑)----(๑•́ ₃ •̀๑)----( ∙̆ .̯ ∙̆ )----(๑˘ ˘๑)----(●′ω`●)----(●･̆⍛･̆●)" \
               "----ಥ_ಥ----_(:qゝ∠)----(´；ω；`)----( `)3')----Σ((( つ•̀ω•́)つ----╰(*´︶`*)╯----( ´´ิ∀´ิ` )----(´∩｀。)----" \
               "( ื▿ ื)----(｡ŏ_ŏ)----( •ิ _ •ิ )----ヽ(*΄◞ิ౪◟ิ‵ *)----( ˘ ³˘)----(; ´_ゝ`)----(*ˉ﹃ˉ)----(◍'౪`◍)ﾉﾞ----(｡◝‿◜｡)" \
               "----(ಠ .̫.̫ ಠ)----(´◞⊖◟`)----(。≖ˇェˇ≖｡)----(◕ܫ◕)----(｀◕‸◕´+)----(▼ _ ▼)----( ◉ืൠ◉ื)----ㄟ(◑‿◐ )ㄏ----" \
               "(●'◡'●)ﾉ♥----(｡◕ˇ∀ˇ◕）----( ◔ ڼ ◔ )----( ´◔ ‸◔`)----(☍﹏⁰)----(♥◠‿◠)----ლ(╹◡╹ლ )----(๑꒪◞౪◟꒪๑)"
    str_list_emoj = str_emoj.split('----')
    if cf.get('configuration','flag_wx_emoj') == '1' :
        flag_wx_emoj = True

    else:
        flag_wx_emoj = False

    print(flag_wx_emoj)

    # 设置节日祝福语
    # 情人节祝福语
    str_Valentine = cf.get("configuration", "str_Valentine")
    print(str_Valentine)

    # 三八妇女节祝福语
    str_Women = cf.get("configuration", "str_Women")
    print(str_Women)

    # 平安夜祝福语
    str_Christmas_Eve = cf.get("configuration", "str_Christmas_Eve")
    print(str_Christmas_Eve)

    # 圣诞节祝福语
    str_Christmas = cf.get("configuration", "str_Christmas")
    print(str_Christmas)

    # 生日的时候的祝福语
    str_birthday = cf.get("configuration", "str_birthday")
    print(str_birthday)

    # 开始守护
    t = Thread(target=start_care,name='start_care')
    t.start()

# 接受信息监听器
my_girl_friend = bot.friends().search(my_lady_wechat_name)[0]

@bot.register(chats=my_girl_friend,except_self=False)
def print_others(msg):

    #输出聊天记录
    print(msg.text)

    # 做极其简单的情感分析
    # 结果仅供参考，请勿完全相信
    postData = {'data':msg.text}
    response = post('https://bosonnlp.com/analysis/sentiment?analysisType=',data=postData)
    data = response.text

    #情感评分指数（越接近1代表心情越好，反之越差）
    now_mod_rank = (data.split(',')[0].replace('[[',''))
    print('来自对方的信息：%s\n当前情感得分：%s\n越接近1表示心情越好，越接近0表示心情越差，情感结果仅供参考，请勿完全相信！\n\n'%(msg.text,now_mod_rank))

    #发送信息到文件传输助手
    mood_message = u'来自对方的信息：' + msg.text + "\n当前情感得分:" + now_mod_rank + "\n越接近1表示心情越好，越接近0表示心情越差，情感结果仅供参考，请勿完全相信！\n\n"
    bot.file_helper.send(mood_message)