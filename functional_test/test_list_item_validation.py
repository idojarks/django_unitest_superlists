from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # 에디스는 메인 페이지에 접속해서 빈 아이템을 등록한다
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # 페이지가 새로고침되고
        # 빈 아이템을 등록할 수 없다는 에러 메시지가 나온다
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "빈 아이템을 등록할 수 없습니다.")

        # 다른 아이템을 입력하고 정상 처리
        self.browser.find_element_by_id('id_new_item').send_keys('우유 사기\n')
        self.check_for_row_in_list_table('1: 우유 사기')

        # 다시 빈 아이템을 등록한다
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # 리스트 페이지에 다시 에러 메시지가 나온다
        self.check_for_row_in_list_table('1: 우유 사기')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "빈 아이템을 등록할 수 없습니다.")

        # 아이템을 입력하면 정상 동작
        self.browser.find_element_by_id('id_new_item').send_keys('차 끓이기\n')
        self.check_for_row_in_list_table('1: 우유 사기')
        self.check_for_row_in_list_table('2: 차 끓이기')
