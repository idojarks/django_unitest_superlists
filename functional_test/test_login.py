from .base import FunctionalTest
import time

class LoginTest(FunctionalTest):

    def test_login_with_google(self):
        res = self.browser.get(self.server_url)
        print('response: ',res)
        
        self.browser.find_element_by_id('id_register').click()
        #time.sleep(1000)
        
        #self.wait_for_element_with_id('id_logout')
        #self.switch_to_new_window('To-Do')

        username = 'idojarks'

        self.browser.find_element_by_id('id_username').send_keys(username)
        self.browser.find_element_by_id('id_email').send_keys('idojarks@gmail.com')
        self.browser.find_element_by_id('id_password1').send_keys('yong4866')
        self.browser.find_element_by_id('id_password2').send_keys('yong4866')
        self.browser.find_element_by_css_selector("button[type='submit']").click()

        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(username, navbar.text)