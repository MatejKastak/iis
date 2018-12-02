from django.urls import path

from . import views, views_managment

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery', views.index, name='gallery'),
    path('logout', views.logout_page, name='logout_page'),
    path('login', views.login_page, name='login'),
    path('login/script', views.login_script, name='login'),
    path('register', views.register, name='register'),
    path('register/script', views.register_script, name='register'),
    path('edit_user', views.edit_user, name='edit_user'),
    path('edit_user/script', views.edit_user_script, name='edit_user'),
    path('user_change_password', views.change_password, name='edit_user'),
    path('user_change_password/script', views.change_password_script, name='edit_user'),

    path('manage_employee', views_managment.manage_employee, name='manage_employee'),
    path('manage_manager', views_managment.manage_manager, name='manage_manager'),

    path('edit_manager/<int:manager_id>', views_managment.edit_manager, name='manage_manager'),
    path('edit_manager/script', views_managment.edit_manager_script, name='manage_manager'),
    path('create_manager', views_managment.create_manager, name='manage_manager'),
    path('create_manager/script', views_managment.create_manager_script, name='manage_manager'),
    path('delete_manager', views_managment.delete_manager, name='manage_manager'),

    path('edit_employee/<int:employee_id>', views_managment.edit_employee, name='manage_employee'),
    path('edit_employee/script', views_managment.edit_employee_script, name='manage_employee'),
    path('create_employee', views_managment.create_employee, name='manage_employee'),
    path('create_employee/script', views_managment.create_employee_script, name='manage_employee'),
    path('delete_employee', views_managment.delete_employee, name='manage_employee'),

    path('costumes/<int:costume_id>', views.costumes, name='costumes'),
    path('costumes/<int:costume_id>/edit', views.costumes_edit, name='costumes_edit'),
    path('costumes/<int:costume_id>/delete', views.costumes_delete, name='costumes_delete'),
    path('add_costume', views.add_costume.as_view(success_url='/gallery'), name='add_costume'),
    path('add_costume_template', views.add_costume_template.as_view(success_url='/costume_templates'), name='add_costume_template'),

    path('accessories/<int:accessory_id>', views.accessories, name='accessories'),
    path('accessories/<int:accessory_id>/edit', views.accessories_edit, name='accessories_edit'),
    path('accessories/<int:accessory_id>/delete', views.accessories_delete, name='accessories_delete'),
    path('add_accessory', views.add_accessory.as_view(success_url='/gallery'), name='add_accessory'),

    path('borrowings', views.borrowings_gallery, name='borrowings_gallery'),
    path('borrowings/<int:borrowing_id>', views.borrowings, name='borrowing'),
    path('borrowings/<int:borrowing_id>/edit', views.borrowings_edit, name='borrowing_edit'),
    path('borrowings/<int:borrowing_id>/delete', views.borrowings_delete, name='borrowing_delete'),

    path('costume_templates', views.costume_templates_gallery, name='costume_templates_gallery'),
    path('costume_templates/<int:ct_id>', views.costume_templates, name='costume_templates'),
    path('costume_templates/<int:costume_template_id>/edit', views.costume_templates_edit, name='costume_templates_edit'),
    path('costume_templates/<int:costume_template_id>/delete', views.costume_templates_delete, name='costume_templates_delete'),

    path('stores', views.stores_gallery, name='stores_gallery'),
    path('add_store', views.add_store.as_view(success_url='/gallery'), name='add_store'),
    path('stores/<int:store_id>', views.stores, name='stores'),
    path('stores/<int:store_id>/edit', views.stores_edit, name='stores_edit'),
    path('stores/<int:store_id>/delete', views.stores_delete, name='stores_delete'),

    path('add_costume_to_basket', views.add_costume_to_basket, name='add_costume_to_basket'),
    path('add_accessory_to_basket', views.add_accessory_to_basket, name='add_accessory_to_basket'),
    path('remove_costume_from_basket', views.remove_costume_from_basket, name='remove_costume_from_basket'),
    path('remove_accessory_from_basket', views.remove_accessory_from_basket, name='remove_accessory_from_basket'),
    path('finish_borrowing', views.finish_borrowing, name='finish_borrowing'),
    path('user_borrowings', views.user_borrowings, name='user_borrowings'),
    path('user_detail/<int:user_id>', views.user_detail, name='user_detail'),
    path('basket', views.basket, name='basket')
]
