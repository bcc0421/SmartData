#!/usr/bin/python
# _*_ coding: UTF-8 _*_

import sys
import datetime

sys.path.append("..")
from Channel import *

#以下只是测试数据，请使用者自行修改为可用数据
apiKey = "xS8MeH5f4vfgTukMcB2Bo6Ea"
secretKey = "chcxUOTIvBkItk91bXbXxQw5VSAaYhBb"
user_id = 665778416804465913
appid = 1867886
channel_id = '4617656892525519033'
dev_host = 'https://channel.iospush.api.duapp.com'

# "appid" = 1867886;
#   "channel_id" = 4617656892525519033;
#   user_id = '665778416804465913'
message = "{" \
          " 'title': 'title', " \
          "'description': 'description', " \
          "'notification_builder_id': 0," \
          "'notification_basic_style': 4," \
          "'open_type':2,'" \
          "custom_content':{" \
          "'type_code':'1'," \
          "'type_content':'7448969'" \
          "} " \
          "}"
# message = json.dumps(message)
message_key = "testtest111"
# message_key = json.dumps(message_key)
tagname = "test_tag"


def test_pushMessage_to_user():
    c = Channel(apiKey, secretKey)
    c.DEFAULT_HOST=dev_host
    push_type = 1
    optional = dict()
    #optional[Channel.USER_ID] = 815730795201756090
    optional[Channel.USER_ID] = 665778416804465913
    optional[Channel.CHANNEL_ID] = 4617656892525519033
    #optional[Channel.CHANNEL_ID] = 4320553738754859600
    #推送通知类型
    optional[Channel.DEVICE_TYPE] = 4
    optional[Channel.MESSAGE_TYPE] = 1
    optional['phone_type'] = 'ios'
    ret = c.pushMessage(push_type, message, hashlib.md5(str(datetime.datetime.now())).hexdigest(), optional)
    print ret


def test_pushMessage_to_tag():
    c = Channel(apiKey, secretKey)
    push_type = 2
    tag_name = 'push'
    optional = dict()
    optional[Channel.TAG_NAME] = tag_name
    ret = c.pushMessage(push_type, message, message_key, optional)
    print ret


def test_pushMessage_to_all():
    c = Channel(apiKey, secretKey)
    push_type = 3
    optional = dict()
    ret = c.pushMessage(push_type, message, message_key, optional)
    print ret


def test_queryBindList():
    c = Channel(apiKey, secretKey)
    optional = dict()
    optional[Channel.CHANNEL_ID] = channel_id
    ret = c.queryBindList(user_id, optional)
    print ret


def test_verifyBind():
    c = Channel(apiKey, secretKey)
    optional = dict()
    optional[Channel.DEVICE_TYPE] = 3
    ret = c.verifyBind(user_id, optional)
    print ret


def test_fetchMessage():
    c = Channel(apiKey, secretKey)
    ret = c.fetchMessage(user_id)
    print ret


def test_deleteMessage():
    c = Channel(apiKey, secretKey)
    msg_id = "111"
    ret = c.deleteMessage(user_id, msg_id)
    print ret


def test_setTag():
    c = Channel(apiKey, secretKey)
    optional = dict()
    optional[Channel.USER_ID] = user_id
    ret = c.setTag(tagname, optional)
    print ret


def test_fetchTag():
    c = Channel(apiKey, secretKey)
    ret = c.fetchTag()
    print ret


def test_deleteTag():
    c = Channel(apiKey, secretKey)
    optional = dict()
    optional[Channel.USER_ID] = user_id
    ret = c.deleteTag(tagname, optional)
    print ret


def test_queryUserTag():
    c = Channel(apiKey, secretKey)
    ret = c.queryUserTag(user_id)
    print ret


def test_queryDeviceType():
    c = Channel(apiKey, secretKey)
    ret = c.queryDeviceType(channel_id)
    print ret


if (__name__ == '__main__'):

    # test_queryBindList()
    # time.sleep(1)
    test_pushMessage_to_user()
    #time.sleep(1)
    #test_pushMessage_to_tag()
    #time.sleep(1)
    #test_pushMessage_to_all()
    #time.sleep(1)
    #
    #test_verifyBind()
    #time.sleep(1)
    #test_fetchMessage()
    #time.sleep(1)
    #test_deleteMessage()
    #time.sleep(1)
    #test_setTag()
    #time.sleep(1)
    #test_fetchTag()
    #time.sleep(1)
    #test_deleteTag()
    #time.sleep(1)
    #test_queryUserTag()
    #time.sleep(1)
    #test_queryDeviceType()
    #time.sleep(1)

