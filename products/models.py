from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.TextField(
        max_length=100,
        # Como se verá el campo en el admin o para el usuario
        verbose_name="nombres",
    )
    description = models.TextField(max_length=300, verbose_name="descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="precio")
    available = models.BooleanField(default=True, verbose_name="disponible")
    photo = models.ImageField(upload_to="logo", null=True, blank=True, verbose_name="foto")
    
    def __str__(self):
        return self.name
