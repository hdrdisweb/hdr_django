from django import forms
from blog.models import Post
from django_ckeditor_5.fields import CKEditor5Field
from panel_admin.models import Medio  # Importamos el modelo Medio
from django.contrib.auth.models import User # Importamos el usuario
from blog.models import Post, Categoria # Importamos el categoria
from django.contrib.auth.forms import UserCreationForm
from blog.models import Categoria


class PostForm(forms.ModelForm):
    contenido = CKEditor5Field("Contenido", config_name="default")

    class Meta:
        model = Post
        fields = ['titulo', 'slug', 'contenido', 'categorias', 'imagen_destacada', 'publicado']
        widgets = { 
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'style': 'font-size: 13px;', 'placeholder': 'Título del post'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'style': 'font-size: 13px;', 'placeholder': 'Slug'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'style': 'font-size: 13px;', 'placeholder': 'Contenido del post'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-select form-select-sm', 'style': 'font-size: 10px;'}),
            'imagen_destacada': forms.FileInput(attrs={'class': 'form-control', 'style': 'font-size: 10px; width: 335px;'}),
            'publicado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'slug']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'font-size: 14px;',
                'placeholder': 'Nombre de la categoría'}),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'font-size: 14px;',
                'placeholder': 'Slug'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Categoria.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Este slug ya existe. Prueba con otro.")
        return slug
    

class MedioForm(forms.ModelForm):
    class Meta:
        model = Medio
        fields = ['nombre', 'tipo', 'archivo']

class UsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser']