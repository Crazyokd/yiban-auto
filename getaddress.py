from yiban import Yiban
import json

if __name__ == '__main__':
    try:
        # read data from file.
        with open('config.json', encoding='utf-8') as f:
            json_datas = json.load(f)['address']

        yiban = Yiban(json_datas['mobile'], json_datas['password'])
        yiban.get_address(month=json_datas['month'], day=json_datas['day'])
    except KeyError as e:
        print("config.json file error:")
    except Exception as e:
        print(e)