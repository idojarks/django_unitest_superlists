from selenium.webdriver.support.wait import WebDriverWait
from .base import FunctionalTest
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from time import sleep

User = get_user_model()

class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)

        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        self.browser.get(self.server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session('idojarks@gmail.com')
        self.browser.get(self.server_url)


        self.get_item_input_box().send_keys('job 1\n')
        self.get_item_input_box().send_keys('job 2\n')
        first_list_url = self.browser.current_url

        self.browser.find_element_by_link_text('나의 목록').click()
        job1 = WebDriverWait(self.browser, 10).until(
            lambda b : b.find_element_by_link_text('job 1'))

        job1.click()

        self.wait_for(
            lambda : self.assertEqual(self.browser.current_url, first_list_url)
            )

        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('게임하기\n')
        second_list_url = self.browser.current_url

        myList = WebDriverWait(self.browser, 3).until(
            lambda b : b.find_element_by_link_text('나의 목록'))
        myList.click()

        myGame = WebDriverWait(self.browser, 3).until(
            lambda b : b.find_element_by_link_text('게임하기'))
        myGame.click()
        self.assertEqual(self.browser.current_url, second_list_url)

        logout = WebDriverWait(self.browser, 3).until(
            lambda b : b.find_element_by_id('id_logout'))
        logout.click()
        self.assertEqual(self.browser.find_elements_by_link_text('나의 목록'), [])

