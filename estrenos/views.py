from django.shortcuts import render

# Create your views here.
from .models import Cine, Pelicula
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from collections import defaultdict

# Función para obtener los estrenos de los cines
def obtener_estrenos_totales():
    def obtener_estrenos_cine(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        estrenos = []
        for item in soup.select('.movie-list-item'):
            titulo = item.select_one('.movie-title').get_text()
            fecha = item.select_one('.release-date').get_text()
            foto_url = item.select_one('.movie-poster')['src']
            horarios = item.select_one('.showtimes').get_text(separator=', ')
            estrenos.append({'titulo': titulo, 'fecha': fecha, 'foto_url': foto_url, 'horarios': horarios})
        
        return estrenos

    # URLs de ejemplo
    url_cine1 = 'https://www.cinesabc.com'
    url_cine2 = 'https://example.com/cine2'
    url_cine3 = 'https://example.com/cine3'

    estrenos_cine1 = obtener_estrenos_cine(url_cine1)
    estrenos_cine2 = obtener_estrenos_cine(url_cine2)
    estrenos_cine3 = obtener_estrenos_cine(url_cine3)

    # Combinando los datos
    return {
        'Cine ABC Elx': estrenos_cine1,
        'Cine IMF Torrevieja': estrenos_cine2,
        'Cine Axion Orihuela': estrenos_cine3,
    }

# Función para guardar los estrenos en la base de datos
def guardar_estrenos():
    cine1 = Cine.objects.get_or_create(nombre='Cine 1')[0]
    cine2 = Cine.objects.get_or_create(nombre='Cine 2')[0]
    cine3 = Cine.objects.get_or_create(nombre='Cine 3')[0]

    estrenos_totales = obtener_estrenos_totales()

    for cine_nombre, estrenos in estrenos_totales.items():
        cine = Cine.objects.get(nombre=cine_nombre)
        for estreno in estrenos:
            fecha = datetime.strptime(estreno['fecha'], '%Y-%m-%d').date()
            Pelicula.objects.create(
                cine=cine,
                titulo=estreno['titulo'],
                fecha=fecha,
                foto_url=estreno['foto_url'],
                horarios=estreno['horarios']
            )

# Mostrar los estrenos de hoy
def mostrar_estrenos_hoy(request):
    hoy = datetime.now().date()
    peliculas = Pelicula.objects.filter(fecha=hoy).select_related('cine')
    
    # Agrupar estrenos por título de película
    estrenos_agrupados = defaultdict(lambda: {'foto_url': '', 'cines': defaultdict(list)})
    for pelicula in peliculas:
        estrenos_agrupados[pelicula.titulo]['foto_url'] = pelicula.foto_url
        estrenos_agrupados[pelicula.titulo]['cines'][pelicula.cine.nombre].append(pelicula.horarios)
    
    # Convertir defaultdict a dict normal para pasar a la plantilla
    context = {
        'estrenos': dict(estrenos_agrupados),
    }
    
    return render(request, 'estrenos.html', context)

def actualizar_estrenos(request):
    guardar_estrenos()
    return HttpResponse("Estrenos actualizados con éxito.")