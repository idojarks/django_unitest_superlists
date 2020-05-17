from .base import FunctionalTest
from unittest import skip

class LayoutAndStylingTest(FunctionalTest):

    @skip
    def test_layout_and_styling(self):
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



    @skip
    def test_cannot_add_empty_list_items(self):
        pass