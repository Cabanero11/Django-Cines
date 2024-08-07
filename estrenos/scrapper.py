import requests
from bs4 import BeautifulSoup


# TODO: No funciona xd
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
estrenos_totales = {
    'Cine ABC Elx': estrenos_cine1,
    'Cine IMF Torrevieja': estrenos_cine2,
    'Cine Axion Orihuela': estrenos_cine3,
}