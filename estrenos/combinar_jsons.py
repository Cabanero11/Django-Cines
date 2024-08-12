import json
from fuzzywuzzy import fuzz, process
import re

# Cargar los datos de los dos JSON
with open('movies.json', 'r', encoding='utf-8') as file:
    abc_elx_movies = json.load(file)

with open('peliculas_torrevieja.json', 'r', encoding='utf-8') as file:
    torrevieja_movies = json.load(file)

# Función para normalizar los nombres de las películas
def normalize_title(title):
    return re.sub(r'\W+', '', title.lower().strip())

# Uso de 'fuzzywuzzy' para encontrar coincidencias aproximadas
def find_best_match(title, titles):
    normalized_title = normalize_title(title)
    choices = [(normalize_title(t), t) for t in titles]
    best_match = process.extractOne(normalized_title, [c[0] for c in choices])
    if best_match[1] >= 80:  # Threshold de coincidencia
        return dict(choices)[best_match[0]]
    return None

# Crear un diccionario para el JSON combinado
combined_movies = {}

# Función para agregar datos al JSON combinado
def add_movie(title, cinema_name, time, ticket_url, image_url):
    normalized_title = normalize_title(title)
    
    if normalized_title not in combined_movies:
        combined_movies[normalized_title] = {
            "title": title,  # Guarda el título original
            "image_url": image_url,
            "cinemas": []
        }
    
    # Buscar el cine en el JSON combinado
    cinemas = combined_movies[normalized_title]["cinemas"]
    cinema_found = False
    
    for cinema in cinemas:
        if cinema["cinema_name"] == cinema_name:
            cinema["times"].append({"time": time, "ticket_url": ticket_url})
            cinema_found = True
            break
    
    if not cinema_found:
        cinemas.append({
            "cinema_name": cinema_name,
            "times": [{"time": time, "ticket_url": ticket_url}]
        })

# Añadir datos del JSON de Cine ABC Elx
for title, data in abc_elx_movies.items():
    image_url = data["image_url"]
    for cinema in data["cinemas"]:
        cinema_name = cinema["cinema_name"]
        for time in cinema["times"]:
            add_movie(title, cinema_name, time["time"], time["ticket_url"], image_url)

# Añadir datos del JSON de Cine IMF Torrevieja
all_titles = list(abc_elx_movies.keys())  # Lista de todos los títulos en el JSON de Elx
for title, data in torrevieja_movies.items():
    image_url = data["image_url"]
    for cinema in data["cinemas"]:
        cinema_name = cinema["cinema_name"]
        for time in cinema["times"]:
            best_match_title = find_best_match(title, all_titles)
            if best_match_title:
                add_movie(best_match_title, cinema_name, time["time"], time["ticket_url"], image_url)
            else:
                add_movie(title, cinema_name, time["time"], time["ticket_url"], image_url)

# Opcional: Actualizar los títulos en el JSON combinado para una presentación más legible
for key, value in combined_movies.items():
    # Ejemplo de actualización simple: Capitalizar el título
    combined_movies[key]["title"] = combined_movies[key]["title"].title()

# Guardar el JSON combinado en un archivo
with open('combined_movies.json', 'w', encoding='utf-8') as file:
    json.dump(combined_movies, file, ensure_ascii=False, indent=4)

print("Datos combinados guardados en 'combined_movies.json'")