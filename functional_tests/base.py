import time
from typing import Callable, Dict
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options as ChromeOptions

MAX_WAIT = 1  # seconds


class BaseTest(LiveServerTestCase):
    browser: webdriver.Chrome

    # Users
    MisterJones = {'username': 'MisterJones',
                   'password': 'MakeLoveNotWar1984'}

    Neo = {'username': 'Neo',
           'password': 'ThereIsNoSp00n'}


    def setUp(self) -> None:
        options = ChromeOptions()
        # options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)


    def tearDown(self) -> None:
        self.browser.quit()


    def send_info(self, inputbox: WebElement, info: str) -> None:
        inputbox.send_keys(info)
        inputbox.send_keys(Keys.ENTER)


    def wait_for(self, fn: Callable[[], None]):
        start_time = time.time()
        while True:
            try:
                return fn()
            except Exception as e:
                if time.time() - start_time > MAX_WAIT:
                    print(
                        '\n****************************************************************************************\n')
                    print(self.browser.page_source)
                    print(
                        '\n****************************************************************************************\n')

                    raise e
                time.sleep(0.1)


    def wait_for_row_in_list_table(self, row_text: str) -> None:

        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)


    def register_user(self, user: Dict[str, str]) -> None:
        self.browser.get(self.live_server_url + '/auth/register/')

        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys(user['username'])

        pass1_field = self.browser.find_element_by_id('id_password1')
        pass1_field.send_keys(user['password'])

        pass2_field = self.browser.find_element_by_id('id_password2')
        self.send_info(pass2_field, user['password'])


    def login_user(self, user: Dict[str, str]) -> None:
        self.browser.get(self.live_server_url + '/login/')

        self.wait_for(lambda: self.browser.find_element_by_id('id_username'))

        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys(user['username'])

        pass1_field = self.browser.find_element_by_id('id_password')
        self.send_info(pass1_field, user['password'])
