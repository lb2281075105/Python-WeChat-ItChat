#coding=utf-8
# itchat监听指定微信公众号发送的文章

import itchat
# import全部消息类型
from itchat.content import *

# 处理微信公众号消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def text_reply(msg):
    # 监听指定微信公众号推送的文章信息
    print msg
    if itchat.search_mps(name='PythonCoder')[0]["NickName"] == "PythonCoder":
        # 爬取的是itchat.search_mps(name='PythonCoder')[0]["NickName"]的公众号文章
        if msg["MsgType"] == 49:
            print "监听到指定微信公众号分享的文章链接："
            # 拿到链接以后就可以获取到文章信息
            print msg["Url"]
        else:
            print "微信公众号分享的不是文章"
    elif itchat.search_mps(name='非著名程序员')[0]["NickName"] == "非著名程序员":
        if msg["MsgType"] == 49:
            print "监听到指定微信公众号分享的文章链接："
            # 拿到链接以后就可以获取到文章信息
            print msg["Url"]
        else:
            print "微信公众号分享的不是文章"
    elif itchat.search_mps(name='程序员大咖')[0]["NickName"] == "程序员大咖":
        if msg["MsgType"] == 49:
            print "监听到指定微信公众号分享的文章链接："
            # 拿到链接以后就可以获取到文章信息
            print msg["Url"]
        else:
            print "微信公众号分享的不是文章"
    elif itchat.search_mps(name='iOS程序员大咖')[0]["NickName"] == "iOS程序员大咖":
        if msg["MsgType"] == 49:
            print "监听到指定微信公众号分享的文章链接："
            # 拿到链接以后就可以获取到文章信息
            print msg["Url"]
        else:
            print "微信公众号分享的不是文章"
    else:
        pass


itchat.auto_login(hotReload=True)
# 绑定消息响应事件后，让itchat运行起来，监听消息
itchat.run()