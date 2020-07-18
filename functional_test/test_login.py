from selenium.webdriver.support.wait import WebDriverWait
from .base import FunctionalTest
import time
from unittest import skip

class LoginTest(FunctionalTest):

    def test_sign_up_with_google(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_signup').click()
        self.wait_for_element_with_id('id_username')
        WebDriverWait(self.browser, 10).until(
            lambda b : b.find_element_by_id('id_username'))

        username = 'idojarks'

        self.browser.find_element_by_id('id_username').send_keys(username)
        self.browser.find_element_by_id('id_email').send_keys('idojarks@gmail.com')
        self.browser.find_element_by_id('id_password1').send_keys('yong4866')
        self.browser.find_element_by_id('id_password2').send_keys('yong4866')
        self.browser.find_element_by_css_selector("button[type='submit']").click()

        navbar = WebDriverWait(self.browser, 10).until(
            lambda b : b.find_element_by_css_selector('.navbar'))
        self.assertIn(username, navbar.text)

   