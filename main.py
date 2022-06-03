import requests
import re
from pprint36 import pprint

url = 'https://www.wildberries.ru/catalog/18256273/detail.aspx?targetUrl=MI'


class ParserWildberries():

    def __init__(self, url):
        self.url = url

    def get_json(self):
        product_number = re.search(r'\d+', self.url)
        url_json = f'https://wbx-content-v2.wbstatic.net/ru/{product_number[0]}.json'
        response = requests.get(url_json).json()
        return response


if __name__ == '__main__':
    product_test = ParserWildberries(url)
    pprint(product_test.get_json())