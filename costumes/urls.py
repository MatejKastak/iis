from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery', views.index, name='gallery'),
    path('login', views.login, name='login'),
    path('login/script', views.login_script, name='login'),
    path('costumes', views.costumes_gallery, name='costumes_gallery'),
    path('costumes/<int:costume_id>', views.costumes, name='costumes'),
    path('accessories/<int:accessory_id>', views.accessories, name='accessories'),
    path('accessories', views.accessories_gallery, name='accessories_gallery'),
    path('basket', views.basket, name='backet'),
    path('user', views.user, name='user'),
    path('settings', views.settings, name='setting'),
    path('borrowings', views.borrowings_gallery, name='borrowings_gallery'),
    path('borrowings/<int:borrowing_id>', views.borrowings, name='borrowings'),
    path('stores', views.stores_gallery, name='stores_gallery'),
    path('stores/<int:store_id>', views.stores, name='stores'),
]
