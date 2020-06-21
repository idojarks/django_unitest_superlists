from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(models.Model):

    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    
    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        return True

    @is_authenticated.setter
    def is_authenticated(self, auth):
        pass
