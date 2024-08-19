from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator

from .forms import ProductForm
from .models import Product


# Create your views here.

"""
    VISTAS BASADAS EN CLASES

class ProductFormView(generic.FormView):
    template_name = "products/add_products.html"
    form_class = ProductForm
    #reverse_lazy permite redirigir a una url
    success_url = reverse_lazy('list_product')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ProductListView(generic.ListView):
    paginate_by = 3 #3 productos por página
    
    model = Product
    template_name = "products/products_list.html"
    context_object_name = 'products'
"""



"""     VISTAS BASADAS EN FUNCIONES     """
def product_form_view(request):
    """Vista de formulario para agregar un producto"""
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect('list_product')
    else:
        product_form = ProductForm()
    data = {'product_form': product_form,}     
           
    return render (
        request,
        'products/add_products.html',
        data
    )
    
    
def product_list(request):
    """Vista de lista de productos"""
    
    products_list = Product.objects.all()
    p = Paginator(products_list, 3) #3 productos por paǵina
    page_number = request.GET.get("page")
    product = p.get_page(page_number)
    data = {
        # 'products': products_list,
        'product': product
            }
    
    return render(
        request,
        'products/products_list.html',
        data
    )
