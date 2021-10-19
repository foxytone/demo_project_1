from .base import BaseTest


class TestHomePage(BaseTest):
    def test_home_page_is_loaded_for_unlogged_user(self):
        self.browser.get(self.live_server_url)

        self.wait_for(lambda: self.browser.find_element_by_id('login_navbar'))
        header = self.browser.find_element_by_id('header')
        self.assertTrue(header.text == "Hello! :) This is your simple To-Do app!\n"
                                       "Please, login or register to start use your tasks!", repr(header.text))


    def test_home_page_is_loaded_fo_logged_user(self):
        self.register_user(self.MisterJones)
        self.browser.get(self.live_server_url)
        self.wait_for(lambda: self.browser.find_element_by_id('logout_navbar'))
        header = self.browser.find_element_by_id('header')
        self.assertTrue(header.text == "Hello! :) This is your simple To-Do app!\n"
                                       "Please, check you tasks here")
