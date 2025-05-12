from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django_ckeditor_5.fields import CKEditor5Field



class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            count = 1
            while Categoria.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{get_random_string(length=4)}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = CKEditor5Field("Contenido", config_name="default")  # ✅ CKEditor 5
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=False)
    categorias = models.ManyToManyField(Categoria)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen_destacada = models.ImageField(upload_to='posts/', blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)
            slug = base_slug
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{get_random_string(length=4)}"
            self.slug = slug
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo
