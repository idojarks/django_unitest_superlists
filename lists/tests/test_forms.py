import unittest
from unittest.case import skip
from django.test import TestCase
from lists.forms import (
    ItemForm,
    EMPTY_LIST_ERROR,
    DUPLICATE_ITEM_ERROR,
    ExistingListItemForm,
    NewListForm,
)
from lists.models import Item, List
from html5print import HTMLBeautifier
from unittest.mock import patch, Mock

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

class NewListFormTest(TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(self, mock_List_create_new):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text':'item1'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(first_item_text='item1')

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_if_user_authenticated(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text':'item1'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(first_item_text='item1', owner=user)

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(self, mock_List_create_new):
        owner = Mock(is_authenticated=True)
        form = NewListForm(data={'text':'item1'})
        form.is_valid()
        list_ = form.save(owner)
        self.assertEqual(list_, mock_List_create_new.return_value)
