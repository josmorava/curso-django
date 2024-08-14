from django.shortcuts import render
from django.views.generic import DetailView

from .models import Order

# Create your views here.
class MyOrderView(DetailView):
    model = Order 
    template_name = "orders/my_order.html"
    
    def get_object(self, queryset=None):
        """Obtener solo una orden que esté activa"""
        return Order.objects.filter(is_active = True)