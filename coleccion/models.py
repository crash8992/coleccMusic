from django.db import models

class Artista(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Disco(models.Model):
    # Opciones para elegir en un menú desplegable
    FORMATOS = [
        ('V', 'Vinilo'),
        ('C', 'CD'),
        ('D', 'Digital'),
    ]

    titulo = models.CharField(max_length=150)
    # Relación: Un disco pertenece a un Artista
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    anio = models.IntegerField(verbose_name="Año de Lanzamiento")
    genero = models.CharField(max_length=50)
    
    # Aquí guardaremos la foto de la portada
    portada = models.ImageField(upload_to='portadas/', blank=True, null=True)
    
    formato = models.CharField(max_length=1, choices=FORMATOS, default='V')

    def __str__(self):
        return f"{self.titulo} - {self.artista.nombre}"
