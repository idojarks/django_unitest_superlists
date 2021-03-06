from time import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys
from unittest import skip
from selenium.webdriver.support.ui import WebDriverWait
import os
from datetime import datetime
from selenium.common.exceptions import WebDriverException

SCREEN_DUMP_LOCATION = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'screendumps')
)

class FunctionalTest(StaticLiveServerTestCase):
   
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                cls.live_server_url = cls.server_url
                return

        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        #self.browser = webdriver.Chrome(ChromeDriverManager().install())        
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\yong\.wdm\drivers\chromedriver\83.0.4103.39\win32\chromedriver.exe")        
        
        #self.browser.implicitly_wait(3)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()

        #self.browser.refresh()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':','.') #[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def get_error_element(self):
        return self.browser.find_element_by_id('id_err_text')
        #return self.browser.find_element_by_css_selector('.has-error')

    def is_inputbox_valid(self):
        inputbox = self.get_item_input_box()

        validation_message = inputbox.get_attribute("validationMessage")
        if validation_message == None:
            return False

        # 브라우저가 폼 유효성 검사 기능을 제공하는지 확인
        script = "return Modernizr.formvalidation"

        # 아래 코드는 동작하지 않는다
        # self.browser.execute_script(script) == None 
        # Modernizr 공부가 필요하다
        if self.browser.execute_script(script) == False:
            script = "return arguments[0].willValidate;"
            if self.browser.execute_script(script, inputbox) == True and \
                inputbox.get_attribute('textContent') == '':
                return False

        '''
        validity
        {
            badInput: false,
            customError: false,
            patternMismatch: false,
            rangeOverflow: false,
            rangeUnderflow: false,
            stepMismatch: false,
            tooLong: false,
            typeMismatch: false,
            valid: false,
            valueMissing: true
        }
        '''
        script = "return arguments[0].validity.valid;"
        return self.browser.execute_script(script, inputbox)

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=3).until(
                lambda b: b.find_element_by_id(element_id)
            )

    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def wait_for(self, function_with_assertion, timeout=3):
        start_time = time()
        while time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)
        return function_with_assertion()