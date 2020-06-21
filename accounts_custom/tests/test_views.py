from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model, SESSION_KEY
from django.http import HttpRequest
from accounts_custom.views import login_custom
from importlib import import_module
from django.conf import settings

User = get_user_model()

class LoginViewTest(TestCase):

    # accounts_custom.views.authenticate 를 mock_authenticate 로 mocking
    @patch('accounts_custom.views.authenticate')
    def test_calls_authenticate_with_assertion_from_post(self, mock_authenticate):
        mock_authenticate.return_value = None
        self.client.post('/accounts_custom/login', data={'email':'idojarks@gmail.com'})
        mock_authenticate.assert_called_once_with('idojarks@gmail.com')

    @patch('accounts_custom.views.authenticate')
    def test_returns_OK_when_user_found(self, mock):
        user = User.objects.create(email='idojarks@gmail.com')
        user.backend = ''
        mock.return_value = user

        response = self.client.post('/accounts_custom/login', data={'email':'idojarks@gmail.com'})

        self.assertEqual(response.content.decode(), 'OK')

    @patch('accounts_custom.views.authenticate')
    def test_gets_logged_in_session_if_authenticate_returns_a_user(self, mock):
        user = User.objects.create(email='idojarks@gmail.com')
        user.backend = ''
        mock.return_value = user

        self.client.post('/accounts_custom/login', data={'email':'idojarks@gmail.com'})

        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))

    @patch('accounts_custom.views.authenticate')
    def test_does_not_get_logged_in_if_authenticate_returns_None(self, mock):
        mock.return_value = None

        self.client.post('/accounts_custom/login', data={'email':'idojarks@gmail.com'})

        self.assertNotIn(SESSION_KEY, self.client.session)

    @patch('accounts_custom.views.login')
    @patch('accounts_custom.views.authenticate')
    def test_calls_auth_and_login(self, mock_auth, mock_login):
        request = HttpRequest()
        request.POST['email'] = 'idojarks@gmail.com'
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        
        user = mock_auth.return_value
        user.backend = ''

        login_custom(request)

        mock_auth.assert_called_once_with(request.POST['email'])
        mock_login.assert_called_once_with(request, user)

        