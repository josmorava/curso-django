from django.contrib import admin
from .models import Order, OrderProduct

# Register your models here.


class OrderProductInline(admin.TabularInline):
    """Para que todos los productos se muestren en el admin"""
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    """Registro de modelo en el admin"""
    model = Order
    inlines = [
        OrderProductInline
    ]
    
admin.site.register(Order,OrderAdmin)