from django.test import TestCase
from accounts2.authentication import CustomAuthenticationBackend, VERIFY_URL
from unittest.mock import patch
from django.contrib.auth import get_user_model

USER_EMAIL = 'idojarks@gmail.com'
User = get_user_model()

@patch('accounts2.authentication.requests.post')
class AuthenticateTest(TestCase):

    def setUp(self):
        self.backend = CustomAuthenticationBackend()
        self.user = User(email=USER_EMAIL)
        self.user.username = 'idojarks'
        self.user.save()
    
    def test_sends_email_to_verify_server_with_domain(self, mock_post):
        self.backend.authenticate(VERIFY_URL, USER_EMAIL)

        mock_post.assert_called_once_with(VERIFY_URL, data=USER_EMAIL)

    def test_returns_none_if_response_errors(self, mock_post):
        # mock_post.return_value 도 mock 이다
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}

        user = self.backend.authenticate(VERIFY_URL, USER_EMAIL)
        
        self.assertIsNone(user)

    def test_returns_none_if_status_not_okay(self, mock_post):
        mock_post.return_value.json.return_value = {'status':'not okay!'}

        user = self.backend.authenticate(VERIFY_URL, USER_EMAIL)

        self.assertIsNone(user)

    def test_finds_exsinting_user_with_email(self, mock_post):
        mock_post.return_value.json.return_value = {'status':'okay', 'email':USER_EMAIL}
        actual_user = self.user
        found_user = self.backend.authenticate(VERIFY_URL, USER_EMAIL)
        self.assertEqual(found_user, actual_user)

    def test_creates_new_user_if_necessary(self, mock_post):
        mock_post.return_value.json.return_value = {'status':'okay', 'email':'a@b.c'}
        found_user = self.backend.authenticate(VERIFY_URL, 'a@b.c')
        new_user = User.objects.get(email='a@b.c')
        self.assertEqual(found_user, new_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        backend = CustomAuthenticationBackend()
        other_user = User(email='other@user.com')
        other_user.username = 'otheruser'
        other_user.save()
        desired_user = User.objects.create(email='a@b.c')
        found_user = backend.get_user('a@b.c')

        self.assertEqual(found_user, desired_user)

    def test_returns_none_if_no_user_with_that_email(self):
        backend = CustomAuthenticationBackend()
        self.assertIsNone(backend.get_user('a@b.c'))
        

