from django.urls import path
from . import views


urlpatterns= [
    path('user_profile', views.user_profile, name='user_profile'),
    path('dashboard_user_profile', views.dashboard_user_profile, name='dashboard_user_profile'),
    path('terms', views.terms, name='terms'),
]