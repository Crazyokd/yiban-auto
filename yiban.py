#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Rekord
# @Date: 2022-02-01

import re
import time
import json
import requests
import datetime
from crypter import rsa_encrypt, aes_encrypt, aes_decrypt
import os
import random

os.environ['NO_PROXY']="www.yiban.cn" # cancel proxy

class Yiban():
    AES_KEY = '2knV5VGRTScU7pOq'
    AES_IV = 'UmNWaNtM0PUdtFCs'
    RSA_KEY = '''-----BEGIN PUBLIC KEY-----
            MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
            Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
            XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
            KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
            A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
            AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
            d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
            7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
            mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
            AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
            uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
            ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
            -----END PUBLIC KEY-----
            '''
    CSRF = '000000' # Any
    COOKIES = {"csrf_token": CSRF}  # 固定cookie 无需更改
    HEADERS = {"Origin": "https://c.uyiban.com", "User-Agent": "Yiban", "AppVersion": "5.0"}  # 固定头 无需更改    
              
    def __init__(self, mobile, password, today=datetime.datetime.today() + datetime.timedelta(hours=8-int(time.strftime('%z')[0:3]))):
        self.session = requests.session()
        self.mobile = mobile
        self.password = password
        self.today = today
        self.login()

    
    def req(self, url, method='get', cookies={}, headers={}, timeout=5, allow_redirects=True, **kwargs):
        time.sleep(1) # 增加请求延时，避免请求过快 Error104
        data = kwargs.get("data")
        params = kwargs.get("params")
        cookies.update(self.COOKIES)
        headers.update(self.HEADERS)
        if method == 'get':
            resp = self.session.get(
                url     = url, 
                data    = data,
                params  = params,
                headers = headers, 
                cookies = cookies, 
                timeout = timeout,
                allow_redirects = allow_redirects
            )
        elif method == 'post':
            resp = self.session.post(
                url     = url, 
                data    = data,
                params  = params,
                headers = headers, 
                cookies = cookies, 
                timeout = timeout,
                allow_redirects = allow_redirects
            )
        else:
            self.session.close()    # close session
            raise Exception('Requests method error.')
        return resp


    def login(self):
        resp = self.req(
            method= 'post',
            url = 'https://mobile.yiban.cn/api/v4/passport/login',
            data = {
                'ct':       '2',
                'identify': '1',
                'mobile':   self.mobile,
                'password': rsa_encrypt(self.RSA_KEY, self.password),
            }
        ).json()
        # print(resp)
        if resp['response'] == 100:
            self.name = resp['data']['user']['name']
            self.access_token = resp['data']['access_token']
            print(self.name, "login success!")
        else:
            self.session.close()    # close session
            raise Exception(f'login fail, the mobile or password is wrong.')
    

    def submit_task(self, address_info):
        # 校本化认证
        self.auth()

        # # 获取未完成任务列表
        # print("uncompleted task list: ", self.getUncompletedList()['data'])
        # # 获取已完成任务列表
        # print("completed task list: ", self.getCompletedList())
        
        self.auto_fill_form(self.getUncompletedList(), address_info)


    def auth(self):
        # 校本化认证
        resp = self.req(
            url='http://f.yiban.cn/iapp/index', 
            params={'act': 'iapp7463'},
            cookies={'loginToken': self.access_token},
            allow_redirects=False
        )
        verify = re.findall(r"verify_request=(.*?)&", resp.headers.get("Location"))[0]
        self.req(
            url='https://api.uyiban.com/base/c/auth/yiban', 
            params={'verifyRequest': verify, 'CSRF': self.CSRF},
        )


    def re_auth(self):
        self.req(
            method='post',
            url='https://oauth.yiban.cn/code/usersure', 
            data={'client_id': '95626fa3080300ea', 'redirect_uri': 'https://f.yiban.cn/iapp7463'}
        )
        

    def getCompletedList(self):
        resp = self.req(
            url='https://api.uyiban.com/officeTask/client/index/completedList', 
            params={
                'StartTime': (self.today+datetime.timedelta(days=-14)).strftime('%Y-%m-%d'),
                'EndTime': "%d-%02d-%02d 23:59" % (self.today.year, self.today.month, self.today.day),
                'CSRF': self.CSRF
            }
        ).json()
        # auth again
        if resp['data'] is None:
            self.re_auth()
            self.session.close()    # close session
            raise Exception("auth expired, please try again.")
        
        return resp
        

    def getUncompletedList(self):
        resp = self.req(
            url='https://api.uyiban.com/officeTask/client/index/uncompletedList', 
            params={
                'StartTime': (self.today+datetime.timedelta(days=-14)).strftime('%Y-%m-%d'),
                'EndTime': "%d-%02d-%02d 23:59" % (self.today.year, self.today.month, self.today.day),
                'CSRF': self.CSRF
            }
        ).json()
        # auth again
        if resp['data'] is None:
            self.re_auth()
            self.session.close()    # close session
            raise ConnectionError("auth expired, please try again.")

        return resp


    def auto_fill_form(self, resp, address_info):
        # generate task title
        task_title = f'{self.today.month}月{self.today.day}日体温检测'
        # traverse task list
        for i in resp['data']:
            if i['Title'] == task_title:
                task_detail = self.req(
                    url='https://api.uyiban.com/officeTask/client/index/detail', 
                    params={'TaskId': i['TaskId'], 'CSRF': self.CSRF}
                ).json()['data']

                # self.view_completed(task_detail['InitiateId'])
                # print(task_detail)

                extend = {
                    "TaskId":  task_detail["Id"],
                    "title": "任务信息",
                    "content": [
                        {"label": "任务名称", "value": task_detail["Title"]},
                        {"label": "发布机构", "value": task_detail["PubOrgName"]},
                        {"label": "发布人", "value": task_detail["PubPersonName"]}
                    ]
                }
                data_form = { 
                    "c77d35b16fb22ec70a1f33c315141dbb": "%d-%02d-%02d %02d:%02d" % (self.today.year, self.today.month, self.today.day, self.today.hour, self.today.minute), 
                    "2d4135d558f849e18a5dcc87b884cce5": str(round(random.uniform(35.2, 35.8), 1)), 
                    "27a2a4cdf16a8c864daca54a00c4db03": {
                        "name": address_info['name'],
                        "location": address_info['location'],
                        "address": address_info['address']
                    }
                }

                submit_data = {}
                submit_data['WFId'] = task_detail['WFId']
                submit_data['Extend'] = json.dumps(extend, ensure_ascii=False)
                submit_data['Data'] = json.dumps(data_form, ensure_ascii=False)
                postData = json.dumps(submit_data, ensure_ascii=False)  # transfer to json

                resp = self.req(
                    method='post',
                    url=f'https://api.uyiban.com/workFlow/c/my/apply',
                    params={'CSRF': self.CSRF},
                    data={'Str': aes_encrypt(self.AES_KEY, self.AES_IV, postData)}
                ).json()

                # Failed
                if resp['code'] != 0:
                    self.session.close()    # close session
                    raise Exception(f"punch failed.")
                break


    "通过此函数可以分析已提交的表单数据"
    def view_completed(self, InitiateId):
        print(self.req(
            url=f'https://api.uyiban.com/workFlow/c/work/show/view/{InitiateId}',
            params={'CSRF': self.CSRF}
        ).json()['data']['Initiate'])

    
    def get_address(self, month=datetime.date.today().month, day=datetime.date.today().day):
        # 校本化认证
        self.auth()
        # generate task title
        task_title = f'{month}月{day}日体温检测'
        # traverse task list
        for i in self.getCompletedList()['data']:
            if i['Title'] == task_title:
                InitiateId = self.req(
                    url='https://api.uyiban.com/officeTask/client/index/detail', 
                    params={'TaskId': i['TaskId'], 'CSRF': self.CSRF}
                ).json()['data']['InitiateId']
                print(self.req(
                    url=f'https://api.uyiban.com/workFlow/c/work/show/view/{InitiateId}',
                    params={'CSRF': self.CSRF}
                ).json()['data']['Initiate']['FormDataJson'][2]['value'])
                break