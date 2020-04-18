from django.views.generic import (CreateView, UpdateView)
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .forms import *
from django.http import JsonResponse


def get_user(request):
    user = request.user
    try:
        user = User.objects.get(id=user.id)
    except (ObjectDoesNotExist, TypeError) as e:
        response = JsonResponse({'error': f'{e}'})
        response.status_code = 406
        return response
    json_data = {
        'user_id': user.id,
        'username': user.username,
        'last_login': user.last_login
    }
    return JsonResponse({'response': json_data})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'user_app/registration.html', context=
    {'user_form': user_form,
     'registered': registered}, )
