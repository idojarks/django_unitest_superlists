from .base import FunctionalTest
from selenium.webdriver.common.by import By
from lists.forms import DUPLICATE_ITEM_ERROR
from unittest import skip
import time

class ItemValidationTest(FunctionalTest):

    
    def test_cannot_add_empty_list_items(self):
        # 에디스는 메인 페이지에 접속해서 빈 아이템을 등록한다
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # 페이지가 새로고침되고
        # 빈 아이템을 등록할 수 없다는 에러 메시지가 나온다
        self.assertFalse(self.is_inputbox_valid())

        # 다른 아이템을 입력하고 정상 처리
        self.get_item_input_box().send_keys('우유 사기\n')
        self.check_for_row_in_list_table('1: 우유 사기')

        # 다시 빈 아이템을 등록한다
        self.get_item_input_box().send_keys('\n')

        # 리스트 페이지에 다시 에러 메시지가 나온다
        self.check_for_row_in_list_table('1: 우유 사기')
        self.assertFalse(self.is_inputbox_valid())

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

        #time.sleep(300)

        error = self.get_error_element()

        # 유닛 테스트할 때 form-group has-error 가 style=hide 때문에 보이지 않음
        # selinium 은 보이는 요소만 정상 작동
        # error.text 는 값이 없음
        # get_attribute() 로 text 값을 얻어 와야 함
        self.assertEqual(error.get_attribute('textContent'), DUPLICATE_ITEM_ERROR)

    
    def test_error_messages_are_cleared_on_input(self):
        # 에디스는 검증 에러를 발생시키도록 신규 목록을 시작한다
        self.browser.get(self.server_url)

        self.get_item_input_box().send_keys('\n')
        
        self.assertFalse(self.is_inputbox_valid())
        
        #time.sleep(300)
