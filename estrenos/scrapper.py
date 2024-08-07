import requests
from bs4 import BeautifulSoup
import json

def scrapeacion():
    url = 'URL_DEL_CINE'  # Reemplaza con la URL real del cine
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    movies = []

    # Suponiendo que la estructura HTML de la página contiene elementos div con la clase 'movie' para cada película
    for movie_div in soup.find_all('div', class_='movie'):
        title = movie_div.find('h2', class_='title').text
        image_url = movie_div.find('img', class_='poster')['src']
        schedules = {}

        # Suponiendo que los horarios están dentro de divs con la clase 'schedules'
        for schedule_div in movie_div.find_all('div', class_='schedule'):
            cinema_name = schedule_div.find('h3', class_='cinema').text
            times = [time.text for time in schedule_div.find_all('span', class_='time')]
            schedules[cinema_name] = times

        movies.append({
            'title': title,
            'image_url': image_url,
            'schedules': schedules,
        })

    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    scrapeacion()