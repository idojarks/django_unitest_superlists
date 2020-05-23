from .base import FunctionalTest
from selenium.webdriver.common.by import By
from lists.forms import DUPLICATE_ITEM_ERROR

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # 에디스는 메인 페이지에 접속해서 빈 아이템을 등록한다
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # 페이지가 새로고침되고
        # 빈 아이템을 등록할 수 없다는 에러 메시지가 나온다
        #error = self.get_error_element()
        #self.assertEqual(error.text, "You can't have an empty list item")

        # 다른 아이템을 입력하고 정상 처리
        self.get_item_input_box().send_keys('우유 사기\n')
        self.check_for_row_in_list_table('1: 우유 사기')

        # 다시 빈 아이템을 등록한다
        self.get_item_input_box().send_keys('\n')

        # 리스트 페이지에 다시 에러 메시지가 나온다
        self.check_for_row_in_list_table('1: 우유 사기')
        #error = self.get_error_element()
        #self.assertEqual(error.text, "You can't have an empty list item")

        # 아이템을 입력하면 정상 동작
        self.get_item_input_box().send_keys('차 끓이기\n')
        self.check_for_row_in_list_table('1: 우유 사기')
        self.check_for_row_in_list_table('2: 차 끓이기')

    def test_cannot_add_duplicate_items(self):
        # 에디스는 메인 페이지로 돌아가서 신규 목록을 시작한다.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('콜라 사기\n')
        self.check_for_row_in_list_table('1: 콜라 사기')

        # 실수로 중복 아이템을 입력한다.
        self.get_item_input_box().send_keys('콜라 사기\n')

        # 에러 메시지를 본다.
        self.check_for_row_in_list_table('1: 콜라 사기')
        error = self.get_error_element()
        self.assertEqual(error.text, DUPLICATE_ITEM_ERROR)