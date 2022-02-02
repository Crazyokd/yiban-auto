#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Rekord
# @Date: 2022-02-02
# 易班校本化打卡

import time
import json
from yiban import Yiban


def main_handler(data=None, extend=None):
    with open('config.json', encoding='utf-8') as f:
        json_datas = json.load(f)['Forms']

    # print(json_datas)
    for data in json_datas:
        msg = f"{time.strftime('%y-%m-%d',time.localtime(time.time()))} 易班打卡："
        nickname = data['UserInfo']['NickName']
        submit_data = data['SubmitData']
        try:
            yiban = Yiban(data['UserInfo']['Mobile'], data['UserInfo']['Password'])
            yiban.submit_task(submit_data)
            msg = f'{msg}{nickname} 打卡成功.'
        except Exception as e:
            msg = f'{msg}{nickname}: {e}'
        finally:
            print(msg)
            time.sleep(1)


if __name__ == '__main__':
    main_handler()