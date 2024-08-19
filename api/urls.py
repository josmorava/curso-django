
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.product_add_view, name="add_product"),
    path('list/', views.product_list_view, name="list_product"),
    path('detail/<int:product_id>/', views.product_detail_view, name="detail_product"),
    path('detail/<int:product_id>/edit/', views.product_edit_view, name="edit_product"),
    path('detail/<int:product_id>/delete/', views.product_delete_view, name="delete_product"),
    
    path('login/', views.login_view, name="login_api"),
    path('logout/', views.logout_view, name="logout_api"),
    path('register/', views.create_user_view, name="register_user_api")

    
] 
