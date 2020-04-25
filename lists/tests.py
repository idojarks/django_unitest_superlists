from django.test import TestCase
from django.urls import reverse
from lists.views import home_page
import urllib
from django.http import HttpRequest
from django.template.loader import render_to_string
import re

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

    def assertalExceptCSRF(self, html_code1, html_code2):
        return self.assertEqual(
            self.remove_csrf(html_code1),
            self.remove_csrf(html_code2)
        )


    def test_root_url_resolves_to_homepage_view(self):
        found = reverse('home')
        #print('found : ', found)

        found = urllib.parse.quote(reverse('home'))
        #print('found : ', found)
        
        self.assertEqual(found, '/')

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        expected_html = render_to_string('home.html',
            {'new_item_text':'신규 작업 아이템'})
        self.assertEqualExceptCSRF(expected_html, response.content.decode())

    def test_homepage_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'aa'

        response = home_page(request)

        expected_html = render_to_string(
            'home.html', 
            {'new_item_text': 'aa'})
        self.assertEqualExceptCSRF(expected_html, response.content.decode())