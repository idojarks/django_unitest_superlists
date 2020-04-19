from django.test import TestCase
from django.urls import reverse
from lists.views import home_page
import urllib
from django.http import HttpRequest
from django.template.loader import render_to_string

class HomePageTest(TestCase):
    def test_root_url_resolves_to_homepage_view(self):
        found = reverse('home')
        #print('found : ', found)

        found = urllib.parse.quote(reverse('home'))
        #print('found : ', found)
        
        self.assertEqual(found, '/')

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')

        # response.content는 byte type.
        #self.assertTrue(response.content.startswith(b'<html>'))
        #self.assertIn(b'<title>To-Do</title>', response.content)
        #self.assertTrue(response.content.endswith(b'</html>'))
        self.assertEqual(expected_html, response.content.decode())