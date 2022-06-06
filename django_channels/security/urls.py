from django.urls import path
from . import views


urlpatterns= [
    path('logout', views.logoutUser, name='logout'),
    path('login', views.loginPage, name='login'),
    path('register', views.registerPage, name='register'),
    
]
