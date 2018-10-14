from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery', views.index, name='gallery')
]
