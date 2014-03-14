#coding:utf-8
import time
import collections

from django.http import HttpResponse
import requests


def md5(str):
    import hashlib
    import types

    if type(str) is types.StringType:
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()
    else:
        return ''


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def quick_pay_conf(request):
    version = '1.0.0'  #消息版本号
    charset = 'UTF-8'  #字符编码
    signMethod = 'MD5'  #签名方法
    signature = '792c154a3e07aeb13e6d8632cdb14980'  #签名信息
    transType = '01'  #交易类型
    merAbbr = u'用户商城名称'  #商品名称
    merId = '105550149170027'  #商品代码
    merCode = ''  #商户类型
    frontEndUrl = "http://115.28.151.155:8000/"
    backEndUrl = "http://115.28.151.155:8000/"
    acqCode = ''
    orderTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    orderNumber = '8888456799'
    commodityName = ''
    commodityUrl = ''
    commodityUnitPrice = ''
    commodityQuantity = ''
    transferFee = ''
    commodityDiscount = ''
    orderAmount = '100000'
    orderCurrency = '156'
    customerName = ''
    defaultPayType = ''
    defaultBankNumber = ''
    transTimeout = ''
    customerIp = get_client_ip(request),
    origQid = ''
    merReserved = ''
    secret_key = '88888888'
    payload = {
        'version': version,
        'charset': charset,
        'transType': transType,
        'merAbbr': merAbbr,
        'merId': merId,
        'merCode': merCode,
        'frontEndUrl': frontEndUrl,
        'backEndUrl': backEndUrl,
        'acqCode': acqCode,
        'orderTime': orderTime,
        'orderNumber': orderNumber,
        'commodityName': commodityName,
        'commodityUrl': commodityUrl,
        'commodityUnitPrice': commodityUnitPrice,
        'commodityQuantity': commodityQuantity,
        'transferFee': transferFee,
        'commodityDiscount': commodityDiscount,
        'orderAmount': orderAmount,
        'orderCurrency': orderCurrency,
        'customerName': customerName,
        'defaultPayType': defaultPayType,
        'defaultBankNumber': defaultBankNumber,
        'transTimeout': transTimeout,
        'customerIp': customerIp[0],
        'origQid': origQid,
        'merReserved': merReserved
    }
    signature_str = ''
    payload = collections.OrderedDict(sorted(payload.items()))
    for (k, v) in payload.items():
        item = "{}={}&".format(k, v.encode('utf8'))
        signature_str += item
    secret_key_str = md5('88888888')
    signature_str += secret_key_str
    signature = md5(signature_str)
    payload['signMethod'] = signMethod
    payload['signature'] = signature
    r = requests.post('http://58.246.226.99/UpopWeb/api/Pay.action', data=payload)
    content = r.text.encode('utf8')
    content = content.replace('/UpopWeb/js/jquery/', '/static/js/')
    return HttpResponse(content)


def quick_pay_conf_test():
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    payload = {
        'version': "1.0.0",
        'signature': 'signature',
        'signMethod': "signMethod",
        'transType': '01',
        'merCode': '105550149170027',
        'merId': '105550149170027',
        'charset': 'UTF-8',
        'merName': u'用户商城名称',
        'merFrontEndUrl': "http://115.28.151.155:8000/",
        'merBackEndUrl': "http://115.28.151.155:8000/",
        'orderTime': current_time,
        'orderNumber': '88888888',
        'orderAmount': '1000',
        'orderCurrency': '156',
        'customerIp': '127.0.0.1'
    }
    signature_str = ''
    payload = collections.OrderedDict(sorted(payload.items()))
    for i in payload:
        item = "{}={}&".format(i, payload[i].encode('utf8'))
        print item
        signature_str += item
    secret_key_str = md5('88888888')
    signature_str += secret_key_str
    print signature_str
    signature = md5(signature_str)
    r = requests.post('http://58.246.226.99/UpopWeb/api/Pay.action', data=payload)
    print r.text.encode('utf8')


if (__name__ == '__main__'):
    quick_pay_conf_test()
