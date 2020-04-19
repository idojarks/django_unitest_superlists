from django.test import TestCase
from django.urls import reverse
from lists.views import home_page
import urllib

class HomePageTest(TestCase):
    def test_root_url_resolves_to_homepage_view(self):

        found = reverse('home')
        print('found : ', found)

        found = urllib.parse.quote(reverse('home'))
        print('found : ', found)
        
        self.assertEqual(found, '/')