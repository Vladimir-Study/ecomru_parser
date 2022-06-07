import random
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup as bs
from pprint36 import pprint
import re
from fake_useragent import UserAgent

url_wildberries = 'https://www.wildberries.ru/catalog/18256287/detail.aspx?targetUrl=MI'
url_ozon = 'https://www.ozon.ru/product/kapsulnaya-kofemashina-nespresso-essenza-mini-c30-white-belyy-231470735/?sh=bdUkAJ1bqQ'
url_yandex = 'https://market.yandex.ru/offer/gXBC9f3VsTCE8tua_dKwkA?cpa=1&onstock=1'


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"class": "table table-striped table-bordered"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies


def get_session(proxy):
    session = requests.Session()
    session.proxies = {"http": proxy, "https": proxy}
    return session


def proxy_checking(proxies_list: list):
    response_status_code = None
    session_proxy = None
    while response_status_code != 200:
        proxy = ProxyIterate(proxies_list)
        proxy_now = next(proxy)
        session = get_session(proxy_now)
        print(proxy_now) # Раскомментировать при необходимости наблюдения процесса проверки прокси
        try:
            response = session.get("http://icanhazip.com", timeout=1.5)
            response_status_code = response.status_code
            session_proxy = proxy_now
        except Exception as e:
            continue
    return session_proxy


def class_definition(url: str, proxy):
    if re.findall(r'wildberries', url):
        result_parse = ParserWildberries(url, proxy)
        return result_parse.get_json()
    if re.findall(r'ozon', url):
        result_parse = ParserOzon(url, proxy)
        return result_parse.get_json()
    if re.findall(r'market.yandex', url):
        print('This functionality is under development')


class ProxyIterate():

    def __init__(self, proxies_list):
        self.proxies_list = proxies_list

    def __next__(self):
        self.proxy = random.choice(self.proxies_list)
        return self.proxy

    def __iter__(self):
        return self


class ParserWildberries():

    def __init__(self, url: str, proxy):
        self.url = url
        self.proxy = proxy

    def get_json(self):
        product_number = re.search(r'\d+', self.url)
        url_json = f'https://wbx-content-v2.wbstatic.net/ru/{product_number[0]}.json'
        proxies = {'http': self.proxy}
        try:
            response = requests.get(url_json, proxies=proxies)
            response.raise_for_status()
        except HTTPError:
            print(f'HTTP Error: {HTTPError}')
        except Exception as e:
            print(f'Exeption: {e}')
        else:
            return response.json()


class ParserOzon():

    def __init__(self, url: str, proxy):
        self.url = url
        self.proxy = proxy

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
        proxies = {'http': self.proxy}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/102.0.5005.63 Safari/537.36',
            'referer': self.url
        }
        try:
            session = requests.Session()
            response = session.get(url_request, params=params, headers=headers, timeout=5)
            print(response.status_code)
            response.raise_for_status()
        except HTTPError as he:
            print(f'HTTP Error {he}')
        except Exception as e:
            print(f'Exception: {e}')
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
        except Exception as e:
            print(f'Exception: {e}')
        else:
            return response


if __name__ == '__main__':
    proxy = proxy_checking(get_free_proxies())
    print(proxy)
    result_json = class_definition(url_wildberries, proxy)
    pprint(result_json)