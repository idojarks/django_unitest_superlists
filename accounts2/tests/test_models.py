from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest import skip


User = get_user_model()

class UserModelTest(TestCase):

    # google login을 쓸 때에는 skip
    @skip
    def test_user_is_valid_with_email_only(self):
        user = User(email='idojarks@gmail.com')
        user.full_clean()

    # google login을 쓸 때에는 skip
    @skip
    def test_email_is_pk(self):
        user = User()
        self.assertFalse(hasattr(user, 'id'))

    def test_is_authenticated(self):
        user = User()
        self.assertTrue(user.is_authenticated)