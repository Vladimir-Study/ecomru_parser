from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

url = 'https://www.wildberries.ru/catalog/18256273/detail.aspx?targetUrl=MI'


class SelectInSelenium():

    def __init__(self):
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # self.exe_path = exe_path
        self.driver = webdriver.Chrome()


class ParserWildberries(SelectInSelenium):

    def __init__(self, url):
        # super().__init__(exe_path)
        super().__init__()
        self.url = url

    def getting_page_code(self):
        self.driver.get(self.url)
        title = self.driver.find_element(By.CSS_SELECTOR, "h1")
        print(title.text)
        self.driver.close()


parse_test = ParserWildberries(url)
parse_test.getting_page_code()
