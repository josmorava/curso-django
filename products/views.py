from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView

from .forms import ProductForm
from .models import Product


# Create your views here.

class ProductFormView(generic.FormView):
    template_name = "products/add_products.html"
    form_class = ProductForm
    #reverse_lazy permite redirigir a una url
    success_url = reverse_lazy('products_list')
    
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class ProductListView(TemplateView):
    template_name = "products/products_list.html"
    def get_context_data(self):
        
        products = Product.objects.all()
        
        # car_list= [
        #     {"title": "BMW"},
        #     {"title": "Mazda"},
        # ]
        
        
        # products_list = [
        #     {"name": products.name},
        #     {"description": products.description},
        #     {"price": products.price},
            
        # ]
        
        return {
            # "products_list": products_list,
            "products": products,
        }
