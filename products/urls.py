
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name="list_product"), 
    path('agregar/', views.product_form_view, name="add_product"),
] 
