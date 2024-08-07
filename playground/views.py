from django.shortcuts import render

# Create your views here.
# request -> response
# request handler
# Template es lo que ve, no views

from django.http import HttpResponse
from .models import Producto

def productos(request):
    # Conseguir un producto de nuestra base de datos (models.py)
    producto = Producto.objects.all()
    return render(request, 
        "productos.html", 
        {"productos": producto}
    )

def say_hi(request):
    #name = 'Caba'
    #x = calcular()

    return render(
        request, 
        'casa.html',
    )

def calcular():
    x = 1
    y = 2
    return x + y
