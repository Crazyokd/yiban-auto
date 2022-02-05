#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Rekord
# @Date: 2022-02-02
# 易班校本化打卡

import time
import datetime
import json
from yiban import Yiban
import requests
from sendemail import start_email


def main_handler(data=None, extend=None):
    # load json datas
    with open('config.json', encoding='utf-8') as f:
        json_datas = json.load(f)['Forms']
    # print(json_datas)

    total_msg = ''
    for data in json_datas:
        success_flag = False
        while success_flag == False:
            success_flag = True
            nickname = data['UserInfo']['NickName']
            today = datetime.datetime.today()
            msg = f"%d-%02d-%02d {nickname}-易班打卡：" % (today.year, today.month, today.day)
            address_info = data['AddressInfo']
            try:
                yiban = Yiban(data['UserInfo']['Mobile'], data['UserInfo']['Password'], today)
                yiban.submit_task(address_info)
                msg = f'{msg}Success.'
            # If an error occurs due to network problems, the program will continue to run
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                success_flag = False
            except Exception as e:
                msg = f'{msg}{e}'
            finally:
                if success_flag == True:                
                    print(msg)
                    total_msg = f'{total_msg}\n\n{msg}'
                time.sleep(1)
    start_email(total_msg)


if __name__ == '__main__':
    main_handler()