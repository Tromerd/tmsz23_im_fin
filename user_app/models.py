from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class User(User):
    def get_absolute_url(self):
        return reverse('user_app:account', args=(self.id,))