from django.db import models

# Create your models here.
# Para poner clases

class Producto(models.Model):
    title = models.CharField(max_length=40)
    completado = models.BooleanField(default=False)