from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet


class TestCase(DjangoTestCase):

    @staticmethod
    def create_user(username, email, password=None):
        if password is None:
            password = 'generic password'
        return User.objects.create_user(username, email, password)

    @staticmethod
    def create_tweet(user, content=None):
        if content is None:
            content = 'default tweet content'
            return Tweet.objects.create(user=user, content=content)
