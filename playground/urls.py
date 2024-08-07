from django.urls import path
from . import views

# Para asociar urls a las views

# URLConf configuracion del modulo, falta importalo
# En la otra carpeta urls.py
urlpatterns = [
    path('inicio/', views.say_hi),
    path('productos/', views.productos)
]
