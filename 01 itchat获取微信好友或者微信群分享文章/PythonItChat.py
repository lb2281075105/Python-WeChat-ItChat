#coding=utf-8
'''
itchat:获取分享给群或者个人的技术文章
(0) 熟悉itchat,(https://www.cnblogs.com/Chenjiabing/p/6907397.html)
(1) itchat 扫码次数太多会被限制扫码登录微信。
(2) itchat:获取分享给群或者个人的技术文章,提取出文章链接、文章标题、文章首页图片、文章内容
(3) 通过获取到的文章链接，爬虫文章内容。
(4) 判断是接收方(ToUserName)是谁、发送方(FromUserName)是谁就是通过唯一的ID来判别的。
(5) python itchat 热登陆(itchat.auto_login(hotReload=True))
(6) xpath模块爬取文章标题、文章内图片
(7) 搭建web服务器环境(Mac使用XAMPP)
(8) pymysql模块自动创建数据库、创建字段、保存内容到字段
(9) navicat 的使用
(10) python 相关模块的使用
'''

# 爬取微信群或者是好友分享的文章
# 监听微信公众号分享的文章
import re
import itchat
# import全部消息类型
from itchat.content import *
import urllib
import lxml.etree
import os
import pymysql
import uuid
import json
import requests
import io
# import cStringIO
from pyquery import PyQuery as pq
# mongodb
from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import *
# import sys
import reload
# reload(sys)
# sys.setdefaultencoding('utf8')
# 连接数据库mysql
table_cms_news = 'cms_news'
table_cms_news_pic = 'cms_news_pic'
# db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='itchat', charset='utf8')
db = pymysql.connect(host='xxx', user='xxx', passwd='xxx', db='fz_afmcms', charset='utf8')
cur = db.cursor()

urlHost = 'xxx'
# 连接到MongoDB
client = MongoClient('xxx', xxx)
db = client.images
fs = GridFS(db, 'fs')

# 处理个人分享消息
# 包括文本、位置、名片、通知、分享(49重点)
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg)
    # 微信里，每个用户和群聊，都使用很长的ID来区分
    if msg["MsgType"] == 49:
        print("个人分享文章地址链接Url:" + "---------------------------")

        xmlcontent = lxml.etree.HTML(get_html(msg["Url"]))
            title = xmlcontent.xpath('//h2[@class="rich_media_title"]/text()')
            imgArray = xmlcontent.xpath('//img/@data-src')
        
            # 来源
            source = xmlcontent.xpath('//span[@class="rich_media_meta rich_media_meta_text rich_media_meta_nickname"]/text()')
                time = xmlcontent.xpath('//em[@class="rich_media_meta rich_media_meta_text"]/text()')
                content = xmlcontent.xpath('//div[@class="rich_media_content "]')[0]
                print (msg["Content"])
                print("来源")
                print (source, time)
                # 下载图片
                print("下载图片")
                # print imgArray
                # print title[0]
                get_image(title, imgArray, source, time,msg["Url"],content)
            
                print ("个人分享文章类型编号MsgType:" + "---------------------------")
                print (msg["MsgType"])
                print ("个人分享Content:" + "---------------------------")
                print (msg["Content"])
                print ("个人分享FromUserName:" + "---------------------------")
                print (msg["FromUserName"])
                print ("个人分享ToUserName:" + "---------------------------")
                print (msg["ToUserName"])
                print ("个人分享链接标题FileName:" + "---------------------------")
                print (msg["FileName"])
            
                # return msg['Text']
                # itchat.send('%s: %s : %s' % (msg['Type'], msg['Text'],msg['Url']), msg['FromUserName'])
                print ("------------个人")
                    # 获取到的信息是某某人和登录者之间的通讯，如果不是和登录这通讯就获取不到
                print (itchat.search_friends(userName=msg['FromUserName'])['NickName'])
                print (itchat.search_friends(userName=msg['ToUserName'])['NickName'])
                    
    else:
        print ("不是个人分享的文章")


# 处理群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def text_reply(msg):
    print (msg)
    if msg["MsgType"] == 49:
        print ("群聊分享文章地址链接Url:" + "---------------------------")
        print (msg["Url"])
        
        xmlcontent = lxml.etree.HTML(get_html(msg["Url"]))
        title = xmlcontent.xpath('//h2[@class="rich_media_title"]/text()')
        imgArray = xmlcontent.xpath('//img/@src')
        
        # 来源
        source = xmlcontent.xpath('//span[@class="rich_media_meta rich_media_meta_text rich_media_meta_nickname"]/text()')
        time = xmlcontent.xpath('//em[@class="rich_media_meta rich_media_meta_text"]/text()')
        # content = xmlcontent.xpath('//div[@class="rich_media_content "]/p/span/text()')
        content = xmlcontent.xpath('//div[@class="rich_media_content "]')[0]
        
        # print msg["Content"]
        print ("内容")
        
        print ("来源")
        print (source,time)
        # 下载图片
        print ("下载图片")
        print (imgArray)
        print (msg["Url"])
        # print title[0]
        get_image(title,imgArray,source,time,msg["Url"],content)
        
        print ("-------------群--------")
        # itchat.send('%s: %s : %s' % (msg['Type'], msg['Text'], msg['Url']), msg['FromUserName'])
        
        print (msg['FromUserName'])
        print (msg['ToUserName'])
    # 这个是需要每次扫码登录都改变的receiver
    # receiver = "@bc33fe9613d2e671dd61c6c75e28fb4af8e1ee86fada62b5a893eafd71e2a797"
    # if msg['FromUserName'] == receiver:
    #     print "----------- 自己在群里发的文章 ------------"
    #     # 自己在群里发的文章
    #     print "昵称:"
    #     print itchat.search_friends(userName=msg['FromUserName'])['NickName']
    #     print " ----------- "
    #     print "群名称:"
    #     print itchat.search_chatrooms(userName=msg['ToUserName'])['NickName']
    #     chatRoomName = "呵呵各地"
    #     # if itchat.search_chatrooms(userName=msg['ToUserName'])['NickName'] == chatRoomName:
    #     #     pass
    #     # else:
    #     #     pass
    #
    # else:
    #     # 群友发的文章
    #     print "----------- 群友发的文章 -----------"
    #     print "昵称:"
    #     print msg['ActualNickName']
    #     print " ----------- "
    #     print "群名称:"
    #     print itchat.search_chatrooms(userName=msg['FromUserName'])['NickName']
    #     chatRoomName = "呵呵各地"
    #     # if itchat.search_chatrooms(userName=msg['FromUserName'])['NickName'] == chatRoomName:
    #     #     pass
    #     # else:
    #     #     pass
    else:
        print ("不是群聊分享的文章")
# return msg['Text']


# 处理微信公众号消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def text_reply(msg):
    print (msg)
    print (itchat.search_mps(name='PythonCoder')[0]["NickName"])
    if msg["MsgType"] == 49:
        print ("监听到制定微信公众号分享的文章链接：")
        print (msg["Url"])
    else:
        print ("微信公众号分享的不是文章")

