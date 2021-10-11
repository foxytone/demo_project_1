from .base import BaseTest


class TestRegisterPage(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        url_postfix = '/auth/register'
        self.register_url = self.live_server_url + url_postfix


    def test_correct_page(self):
        self.browser.get(self.register_url)
        self.assertTrue(self.browser.find_element_by_css_selector('h1').text == 'Registration')
        self.assertTrue(self.browser.title == 'Registration')


    def test_cant_register_with_empty_username(self):
        self.browser.get(self.register_url)

        username_field = self.browser.find_element_by_id('id_username')
        self.send_info(username_field, '')

        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_username:invalid'))


    def test_cant_register_without_password1(self):
        self.browser.get(self.register_url)

        username_field = self.browser.find_element_by_id('id_username')
        self.send_info(username_field, 'MisterJones')

        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_password1:invalid'))


    def test_cant_register_without_password2(self):
        self.browser.get(self.register_url)

        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys('MisterJones')

        pass1_field = self.browser.find_element_by_id('id_password1')
        self.send_info(pass1_field, 'MakeLoveNotWar1984')

        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_password2:invalid'))


    def test_cant_register_with_incorrect_passwords(self):
        self.browser.get(self.register_url)

        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys('MisterJones')

        pass1_field = self.browser.find_element_by_id('id_password1')
        pass1_field.send_keys('MakeLoveNotWar1984')

        pass2_field = self.browser.find_element_by_id('id_password2')
        self.send_info(pass2_field, 'DifferentPassword123')

        self.wait_for(lambda: self.browser.find_element_by_id('error_1_id_password2'))


    def test_can_register_proper_user(self):
        self.browser.get(self.register_url)

        user = 'MisterJones'
        password = ('MakeLoveNotWar1984')

        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys(user)

        pass1_field = self.browser.find_element_by_id('id_password1')
        pass1_field.send_keys(password)

        pass2_field = self.browser.find_element_by_id('id_password2')
        self.send_info(pass2_field, password)

        self.wait_for(lambda: self.browser.find_element_by_id('account_navbar'))
        self.wait_for(lambda: self.assertTrue(self.browser.find_element_by_id('account_navbar').text == user))
