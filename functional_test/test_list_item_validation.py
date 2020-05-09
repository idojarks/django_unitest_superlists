from .base import FunctionalTest
from unittest import skip

class ItemValidationTest(FunctionalTest):

    @skip
    def test_cannot_add_empty_list_items(self):
        pass