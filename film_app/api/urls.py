from rest_framework import routers
from django.conf.urls import include
from django.urls import path

from . import views

router = routers.DefaultRouter()
router.register('review', views.ReviewViewSet)
router.register('like_review', views.ReviewLikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]