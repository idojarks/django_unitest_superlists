from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())        
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 새로운 온라인 앱이 나왔다는 소식을 듣고
        # 그 앱을 확인하러 간다
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더가 'To-Do'라고 쓰였다
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 작업 하나를 등록한다
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')

        # 텍스트 박스에 "밥 먹기"라고 쓴다
        inputbox.send_keys('밥 먹기')

        # 엔터 키를 누르면 페이지가 새로 바뀌고
        # "1: 밥 먹기" 항목이 보인다
        inputbox.send_keys(Keys.ENTER)

        # 다른 항목을 넣는다
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('이빨 닦기')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: 밥 먹기', [row.text for row in rows])
        self.assertIn('2: 이빨 닦기', [row.text for row in rows])
        
        # 항목을 더 쓸 수 있는 여분의 텍스트 박스가 있다
        # 그곳에 "씻기"라고 쓴다
        self.fail('Finish the test.')

        # 페이지가 새로 바뀌고, 두 개의 항목이 보인다
        # 입력한 내용이 저장되는지 궁금하다
        # 사이트는 그녀가 쓸 URL을 만들어준다
        # 그리고 URL의 설명도 함께 제공한다

        # 안내 받은 URL로 접속하면 내가 만든 작업 목록을 볼 수 있다



