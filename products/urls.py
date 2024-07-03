
from django.urls import path
from .views import ProductFormView, ProductList

urlpatterns = [
    path('agregar/', ProductFormView.as_view(), name="add_product"),
    path('lista/', ProductList, name="products_list"), 
]
