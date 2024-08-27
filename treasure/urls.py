from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('service/', service, name='service'),
    path('team/', team, name='team'),
    path('why/', why, name='why')
]