from yiban import Yiban
import json

if __name__ == '__main__':
    try:
        # read data from file.
        with open('config.json', encoding='utf-8') as f:
            json_datas = json.load(f)['address']

        yiban = Yiban(json_datas['mobile'], json_datas['password'], '10月17日体温检测')
        yiban.get_address()
        print(yiban.get_picture("9a6da1b5c2519032945d1048a60d75f9"))
    except KeyError as e:
        print("config.json file error:")
    except Exception as e:
        print(e)