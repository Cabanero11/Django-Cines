from django.db import models

# Create your models here.

# Para guardar los Cines diferentes
class Cine(models.Model):
    nombre = models.CharField(max_length=100)

# Para las peliculas
class Pelicula(models.Model):
    cine = models.ForeignKey(Cine, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    # Fecha de Hoy solo
    fecha = models.DateField() 
    foto_url = models.URLField()
    horarios = models.CharField(max_length=200)
    