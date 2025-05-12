import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Post, Categoria  # Modelos de blog
from blog.views import detalle_entrada  # ✅ Importar desde blog
from django.contrib.auth.models import User  # Modelo de usuarios
from .forms import PostForm  # Formulario para crear/editar posts
from panel_admin.models import Medio  # Para medios
from .models import Medio
from .forms import MedioForm
from panel_admin.forms import UsuarioForm  
from django.contrib import messages  # ✅ Importar messages
from blog.models import Categoria
from django.utils.text import slugify
from panel_admin.forms import CategoriaForm



@login_required
def dashboard(request):
    ultimas_noticias = Post.objects.filter(publicado=True).order_by('-fecha_publicacion')[:5]  # Últimas 5 noticias
    ultimos_usuarios = User.objects.order_by('-date_joined')[:5]  # Últimos 5 usuarios registrados

    return render(request, 'panel_admin/dashboard.html', {
        'ultimas_noticias': ultimas_noticias,
        'ultimos_usuarios': ultimos_usuarios
    })

# ---- CRUD DE POSTS ----
@login_required
def lista_posts(request):
    posts = Post.objects.all().order_by('-fecha_publicacion')
    return render(request, 'panel_admin/lista_posts.html', {'posts': posts})

@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            form.save_m2m()
            return redirect('lista_posts')
    else:
        form = PostForm()
    return render(request, 'panel_admin/crear_post.html', {'form': form})

@login_required
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('lista_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'panel_admin/editar_post.html', {'form': form, 'post': post})

@login_required
def eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('lista_posts')
    return render(request, 'panel_admin/eliminar_post.html', {'post': post})

@login_required
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'panel_admin/lista_usuarios.html', {'usuarios': usuarios})

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'panel_admin/lista_categorias.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'panel_admin/crear_categorias.html', {'form': form})

@login_required
def lista_medios(request):
    medios = Medio.objects.all()  # Si tienes un modelo llamado 'Medio'
    return render(request, 'panel_admin/lista_medios.html', {'medios': medios})

@login_required
def lista_medios(request):
    medios = Medio.objects.all().order_by('-fecha_subida')
    return render(request, 'panel_admin/lista_medios.html', {'medios': medios})

@login_required
def subir_medio(request):
    if request.method == 'POST':
        form = MedioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_medios')
    else:
        form = MedioForm()
    return render(request, 'panel_admin/subir_medio.html', {'form': form})

@login_required
def eliminar_medio(request, medio_id):
    medio = Medio.objects.get(id=medio_id)
    if request.method == 'POST':
        medio.delete()
        return redirect('lista_medios')
    return render(request, 'panel_admin/eliminar_medio.html', {'medio': medio})




# gestion de usuarios
@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)

            # Obtener el valor del rol seleccionado
            rol = request.POST.get('rol')

            if rol == "superuser":
                usuario.is_superuser = True
                usuario.is_staff = True  # Los superusuarios también son staff
            elif rol == "admin":
                usuario.is_staff = True
                usuario.is_superuser = False  # Asegurar que no es superusuario
            else:
                usuario.is_staff = False  # Editor
                usuario.is_superuser = False  # No es superusuario

            usuario.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    
    return render(request, 'panel_admin/crear_usuario.html', {'form': form})



@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'panel_admin/editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)

    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')

    return render(request, 'panel_admin/eliminar_usuario.html', {'usuario': usuario})

# MEDIOS 
def lista_medios(request):
    # Obtener los archivos que ya están en la base de datos
    medios_db = Medio.objects.all()

    # Buscar solo en 'media/posts/'
    media_path = os.path.join(settings.MEDIA_ROOT, 'posts')
    archivos_en_carpeta = []

    if os.path.exists(media_path):  # Verificamos que la carpeta exista
        for archivo in os.listdir(media_path):
            archivos_en_carpeta.append({
                'nombre': archivo,
                'url': f"{settings.MEDIA_URL}posts/{archivo}",
                'tipo': 'imagen' if archivo.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp')) else 'otro'
            })

    return render(request, 'panel_admin/lista_medios.html', {
        'medios_db': medios_db,
        'archivos_en_carpeta': archivos_en_carpeta,
    })

def eliminar_medio_archivo(request, nombre_archivo):
    """Elimina un archivo de la carpeta media/posts/"""
    archivo_path = os.path.join(settings.MEDIA_ROOT, 'posts', nombre_archivo)

    if os.path.exists(archivo_path):  
        os.remove(archivo_path)
        messages.success(request, f"El archivo {nombre_archivo} ha sido eliminado correctamente.")
    else:
        messages.error(request, "El archivo no existe o ya ha sido eliminado.")

    return redirect('lista_medios')

# ---- CRUD DE Categorias ----
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'panel_admin/lista_categorias.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        slug = slugify(nombre)  # Generar slug automáticamente
        #descripcion = request.POST.get('descripcion', '')
        Categoria.objects.create(nombre=nombre, slug=slug)
        return redirect('lista_categorias')

    return render(request, 'panel_admin/crear_categorias.html', {'titulo': 'Crear Categoría'})

def editar_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)

    if request.method == "POST":
        categoria.nombre = request.POST['nombre']
        categoria.slug = request.POST['slug']  # 👈 Permitir actualizar el slug
        categoria.descripcion = request.POST.get('descripcion', '')

        categoria.save()
        return redirect('lista_categorias')  # Redirigir después de guardar

    return render(request, 'panel_admin/editar_categorias.html', {'categoria': categoria})

def eliminar_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)

    if request.method == "POST":
        categoria.delete()
        return redirect('lista_categorias')

    return render(request, 'panel_admin/eliminar_categoria.html', {'titulo': 'Eliminar Categoría', 'categoria': categoria})