# 获取网页内容
def get_html(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    return html.replace('data-src', 'src')

# 下载图片
def get_image(title,imgArray,source,time,linkurl,content):
    print ("标题")
    result = cur.execute("select source_url from cms_news WHERE source_url='"+ linkurl + "'")
    print(str(result) + '------------url-----------')
    
    titleJ = ''
    sourceJ = ''
    timeJ = ''
    
    if len(title) == 0:
        pass
    # titleJ = ''
    else:
        titleJ = title[0].strip().replace("\n", "")
    if len(source) == 0:
        # sourceJ = ''
        pass
    else:
        sourceJ = source[0].strip().replace("\n", "")
    if len(time) == 0:
        # timeJ = ''
        pass
    else:
        timeJ = time[0].strip().replace("\n", "")
    
    if len(imgArray) == 0:
        pass
    else:
        print ('wo de shi ')
        print (content)
        for item in imgArray:
            
            if len(item) == 0:
                imgArray.remove(item)
                continue
            if item.find('http') == 0:
                pass
            else:
                imgArray.remove(item)

        for item in imgArray:
            
            if item.find('http') == 0:
                print (item.find('http'))
                # 根据宽高来筛选图片
                data = requests.get(item).content
                tmpIm = io(data)
                from PIL import Image
                img = Image.open(tmpIm)
                width = img.size[0]
                height = img.size[1]
                if width < 460 and height < 460:
                    imgArray.remove(item)
                else:
                    pass
            else:
                continue

print (imgArray)

# print imgArray
print ('图片筛选')
    # if len(imgArray) == 0:
    #     return
    # return
    new_id = str(uuid.uuid1()).strip().replace("-", "")
    new_id1 = str(uuid.uuid1()).strip().replace("-", "")
    new_id2 = str(uuid.uuid1()).strip().replace("-", "")
    
    if result:
        print("------------数据库里面存在此数据------------")
else:
    if os.path.isdir('./imgs'):
        pass
        else:
            os.mkdir("./imgs")
    if len(imgArray) == 0:
        pass
        else:
            for index,item in enumerate(imgArray):
                if index == 0:
                    with open('imgs/' + new_id + ".png", 'a+') as file:
                        file.write(get_html(item))
                        file.close
                elif index == 1:
                    with open('imgs/' + new_id1 + ".png", 'a+') as file:
                        file.write(get_html(item))
                        file.close
                elif index == 2:
                    with open('imgs/' + new_id2 + ".png", 'a+') as file:
                        file.write(get_html(item))
                        file.close
ima_dic = ""
    news_pic = ""
        news_pic_s = ""
        news_pic_t = ""
        
        news_content = ""
        news_content1 = ''
        # 内容
        if len(content) == 0:
            news_content = ""
            news_content1 = ''
        else:
            pass
    # news_content1 = content[0]
    # news_content = content
    content = lxml.etree.tostring(content, pretty_print=True, method='html')
        pqcontent = pq(unicode(content,'utf-8'))
        
        pqcontent('div').remove_attr('class')
        pqcontent('div').remove_attr(' ')
        pqcontent('div').remove_attr('style')
        pqcontent('div').remove_attr('id')
        pqcontent('url').remove_attr('class')
        pqcontent('url').remove_attr('cid')
        pqcontent('url').remove_attr('data-mark')
        pqcontent('url').remove_attr('style')
        pqcontent('url').remove_attr('mdtype')
        pqcontent('url').remove_attr('class')
        pqcontent('url').remove_attr('id')
        pqcontent('url').remove_attr('cid')
        pqcontent('code').remove_attr('style')
        pqcontent('a').remove_attr('href')
        pqcontent('a').remove_attr('class')
        pqcontent('a').remove_attr('style')
        pqcontent('a').remove_attr('id')
        pqcontent('a').remove_attr('data')
        pqcontent('p').remove_attr('style')
        pqcontent('p').remove_attr('class')
        pqcontent('p').remove_attr('id')
        pqcontent('p').remove_attr('data-mpa-powered-by')
        pqcontent('span').remove_attr('cid')
        pqcontent('span').remove_attr('mdtype')
        pqcontent('p').remove_attr('cid')
        pqcontent('p').remove_attr('mdtype')
        pqcontent('span').remove_attr('spellcheck')
        pqcontent('video').remove_attr('style')
        pqcontent('video').remove_attr('class')
        pqcontent('video').remove_attr('id')
        pqcontent('source').remove_attr('style')
        pqcontent('source').remove_attr('class')
        pqcontent('source').remove_attr('id')
        pqcontent('table').remove_attr('style')
        pqcontent('table').remove_attr('class')
        pqcontent('table').remove_attr('id')
        pqcontent('tr').remove_attr('style')
        pqcontent('tr').remove_attr('class')
        pqcontent('tr').remove_attr('id')
        pqcontent('img').remove_attr('style')
        pqcontent('img').remove_attr('class')
        pqcontent('img').remove_attr('id')
        pqcontent('img').remove_attr('data-s')
        pqcontent('img').remove_attr('data-copyright')
        pqcontent('img').remove_attr('data-ratio')
        pqcontent('td').remove_attr('style')
        pqcontent('td').remove_attr('class')
        pqcontent('td').remove_attr('id')
        pqcontent('h1').remove_attr('style')
        pqcontent('h1').remove_attr('class')
        pqcontent('h1').remove_attr('id')
        pqcontent('h2').remove_attr('style')
        pqcontent('h2').remove_attr('class')
        pqcontent('h2').remove_attr('id')
        pqcontent('h3').remove_attr('style')
        pqcontent('h3').remove_attr('class')
        pqcontent('h3').remove_attr('id')
        pqcontent('section').remove_attr('style')
        pqcontent('section').remove_attr('class')
        pqcontent('section').remove_attr('id')
        pqcontent('fieldset').remove_attr('style')
        pqcontent('fieldset').remove_attr('class')
        pqcontent('fieldset').remove_attr('id')
        pqcontent('span').remove_attr('style')
        pqcontent('span').remove_attr('class')
        pqcontent('span').remove_attr('id')
        pqcontent('span').remove_attr('md-inline')
        pqcontent('span').remove_attr('data-shimo-docs')
        pqcontent('strong').remove_attr('style')
        pqcontent('strong').remove_attr('class')
        pqcontent('strong').remove_attr('id')
        pqcontent('blockquote').remove_attr('style')
        pqcontent('blockquote').remove_attr('class')
        pqcontent('blockquote').remove_attr('id')
        pqcontent('legend').remove_attr('style')
        pqcontent('legend').remove_attr('class')
        pqcontent('legend').remove_attr('id')
        pqcontent('br').remove_attr('style')
        pqcontent('br').remove_attr('class')
        pqcontent('br').remove_attr('id')
        print ('-----------------------------------------')
        print (type(str(pqcontent.html())))
        print ('-----------------------------------------')
        # print pqcontent.html()
        if len(imgArray) == 0:
            pass
        else:
            ima_dic = imgArray[0]

if len(imgArray) == 0:
    pass
        elif len(imgArray) == 1:
            news_pic = imgArray[0]
            data = requests.get(news_pic).content
            id = fs.put(data, filename = new_id + '.png')
            print (id)
            news_pic = urlHost + new_id + '.png'
    elif len(imgArray) == 2:
        news_pic = imgArray[0]
        news_pic_s = imgArray[1]
        for index,item in enumerate(imgArray):
            if index == 0:
                data = requests.get(item).content
                id = fs.put(data, filename=new_id + '.png')
                print (id)
                news_pic = urlHost + new_id + '.png'
                else:
                    data = requests.get(item).content
                    id = fs.put(data, filename=new_id1 + '.png')
                    print (id)
                    news_pic_s = urlHost + new_id1 + '.png'
elif len(imgArray) >= 3:
    news_pic = imgArray[0]
    news_pic_s = imgArray[1]
    news_pic_t = imgArray[2]
    print (news_pic)
    print (news_pic_s)
    print (news_pic_t)
    for index,item in enumerate(imgArray):
        if index == 0:
            data = requests.get(item).content
            id = fs.put(data, filename=new_id + '.png')
            print (id)
            news_pic = urlHost + new_id + '.png'
                elif index == 1:
                    data = requests.get(item).content
                    id = fs.put(data, filename=new_id1 + '.png')
                    print (id)
                    news_pic_s = urlHost + new_id1 + '.png'
            else:
                data = requests.get(item).content
                id = fs.put(data, filename=new_id2 + '.png')
                print (id)
                news_pic_t = urlHost + new_id2 + '.png'

    cur.execute(
                'INSERT INTO ' + table_cms_news_pic + ' (news_id,pic_url,pic_desc) VALUES (%s,%s,%s)',
                (new_id, news_pic,""))
        cur.execute(
                    'INSERT INTO ' + table_cms_news + ' (news_open_type,news_id,news_title,news_type,com_id,'\
                    'news_column_code1,news_column_name1,'\
                    'news_column_code2,news_column_name2,news_desc,news_pic,'\
                    'news_pic_s,news_pic_t,news_pic_is_show,'\
                    'news_content,news_source,news_cuser_name,'\
                    'news_ctime,news_url,news_status,view_count,platid,source_url) '\
                    'VALUES (%s,%s, %s,%s,%s, %s,%s,%s,%s, %s,%s, %s,%s,%s,'\
                    ' %s,%s, %s,%s,%s,%s,%s,%s,%s)',
                    ('1',new_id,titleJ,'1','','','','','','',news_pic,news_pic_s,
                     news_pic_t,'1',pqcontent.html(),sourceJ,sourceJ,timeJ,"",
                     '1',200,'weixin',linkurl))
                     
                     cur.connection.commit()
                     print("------------------------  插入成功  ----------------------------------")

# 连接数据库
 def get_connect():

     try:
         # 创建表
         cur.execute(
             'CREATE TABLE ' + table_cms_news + ' (id BIGINT(7) NOT NULL AUTO_INCREMENT, title VARCHAR(1000),url VARCHAR(10000), img VARCHAR(1000), source VARCHAR(1000), time VARCHAR(1000), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id))')
     except pymysql.err.InternalError as e:
         print(e)
     # 修改表字段
     cur.execute('ALTER DATABASE itchat CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci')
     cur.execute(
         'ALTER TABLE ' + table_cms_news + ' CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
     cur.execute(
         'ALTER TABLE ' + table_cms_news + ' CHANGE title title VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
     cur.execute(
         'ALTER TABLE ' + table_cms_news + ' CHANGE url url VARCHAR(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
     cur.execute(
             'ALTER TABLE ' + table_cms_news + ' CHANGE img img VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
     cur.execute(
         'ALTER TABLE ' + table_cms_news + ' CHANGE source source VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
     cur.execute(
         'ALTER TABLE ' + table_cms_news + ' CHANGE time time VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')

def loginCallback():
    pass
def exitCallback():
    pass
# 热登录(在一段时间内不用扫码登录还能保持登录状态)
 get_connect()
print ("哈哈")
itchat.auto_login(hotReload=True)
# 绑定消息响应事件后，让itchat运行起来，监听消息
itchat.run()


