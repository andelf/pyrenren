#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import webbrowser
from collections import defaultdict

from renren import AuthHandler, API
try:
    raw_input
except NameError:
    raw_input = input

API_Id = 'b3e99c82722f4204a43cf94129caf8e0'
API_Secret = 'e17954ec48cb4aa085144402f2604ff5'

CALLBACK_URL = "http://graph.renren.com/oauth/login_success.html"


auth = AuthHandler(API_Id, API_Secret, CALLBACK_URL, scope='status_update')


url = auth.get_authorization_url()
print (url)

webbrowser.open(url)

code='yzGI68aa2Nu3XTDMj1BY9lSxZT5q30MT'
code = raw_input('Code:').strip()

token = auth.get_access_token(code)
# {u'access_token': u'112893|5.4040a571daf532f413ea91fde1ac0c35.86400.1307268000-319621581',
#  u'expires_in': 88960}
#print token
print ('token=', token)
token = token['access_token']

session = auth.get_session_key(token)
#print session
print ('session=', session)

api = API(auth)

def dumpInfo(info):
    print ('{0[uid]} {0[name]} {1}'.format(info, strSex(info['sex'])))


friends_ids = api.call('friends.get')
print ('You Hava {0} Friends.'.format(len(friends_ids)))

boys = 0
girls = 0
provinceCounter = defaultdict(int)
birthyearCounter = defaultdict(int)
birthmonthCounter = defaultdict(int)
entranceYearCounter = defaultdict(int)
universityCounter = defaultdict(int)
signCounter = defaultdict(int)


strSex = lambda sex: '女' if sex == 0 else '男'

def dumpDict(title, dct, keyMapper=None, valueMapper=None, count=5):
    if keyMapper is None:
        keyMapper = lambda n:n
    if valueMapper is None:
        valueMapper = lambda n:n
    print ('== %s ==' % title)
    items = list(dct.items())
    items.sort(key = lambda i : i[1], reverse=True)
    for i,v in items[:count]:
        print (keyMapper(i), '=>', valueMapper(v))

def getSign(birthday):
    year, month, day = list(map(int, birthday.split('-')))
    if not (year*month*day):
        return ''
    dateSeg = [(1, 20.5), (2, 19.5), (3, 20.5), (4, 20.5),
               (5, 21.5), (6, 21.5), (7, 22.5), (8, 23.5),
               (9, 23.5), (10, 23.5), (11, 22.5), (12, 21.5),
               (13, 32)]
    names = ['魔羯座', '水瓶座', '双鱼座', '白羊座',
             '金牛座', '双子座', '巨蟹座', '狮子座',
             '处女座', '天秤座', '天蝎座', '射手座',
             '魔羯座']
    myseg = (month, day)
    for index, seg in enumerate(dateSeg):
        if myseg < seg:
            break
    return names[index]



infos = api.call('users.getInfo', uids=','.join(map(str, friends_ids)),
                 fields='uid,name,sex,birthday,hometown_location,university_history')

for info in infos:
    if info['sex'] == 0:
        girls += 1
    else:
        boys += 1
    #dumpInfo(info)
    #print info
    if info['hometown_location']:
        provinceCounter[info['hometown_location']['province']] += 1
    else:
        provinceCounter[''] += 1
    birthyearCounter[int(info['birthday'].split('-')[0])] += 1
    birthmonthCounter[int(info['birthday'].split('-')[1])] += 1
    signCounter[getSign(info['birthday'])] += 1
    if info['university_history']:
        univInfos = info['university_history']
        year = 0
        recentInfo = {}
        for univ in univInfos:
            if univ.get('year', 0) > year:
                year = univ['year']
                recentInfo = univ
        universityCounter[recentInfo.get('name','')] += 1
        entranceYearCounter[year] += 1
    else:
        universityCounter[''] += 1
        entranceYearCounter[0] += 1


uid = api.call('users.getLoggedInUser')['uid']
myinfo = api.call('users.getInfo', uids=uid,
                  fields='uid,name,sex,birthday,hometown_location,university_history')[0]

#api.call('users.getInfo', uids=319621581, fields='uid,name,sex,birthday,hometown_location')
#uid,name,sex,star,zidou,vip,birthday,email_hash,tinyurl,headurl,mainurl,hometown_location,work_history,university_history

print ('=*= 山寨好友档案 v0.0.1dev =*=')
dumpInfo(myinfo)
print (getSign(myinfo['birthday']))

print ('== 好友性别信息 == \n  Boys : {}\n  Girls: {}'.format(boys, girls))

dumpDict('好友省份分布', provinceCounter,
         keyMapper = lambda p: '未填写' if not bool(p) else p,
         valueMapper = lambda v: '%s个' % v)
dumpDict('好友出生年份分布', birthyearCounter,
         keyMapper = lambda p: '未填写' if not int(p) else '%s年' % p,
         valueMapper = lambda v: '%s个' % v
         )
dumpDict('好友出生月份分布', birthmonthCounter,
         keyMapper = lambda p: '未填写' if not int(p) else '%s月' % p,
         valueMapper = lambda v: '%s个' % v)
dumpDict('好友星座分布', signCounter,
         keyMapper = lambda p: '未填写' if not bool(p) else p,
         valueMapper = lambda v: '%s个' % v)

dumpDict('好友大学分布', universityCounter,
         keyMapper = lambda p: '未填写' if not bool(p) else p,
         valueMapper = lambda v: '%s个' % v)
dumpDict('好友入学年份分布', entranceYearCounter,
         keyMapper = lambda p: '未填写' if not int(p) else '%s年' % p,
         valueMapper = lambda v: '%s个' % v)

