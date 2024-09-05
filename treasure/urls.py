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
    path('connexion/', connexion, name='connexion'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', user_profile, name='profile'),
    path('update_image/', update_image, name='update_image'),
    path('update_profile/', update_profile, name='update_profile'),
    path('manage_recap/', manage_recap, name='manage_recap'),
    path('recap_show/', recap_show, name='recap_show'),
    path('delete_recap/', delete_recap, name='delete_recap'),
    path('add_new_report/', add_new_report, name='add_new_report'),
    path('update_recap/', update_recap, name='update_recap'),
]
