from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.functions import datetime
from django.urls import reverse


class Film(models.Model):
    title = models.CharField(max_length=256, blank=False, verbose_name='Title')
    url = models.URLField(max_length=256, blank=False, verbose_name='Kinogo URL')
    description = models.TextField(max_length=2048, blank=True, verbose_name='Description')
    poster = models.ImageField(
        upload_to='image/film_app/posters/',
        default=None, blank=True, null=True, verbose_name='Poster')
    year = models.CharField(max_length=24, default=None, blank=True, null=True, verbose_name='Year')
    duration = models.CharField(max_length=256, blank=True, verbose_name='Duration')
    genres = models.CharField(max_length=512, blank=True, verbose_name='Genres')

    def __str__(self):
        return f'{self.title} - {self.year}'

    def get_absolute_url(self):
        return reverse('film_app:film', args=(self.id,))

    class Meta:
        verbose_name = 'Film'
        verbose_name_plural = 'Films'
        ordering = ('title', 'year', 'duration')


class Screenshots(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    screenshot = models.ImageField(
        upload_to='image/film_app/screens/',
        default=None, blank=True, null=True, verbose_name='Screenshot')

    class Meta:
        verbose_name = 'Screenshot'
        verbose_name_plural = 'Screenshots'


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: fix
    #  1) 'OverflowError: Python int too large to convert to C long' problem with datefield
    #  2) problem with date formatting
    date = models.DateTimeField(verbose_name='Date', default=datetime.datetime.now, blank=True, null=True)
    # date = models.DateField(verbose_name='Date', default=datetime.datetime.now, blank=True, null=True)
    title = models.CharField(max_length=256, blank=False, verbose_name='Title')
    text = models.TextField(max_length=10112, verbose_name='Text')
    is_deleted = models.BooleanField(default=False, verbose_name='Deleted')

    def get_absolute_url(self):
        return reverse('film_app:review', args=(self.id,))

    def delete(self, using=None, keep_parents=True):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f'Review "{self.title}" added "{self.date}" for "{self.film}" by "{self.user}"'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ('film', 'user',)


class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('film_app:review', args=self.review)
