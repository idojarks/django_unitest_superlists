from .base import FunctionalTest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from unittest import skip

   
class NewVisitorTest(FunctionalTest):

    @skip
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 새로운 온라인 앱이 나왔다는 소식을 듣고
        # 그 앱을 확인하러 간다
        self.browser.get(self.server_url)

        # 웹 페이지 타이틀과 헤더가 'To-Do'라고 쓰였다
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('작업 목록 시작', header_text)

        # 작업 하나를 등록한다
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')

        # 텍스트 박스에 "밥 먹기"라고 쓴다
        inputbox.send_keys('밥 먹기')

        # 엔터 키를 누르면 페이지가 새로 바뀌고
        # "1: 밥 먹기" 항목이 보인다
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: 밥 먹기')

        # 다른 항목을 넣는다
        inputbox = self.get_item_input_box()
        inputbox.send_keys('이빨 닦기')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: 밥 먹기', [row.text for row in rows])
        self.assertIn('2: 이빨 닦기', [row.text for row in rows])
        
        # 페이지를 다시 갱신하고, 두 개 아이템이 목록에 보인다.
        self.check_for_row_in_list_table('2: 이빨 닦기')
        self.check_for_row_in_list_table('1: 밥 먹기')

        # 새로운 사용자인 프란시스가 사이트에 접속한다.
        
        ## 새로운 브라우저 세션을 이용해서 에디스의 정보가
        ## 쿠키를 통해 유입되는 상황을 방지한다
        self.browser.quit()
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

        # 프란시스가 홈페이지에 접속한다.
        # 에디스의 리스트는 보이지 않는다
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('밥 먹기', page_text)
        self.assertNotIn('이빨 닦기', page_text)

        # 프란시스가 새로운 작업 아이템을 입력하기 시작한다
        # 그는 에디스보다 재미가 없다
        inputbox = self.get_item_input_box()
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        # 프란시스가 전용 URL을 취득한다
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스가 입력한 흔적이 없음을 다시 확인한다
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('밥 먹기', page_text)
        self.assertNotIn('이빨 닦기', page_text)

        # 둘 다 만족하고 잠자리에 든다


        # 에디스는 메인 페이지를 방문한다
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # 그녀는 입력 상자가 가운데 배치됐음을 본다
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # 그녀는 새로운 리스트를 시작하고
        # 입력 상자가 가운데 배치됐음을 확인한다
        inputbox.send_keys('testing\n')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
