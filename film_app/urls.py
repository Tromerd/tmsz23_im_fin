from django.urls import path, include
from .views import (
    index,
    FilmListView,
    FilmDetailsView,
    ReviewListView,
    ReviewDetailsView,
    LikedReviewListView,
)

# TODO: resolve problem 'attempted relative import beyond top-level package'
# from ..parser import kinogo_parser

from .stub_parser import foo

app_name = 'film_app'

urlpatterns = [
    path('', index, name='index'),
    path('films/', FilmListView.as_view(), name='films'),
    path('film/<int:pk>/', FilmDetailsView.as_view(), name='film'),
    path('review/<int:pk>/', ReviewDetailsView.as_view(), name='review'),
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('liked_reviews/', LikedReviewListView.as_view(), name='liked_reviews'),
    path('api/', include('film_app.api.urls')),
    path('run/', foo, name='run'),
]
