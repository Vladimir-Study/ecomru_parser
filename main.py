import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pprint36 import pprint
import re

url_wildberries = 'https://www.wildberries.ru/catalog/18256273/detail.aspx?targetUrl=MI'
url_ozon = 'https://www.ozon.ru/product/kofemashina-kapsulnaya-homberg-hb11515-chernyy-166447043/?sh=bdUkALaXcg'
url_yandex = 'https://market.yandex.ru/offer/gXBC9f3VsTCE8tua_dKwkA?cpa=1&onstock=1'


class ParserWildberries():

    def __init__(self, url: str):
        self.url = url

    def get_json(self):
        product_number = re.search(r'\d+', self.url)
        url_json = f'https://wbx-content-v2.wbstatic.net/ru/{product_number[0]}.json'
        try:
            response = requests.get(url_json, timeout=5)
            response.raise_for_status()
        except HTTPError:
            print(f'HTTP Error: {HTTPError}')
        except Exception:
            print(f'Exeption: {Exception}')
        else:
            return response.json()


class ParserOzon():

    def __init__(self, url: str):
        self.url = url

    def get_json(self):
        sub_one = re.sub(r'\S+[.]ru', '', self.url)
        sub_two = re.sub(r'[?]sh\S+', '', sub_one)
        sh = re.sub(r'\S+sh[=]', '', self.url)
        params = {
            'url': sub_two,
            'layout_page_index': '2',
            'sh': sh
        }
        url_request = 'https://www.ozon.ru/api/composer-api.bx/page/json/v2'
        try:
            response = requests.get(url_request, params=params, timeout=5)
            response.raise_for_status()
        except HTTPError:
            print(f'HTTP Error {HTTPError}')
        except Exception:
            print(f'Exception: {Exception}')
        else:
            return response.json()


class ParserYandex():

    def __init__(self, url):
        self.url = url

    def get_response(self):
        try:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Host': 'market.yandex.ru',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            }
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
        except HTTPError:
            print(f'HTTP Error {HTTPError}')
        except Exception:
            print(f'Exception: {Exception}')
        else:
            return response

if __name__ == '__main__':
    # product_test = ParserWildberries(url_wildberries)
    # pprint(product_test.get_json())
    # product = ParserOzon(url_ozon)
    # json_read = product.get_json()
    # with open('ozon.json', 'w', encoding='utf-8') as file:
    #     json.dump(json_read, file, ensure_ascii=False)
    yandex_product = ParserYandex(url_yandex)
    res_get_yandex = yandex_product.get_response()
    pprint(res_get_yandex.text.encode('utf-8'))
    soup = BeautifulSoup(res_get_yandex.text, 'html.parser')