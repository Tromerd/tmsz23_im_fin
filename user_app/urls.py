from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import get_user, register
from django.conf.urls import url

app_name = 'user_app'


urlpatterns = [
    path('login/', LoginView.as_view(template_name='user_app/login.html'),
         name='login'),
    # path('register/', RegisterView.as_view(template_name='/user_app/login'),
    #      name='login'),
    path('logout/', LogoutView.as_view(next_page='/user_app/login'),
         name='logout'),
    path('get_user/', get_user, name='user_json'),
    path('register/', register, name='register'),
    #url(r'^register/$', register, name='user_app/register'),
]