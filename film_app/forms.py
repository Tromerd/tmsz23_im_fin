from django import forms
from .models import *


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'text', 'date', 'user')


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = '__all__'
