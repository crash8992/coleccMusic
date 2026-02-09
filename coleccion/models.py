from django.db import models

class Artista(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre

class Disco(models.Model):
    # ... tus campos actuales ...
    titulo = models.CharField(max_length=200)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    anio = models.IntegerField()
    genero = models.CharField(max_length=100)
    
    OPCIONES_FORMATO = [
        ('V', 'Vinilo'),
        ('C', 'CD'),
        ('D', 'Digital'),
        ('CT', 'Cassette'),
    ]
    formato = models.CharField(max_length=2, choices=OPCIONES_FORMATO)
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)

    # --- CAMPO NUEVO ---
    spotify_url = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="Link de Spotify (Opcional)",
        help_text="Copia el link del álbum desde Spotify (ej: https://open.spotify.com/album/...)"
    )

    def __str__(self):
        return f"{self.titulo} - {self.artista}"

    # --- FUNCIÓN MÁGICA PARA EL ID ---
    @property
    def spotify_id(self):
        """
        Extrae el ID del álbum de la URL completa.
        Ejemplo: De '.../album/4m2880jivSbbyEG...' saca '4m2880jivSbbyEG...'
        """
        if self.spotify_url:
            try:
                # Divide por '/' y toma el último pedazo, quitando interrogantes si los hay
                return self.spotify_url.split('/')[-1].split('?')[0]
            except:
                return None
        return None