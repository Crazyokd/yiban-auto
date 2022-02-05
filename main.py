#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Rekord
# @Date: 2022-02-02
# 易班校本化打卡

import time
import json
from yiban import Yiban
import requests


def main_handler(data=None, extend=None):
    # load json datas
    with open('config.json', encoding='utf-8') as f:
        json_datas = json.load(f)['Forms']
    # print(json_datas)

    for data in json_datas:
        success_flag = False
        while success_flag == False:
            success_flag = True
            nickname = data['UserInfo']['NickName']
            msg = f"{time.strftime('%y-%m-%d',time.localtime(time.time()))} {nickname}-易班打卡："
            address_info = data['AddressInfo']
            try:
                yiban = Yiban(data['UserInfo']['Mobile'], data['UserInfo']['Password'])
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
                time.sleep(1)


if __name__ == '__main__':
    main_handler()