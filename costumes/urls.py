from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery', views.index, name='gallery'),
    path('logout', views.logout_page, name='logout_page'),
    path('login', views.login_page, name='login'),
    path('login/script', views.login_script, name='login'),
    path('register', views.register, name='register'),
    path('register/script', views.register_script, name='register'),
    path('manage_employee', views.manage_employee, name='manage_employee'),
    path('manage_manager', views.manage_manager, name='manage_manager'),
    path('edit_manager/<int:manager_id>', views.edit_manager, name='manage_manager'),
    path('edit_manager/script', views.edit_manager_script, name='manage_manager'),

    path('costumes/<int:costume_id>', views.costumes, name='costumes'),
    path('costumes/<int:costume_id>/edit', views.costumes_edit, name='costumes_edit'),
    path('costumes/<int:costume_id>/delete', views.costumes_delete, name='costumes_delete'),
    path('costumes/<int:costume_id>/duplicate', views.costumes_duplicate, name='costumes_duplicate'),
    path('add_costume', views.add_costume.as_view(success_url='/gallery'), name='add_costume'),
    path('add_costume_template', views.add_costume_template.as_view(), name='add_costume_template'),

    path('accessories/<int:accessory_id>', views.accessories, name='accessories'),
    path('accessories/<int:accessory_id>/edit', views.accessories_edit, name='accessories_edit'),
    path('accessories/<int:accessory_id>/delete', views.accessories_delete, name='accessories_delete'),
    path('accessories/<int:accessory_id>/duplicate', views.accessories_duplicate, name='accessories_duplicate'),
    path('add_accessory', views.add_accessory.as_view(success_url='/gallery'), name='add_accessory'),

    path('basket', views.basket, name='backet'),
    path('user', views.user, name='user'),
    path('settings', views.settings, name='setting'),
    path('borrowings', views.borrowings_gallery, name='borrowings_gallery'),
    path('borrowings/<int:borrowing_id>', views.borrowings, name='borrowings'),
    path('borrowings/<int:accessory_id>/edit', views.borrowings_edit, name='borrowings_edit'),
    path('borrowings/<int:accessory_id>/delete', views.borrowings_delete, name='borrowings_delete'),
    path('stores', views.stores_gallery, name='stores_gallery'),
    path('stores/<int:store_id>', views.stores, name='stores'),
]
