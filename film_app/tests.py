from django.test import TestCase
from django.contrib.auth.models import User

# TODO: fix issue with
#  'Model class django.contrib.contenttypes.models.
#  ContentType doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.'

from .models import *

USERNAME = 'admin'
PASSWORD = 'admin23'


class ApiTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username=USERNAME,
            password=PASSWORD,
            is_superuser=True,
            is_staff=True,

        )

        self.film = Film.objects.create(
            title='Test Film',
            description='Test Description',
            poster='/image/film_app/posters/test_poster.jpg',
            year='2013',
            duration='90m',
            genres='genre1, genre2',
            url='http://test.url'
        )

        self.screenshot01 = Screenshots.objects.create(
            film=self.film,
            screenshot='/image/film_app/screens/test_screen01.jpg',
        )

        self.screenshot02 = Screenshots.objects.create(
            film=self.film,
            screenshot='/image/film_app/screens/test_screen02.jpg',
        )

        self.review = Review()
        self.review.user = self.user
        self.review.film = self.film
        self.review.title = 'Test Review Title'
        self.review.text = 'Test Review Text'
        self.review.date = '2020-04-18 09:21:47.158000'
        self.review.is_deleted = False
        self.review.save()

        self.like = ReviewLike()
        self.like.user = self.user
        self.like.review = self.review
        self.review.save()

    def testApiAddReview(self):
        self.client.login(USERNAME=USERNAME, PASSWORD=PASSWORD)

        # my_user = User.objects.get(id=1)
        # print('USER', my_user.username, my_user.password, my_user.is_superuser, my_user.user_permissions)

        response = self.client.post('/api/review/', {
            'user': self.user,
            'film': self.film,
            'title': 'Test Review Title02',
            'text': 'Test Review Text02',
            'date': '2020-03-18 09:22:47.158000',
            'is_deleted': False
        }, follow=True)

        print(f'RESPONSE = {response}')

        self.assertContains(
            response,
            text='',
            status_code=201
        )

        new_review = Review.objects.get(id=2)
        self.assertEqual('Test Review Title02', new_review.title)
        self.assertEqual('Test Review Text02', new_review.text)
