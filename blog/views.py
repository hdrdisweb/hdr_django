from django.shortcuts import render, get_object_or_404
from .models import Post, Categoria
from django.core.paginator import Paginator
from blog.models import Categoria  # Importar el modelo correcto


def lista_entradas(request):
    entradas_list = Post.objects.filter(publicado=True).order_by('-fecha_publicacion')
    paginator = Paginator(entradas_list, 2)  # 2 noticias por página

    page_number = request.GET.get('page')
    entradas = paginator.get_page(page_number)

    categorias = Categoria.objects.all()  # Para mostrar las categorías

    context = {
        'entradas': entradas,
        'categorias': categorias,
        'is_paginated': entradas.has_other_pages(),  # Indica si hay más de una página
    }

    return render(request, 'blog/lista_entradas.html', context)


def detalle_entrada(request, slug):
    entrada = get_object_or_404(Post, slug=slug, publicado=True)
    categorias = Categoria.objects.all()  # Obtener todas las categorías para el sidebar
    return render(request, 'blog/detalle_entrada.html', {'entrada': entrada, 'categorias': categorias})

def lista_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    entradas = Post.objects.filter(categorias=categoria, publicado=True)  # ✅ Filtrar por la categoría seleccionada
    categorias = Categoria.objects.all()  # ✅ Obtener todas las categorías para el sidebar

    return render(request, 'blog/lista_categoria.html', {
        'categoria': categoria,
        'entradas': entradas,
        'categorias': categorias,  # ✅ Pasar todas las categorías al contexto
    })

def buscar_entradas(request):
    query = request.GET.get('q')
    if query:
        resultados = Post.objects.filter(titulo__icontains=query, publicado=True)
    else:
        resultados = Post.objects.none()
    categorias = Categoria.objects.all()  # Para mostrar todas las categorías en el sidebar
    return render(request, 'blog/buscar_entradas.html', {'resultados': resultados, 'query': query, 'categorias': categorias})
