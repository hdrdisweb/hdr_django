from django.shortcuts import render, get_object_or_404
from .models import Post, Categoria
from django.core.paginator import Paginator

def lista_entradas(request):
    entradas = Post.objects.filter(publicado=True).order_by('-fecha_publicacion')
    return render(request, 'blog/lista_entradas.html', {'entradas': entradas})

def detalle_entrada(request, slug):
    entrada = get_object_or_404(Post, slug=slug, publicado=True)
    return render(request, 'blog/detalle_entrada.html', {'entrada': entrada})

def lista_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    entradas = Post.objects.filter(categorias=categoria, publicado=True).order_by('-fecha_publicacion')
    return render(request, 'blog/lista_entradas.html', {'entradas': entradas, 'categoria': categoria})

def buscar_entradas(request):
    query = request.GET.get('q')
    if query:
        resultados = Post.objects.filter(titulo__icontains=query, publicado=True)
    else:
        resultados = Post.objects.none()
    return render(request, 'blog/buscar_entradas.html', {'resultados': resultados, 'query': query})
