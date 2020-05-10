from django.test import TestCase
from django.urls import reverse
from lists.views import home_page
import urllib
from django.http import HttpRequest
from django.template.loader import render_to_string
import re
from lists.models import Item, List
from django.utils.html import escape

class HomePageTest(TestCase):
    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def assertEqualExceptCSRF(self, html_code1, html_code2):
        return self.assertEqual(
            self.remove_csrf(html_code1),
            self.remove_csrf(html_code2)
        )
    

    def test_root_url_resolves_to_homepage_view(self):
        found = reverse('home')
        found = urllib.parse.quote(reverse('home'))
        
        self.assertEqual(found, '/')
    
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
            data={'item_text':new_item_text}
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
            data={'item_text':'aa'}
        )

        self.assertRedirects(response, '/lists/%d/' % correct_list.id)

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.get('/lists/%d/' % correct_list.id)
        
        self.assertEqual(response.context['list'], correct_list)

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % list_.id, 
            data={'item_text':''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        item_text = '신규 작업 아이템'
        
        # trailing slash, 꼬리 /
        # 사용하지 않는 경우 : DB를 바꾸는 '액션' URL, 파일
        # 사용하는 경우 : 디렉토리
        self.client.post('/lists/new', data={'item_text':item_text})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.list, List.objects.first())

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text':'신규 작업 아이템'})
        list_ = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % list_.id)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        #print(response.content.decode())
        #print(expected_error)
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

