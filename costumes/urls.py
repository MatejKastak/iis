from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery', views.index, name='gallery'),
    path('costume/<int:costume_id>', views.costume, name='costume'),
    path('costume', views.costume_gallery, name='costume_gallery'),
    path('accessory/<int:accessory_id>', views.accessory, name='accessory'),
    path('accessory', views.accessory_gallery, name='accessory_gallery'),
    path('basket', views.basket, name='backet'),
    path('user', views.user, name='user'),
    path('settings', views.settings, name='setting'),
    path('borrowings', views.borrowings_gallery, name='borrowings_gallery'),
    path('borrowings/<int:borrowing_id>', views.borrowings, name='borrowings'),
    path('stores', views.stores_gallery, name='stores_gallery'),
    path('stores/<int:store_id>', views.stores, name='stores'),
]
