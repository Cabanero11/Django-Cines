# Codigo para copiar y pegar en el shell, para tener datos

from estrenos.models import Cine, Pelicula
from datetime import datetime

# Crear cines de ejemplo
cine1 = Cine.objects.create(nombre='Cine ABC Elx')
cine2 = Cine.objects.create(nombre='Cine IMF Torrevieja')
cine3 = Cine.objects.create(nombre='Cine Axion Orihuela')

# Crear estrenos de ejemplo
Pelicula.objects.create(
    cine=cine1,
    titulo='Deadpool 3',
    fecha=datetime.now().date(),
    foto_url='https://www.cinesabc.com/files/deadpool_bueno2_nfxv9ztf.jpg',
    horarios='14:00, 16:00, 20:00'
)

Pelicula.objects.create(
    cine=cine2,
    titulo='Deadpool 2',
    fecha=datetime.now().date(),
    foto_url='https://www.cinesabc.com/files/deadpool_bueno2_nfxv9ztf.jpg',
    horarios='14:30, 16:30, 21:00'
)

Pelicula.objects.create(
    cine=cine3,
    titulo='Deadpool 1',
    fecha=datetime.now().date(),
    foto_url='https://www.cinesabc.com/files/deadpool_bueno2_nfxv9ztf.jpg',
    horarios='13:30, 15:30, 18:00, 22:00'
)

Pelicula.objects.create(
    cine=cine1,
    titulo='Avengers: Endgame',
    fecha=datetime.now().date(),
    foto_url='https://www.cinesabc.com/files/deadpool_bueno2_nfxv9ztf.jpg',
    horarios='12:00, 15:00, 18:00'
)

Pelicula.objects.create(
    cine=cine2,
    titulo='Avengers: Cum',
    fecha=datetime.now().date(),
    foto_url='https://www.cinesabc.com/files/deadpool_bueno2_nfxv9ztf.jpg',
    horarios='11:30, 14:30, 17:30'
)

Pelicula.objects.create(
    cine=cine3,
    titulo='Avengers: Ahora es serio',
    fecha=datetime.now().date(),
    foto_url='https://www.cinesabc.com/files/deadpool_bueno2_nfxv9ztf.jpg',
    horarios='13:00, 16:00, 19:00'
)

Pelicula.objects.create(
    cine=cine1,
    titulo='Joker',
    fecha=datetime.now().date(),
    foto_url='https://www.cinesabc.com/files/deadpool_bueno2_nfxv9ztf.jpg',
    horarios='10:00, 13:00, 16:00'
)

Pelicula.objects.create(
    cine=cine2,
    titulo='Joker 2',
    fecha=datetime.now().date(),
    foto_url='https://www.cinesabc.com/files/deadpool_bueno2_nfxv9ztf.jpg',
    horarios='12:00, 15:00, 18:00'
)

Pelicula.objects.create(
    cine=cine3,
    titulo='Batman',
    fecha=datetime.now().date(),
    foto_url='https://www.cinesabc.com/files/deadpool_bueno2_nfxv9ztf.jpg',
    horarios='14:00, 17:00, 20:00'
)

Pelicula.objects.create(
    cine=cine1,
    titulo='Inception',
    fecha=datetime.now().date(),
    foto_url='https://www.cinesabc.com/files/deadpool_bueno2_nfxv9ztf.jpg',
    horarios='11:00, 14:00, 17:00'
)