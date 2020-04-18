from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *


class ReviewViewSet (ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        return super (ReviewViewSet, self).list(request, *args, **kwargs)


class ReviewLikeViewSet(ModelViewSet):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer
