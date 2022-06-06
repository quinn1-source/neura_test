from django.urls import path
from . import views


urlpatterns= [
        #path('', views.index, name='index'),
        path('', views.home_screen_view, name='home'),

]
