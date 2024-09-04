from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('service/', service, name='service'),
    path('team/', team, name='team'),
    path('login/', login, name='login'),
    path('registration/', register_page, name='register'),
    path('save/', save_user, name='save'),
]