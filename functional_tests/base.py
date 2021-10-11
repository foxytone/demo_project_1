from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import time
from typing import Callable
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 2  # seconds


class BaseTest(LiveServerTestCase):
    browser: webdriver.Firefox


    def setUp(self) -> None:
        options = FirefoxOptions()
        options.add_argument('--headless')
        self.browser = webdriver.Firefox(options=options)


    def tearDown(self) -> None:
        self.browser.quit()


    def send_info(self, inputbox: WebElement, info: str) -> None:
        inputbox.send_keys(info)
        inputbox.send_keys(Keys.ENTER)


    def wait_for(self, fn: Callable[[], None]) -> None:
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise (e, 'probably need to increase MAX_WAIT + ')
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
