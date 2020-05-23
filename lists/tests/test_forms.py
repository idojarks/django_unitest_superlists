from django.test import TestCase
from lists.forms import ItemForm, EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from lists.models import Item, List
from html5print import HTMLBeautifier

class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="작업 아이템 입력"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        # key : 필드 네임
        # value : 필드 값, 타입은 대부분 string
        data = {
            'text': '',
        }
        form = ItemForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'], 
            [EMPTY_LIST_ERROR]
        )

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text':'do me'})
        new_item = form.save(for_list=list_)

        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)

class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="작업 아이템 입력"', form.as_p())

    def test_form_validation_for_blank_items(self):
        data = {
            'text': '',
        }
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_form_validation_for_duplicate_items(self):
        data = {
            'text': 'aa',
        }
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='aa')
        form = ExistingListItemForm(for_list=list_, data=data)
        self.assertFalse(form.is_valid())
        #print(HTMLBeautifier.beautify(form.as_p(), 4))
        
        # ErrorDict.__str__() 호출
        # html의 ul 태그 형식으로 출력
        #print(form.errors)

        # errors : ErrorDict
        #   key : field name
        #   value : error
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.first())