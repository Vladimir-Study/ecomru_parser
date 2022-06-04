import requests
from pprint36 import pprint
import re
import json

url_product = 'https://www.ozon.ru/product/kofemashina-kapsulnaya-homberg-hb11515-chernyy-166447043/?sh=bdUkALaXcg'


class ParserOzon():

    def __init__(self, url):
        self.url = url

    def get_json(self):
        sub_one = re.sub(r'\S+[.]ru', '', self.url)
        sub_two = re.sub(r'[?]sh\S+', '', sub_one)
        sh = re.sub(r'\S+sh[=]', '', url_product)
        params = {
            'url': sub_two,
            'layout_page_index': '2',
            'sh': sh
        }
        url_request = 'https://www.ozon.ru/api/composer-api.bx/page/json/v2'
        response = requests.get(url_request, params=params).json()
        return response


if __name__ == '__main__':
    product = ParserOzon(url_product)
    json_read = product.get_json()
    with open('ozon.json', 'w', encoding='utf-8') as file:
        json.dump(json_read, file, ensure_ascii=False)