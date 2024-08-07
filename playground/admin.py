from django.contrib import admin


# Register your models here.
# La UI del admin aca
# Por cada nuevo modelo: python .\manage.py makemigrations
# Luego: python .\manage.py migrate
from .models import Producto

admin.site.register(Producto)

# Crear un usuario
# python .\manage.py createsuperuser
# admin
# admin