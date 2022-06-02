from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.wildberries.ru/catalog/18256273/detail.aspx?targetUrl=MI'
EXE_PATH = 'chromedriver.exe'


class SelectInSelenium():

    def __init__(self, exe_path):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.exe_path = exe_path
        self.driver = webdriver.Chrome(executable_path=EXE_PATH, options=chrome_options)


class ParserWildberries(SelectInSelenium):

    def __init__(self, url, exe_path):
        super().__init__(exe_path)
        self.url = url

    def getting_page_code(self):
        self.driver.get(self.url)
        photo_li = self.driver.find_element_by_xpath(".//div[@class='collapsable__content']")
        # for elem in photo_li:
        #     print(elem)
        print(photo_li.text)

parse_test = ParserWildberries(url, EXE_PATH)
parse_test.getting_page_code()