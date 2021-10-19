from .base import BaseTest
from selenium.webdriver.common.keys import Keys
import unittest


class TestLoginPage(BaseTest):
    @unittest.skip
    def test_cant_create_incorrect_user(self):
        self.browser.get('login/')
        username_box = self.browser.find_element_by_id('id_username')
        self.send_info(username_box, 'A')
    
    
    def setUp(self) -> None:
        super().setUp()
        url_postfix = '/login/'
        self.login_url = self.live_server_url + url_postfix
    
    
    def test_correct_page(self):
        self.browser.get(self.login_url)
        self.assertTrue(self.browser.find_element_by_css_selector('h1').text == 'Login')
        self.assertTrue(self.browser.title == 'Login')
    
    
    def test_cant_send_empty_user(self):
        self.browser.get(self.login_url)
        
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys(Keys.ENTER)
        
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_username:invalid'))
    
    
    def test_cant_add_empty_password(self):
        self.browser.get(self.login_url)
        
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys('MisterJones')
        
        pass_field = self.browser.find_element_by_id('id_password')
        pass_field.send_keys(Keys.ENTER)
        
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_password:invalid'))
    
    
    def test_cant_add_improper_password(self):
        self.browser.get(self.login_url)
        
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys('MisterJones')
        
        pass_field = self.browser.find_element_by_id('id_password')
        pwd = '123'
        self.send_info(pass_field, pwd)
        
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_password:invalid'))
        
        error_text = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
        
        pass_field = self.browser.find_element_by_id('id_password')
        pwd = 'kitty'
        self.send_info(pass_field, pwd)
        
        self.wait_for(lambda: self.assertIn(error_text, self.browser.find_element_by_xpath("/html/body").text))
        
        pass_field = self.browser.find_element_by_id('id_password')
        pwd = 'Google123'
        self.send_info(pass_field, pwd)
        
        self.wait_for(lambda: self.assertIn(error_text, self.browser.find_element_by_xpath("/html/body").text))
    
    
    def test_redirects_from_login_if_logged_in_already(self):
        self.register_user(self.MisterJones)
        self.browser.get(self.login_url)
        
        header = self.wait_for(lambda: self.browser.find_element_by_id('header'))
        self.assertTrue(header.text == 'Hello! :) This is your simple To-Do app!\nPlease, check you tasks here',
                        header.text)
