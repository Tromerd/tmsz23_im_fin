from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView)
from .forms import *


def index(request):
    return render(request, 'film_app/base.html', context={
        'text': 'This app loads films from http://kinogo-net.org/ru/',
        'update_films': True,
    })


class FilmListView(ListView):
    template_name = 'film_app/films.html'
    model = Film
    context_object_name = 'films'
    paginate_by = 10

    def get_queryset(self):
        return Film.objects.all()

    def get_paginate_by(self, queryset):
        page_number = self.request.GET.get('page_number')
        if page_number is not None:
            self.paginate_by = page_number
        return super(FilmListView, self).get_paginate_by(self.queryset)


class FilmDetailsView(DetailView):
    template_name = 'film_app/film.html'
    model = Film

    def get_context_data(self, *args, **kwargs):
        screens = Screenshots.objects.filter(film_id=self.kwargs['pk'])
        img = []
        for screen in screens:
            img.append(screen.screenshot)
        reviews = Review.objects.filter(film_id=self.kwargs['pk'])
        # TODO: extend context with number of likes for each review (move to separate function (reusing in another view)
        rws = []
        for review in reviews:
            rws.append(review)
        context = super().get_context_data(**kwargs)
        context['screens'] = img
        context['reviews'] = rws
        return context


class ReviewDetailsView(DetailView):
    template_name = 'film_app/review.html'
    model = Review

    def get_context_data(self, *args, **kwargs):
        likes_count = ReviewLike.objects.filter(review_id=self.kwargs['pk']).count()
        context = super().get_context_data(**kwargs)
        context['likes_count'] = likes_count
        return context


class ReviewListView(ListView):
    template_name = 'film_app/reviews.html'
    model = Review
    context_object_name = 'all_reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.all()

    # TODO: extend context with number of likes for each review
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# TODO:
#  1) pass values from User and User models
#  2) change template
class LikedReviewListView(ListView):
    template_name = 'film_app/liked_reviews.html'
    model = ReviewLike
    context_object_name = 'liked_reviews'
    paginate_by = 10

    def get_queryset(self):
        return ReviewLike.objects.all()

    def get_paginate_by(self, queryset):
        page_number = self.request.GET.get('page_number')
        if page_number is not None:
            self.paginate_by = page_number
        return super(LikedReviewListView, self).get_paginate_by(self.queryset)
