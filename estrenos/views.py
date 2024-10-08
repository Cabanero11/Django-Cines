from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json, os

def mostrar_estrenos(request):
    # Definir la ruta del archivo JSON en el mismo directorio que manage.py
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'combined_movies.json')

    # Leer el archivo JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            movies = json.load(file)
    except FileNotFoundError:
        return HttpResponse("Archivo combines_movies.json no encontrado", status=404)
    except json.JSONDecodeError:
        return HttpResponse("Error al decodificar el archivo JSON", status=500)
    
    # Obtener el término de búsqueda, si existe
    query = request.GET.get('search', '').lower()

    # Filtrar las películas según el término de búsqueda
    filtered_movies = {}
    for title, data in movies.items():
        if query in title.lower():
            filtered_movies[title] = data

    # Pasar los datos al template
    return render(request, 'estrenos.html', {'estrenos': filtered_movies})
        