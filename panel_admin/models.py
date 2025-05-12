from django.db import models  
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from blog.models import Post, Categoria


class Medio(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='medios/')
    tipo = models.CharField(max_length=50, choices=[('imagen', 'Imagen'), ('video', 'Video'), ('documento', 'Documento')])
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre