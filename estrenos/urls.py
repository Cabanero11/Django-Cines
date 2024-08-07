from django.urls import path
from . import views

# Para asociar urls a las views

# URLConf configuracion del modulo, falta importalo
# En la otra carpeta urls.py
urlpatterns = [
    # En el base
    path('', views.mostrar_estrenos_hoy),
    # URL para actualizar estrenos
    path('actualizar_estrenos/', views.actualizar_estrenos),  
]
