from django.contrib import admin
from .models import *

film_models = (
    Film,
    Screenshots,
    Review,
    ReviewLike
)

for el in film_models:
    admin.site.register(el)