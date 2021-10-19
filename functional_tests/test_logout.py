from .base import BaseTest


class TestLogout(BaseTest):
    def test_correct_redirect_and_logout(self):
        self.register_user(self.MisterJones)

        # Registered, wait for account name on top left
        username = self.wait_for(lambda: self.browser.find_element_by_id('account_navbar'))
        self.assertTrue(username.text == self.MisterJones['username'])

        # Logout, wait for 'Login' element
        self.browser.get(self.live_server_url + '/logout/')
        self.wait_for(lambda: self.browser.find_element_by_id('login_navbar'))
