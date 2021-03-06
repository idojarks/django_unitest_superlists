from django.test import TestCase
from django.urls import reverse
from lists.views import home_page
import urllib
from django.http import HttpRequest
from django.template.loader import render_to_string
import re
from lists.models import Item, List
from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from unittest import skip

from django.contrib.auth import get_user_model
User = get_user_model()

from lists.views import new_list
from unittest.mock import patch, Mock

class HomePageTest(TestCase):

    maxDiff = None

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def assertEqualExceptCSRF(self, html_code1, html_code2):
        return self.assertEqual(
            self.remove_csrf(html_code1),
            self.remove_csrf(html_code2)
        )
   
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
    
class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='another item 1', list=other_list)
        Item.objects.create(text='another item 2', list=other_list)

        response = self.client.get('/lists/%d/' % correct_list.id)

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'another item 1')
        self.assertNotContains(response, 'another item 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        new_item_text = '기존 목록에 신규 아이템'

        self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'text':new_item_text}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'text':'aa'}
        )

        self.assertRedirects(response, '/lists/%d/' % correct_list.id)

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.get('/lists/%d/' % correct_list.id)
        
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post('/lists/%d/' % list_.id, data={'text':''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_dupulicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post('/lists/%d/' % list1.id, data={'text':'textey'})
        
        expected_error = escape(DUPLICATE_ITEM_ERROR)

        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.count(), 1)

class NewListViewIntegratedTest(TestCase):

    def test_saving_a_POST_request(self):
        item_text = '신규 작업 아이템'
        
        # trailing slash, 꼬리 /
        # 사용하지 않는 경우 : DB를 바꾸는 '액션' URL, 파일
        # 사용하는 경우 : 디렉토리
        self.client.post('/lists/new', data={'text':item_text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.list, List.objects.first())

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text':'신규 작업 아이템'})
        list_ = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % list_.id)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        request = HttpRequest()
        request.user = User.objects.create(email='a@b.com')
        request.POST['text'] = 'item1'

        new_list(request)

        list_ = List.objects.first()
        self.assertEqual(list_.owner, request.user)

class MyListsTest(TestCase):


    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='idojarks@gmail.com')

        response = self.client.get('/lists/users/idojarks@gmail.com/')

        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@gmail.com')
        correct_user = User.objects.create(email='idojarks@gmail.com')
        
        response = self.client.get('/lists/users/idojarks@gmail.com/')

        self.assertEqual(response.context['owner'], correct_user)

@patch('lists.views.NewListForm')
@patch('lists.views.redirect')
class NewListViewUnitTest(TestCase):
    
    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new item'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockRedirect, mockNewListForm):
        new_list(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockRedirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    def test_redirects_to_form_returned_object_if_form_valid(self, mockRedirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        response = new_list(self.request)
        self.assertEqual(response, mockRedirect.return_value)
        mockRedirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(self, mockRender, mockRedirect, mockNewlistForm):
        mock_form = mockNewlistForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mockRender.return_value)
        mockRender.assert_called_once_with(self.request, 'home.html', {'form':mock_form})

    def test_does_not_save_if_form_invalid(self, mockRedirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        new_list(self.request)

        self.assertFalse(mock_form.save.called)