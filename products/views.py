from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
import json

from .forms import ProductForm
from .models import Product
# from .serializers import ProductListSchema
from django.core import serializers


# Create your views here.

class ProductFormView(generic.FormView):
    template_name = "products/add_products.html"
    form_class = ProductForm
    #reverse_lazy permite redirigir a una url
    success_url = reverse_lazy('products_list')
    
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

# class ProductListView(TemplateView):
#     template_name = "products/products_list.html"
#     def get_context_data(self):
#         products = Product.objects.all()
        
#         products_list = serializers.serialize("json", Product.objects.all(), fields=['name', 'description','price'])
#         products_dict = json.loads(products_list)
        
#         print(type(products_list))
#         products_name = products_dict['pk']
        
#         data = products_dict
            
#         return {
#             "products_list": products_list,
#             "products": data,
#             "products_name": products_name
#             # "products_list": products_list,
#         }

def ProductList(request):
    products = Product.objects.all()
    data = {
        'productos': products
    }
    return render(
        request,
        'products/products_list.html',
        data
    )