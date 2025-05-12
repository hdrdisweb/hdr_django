from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.lista_entradas, name='lista_entradas'),
    path('categorias/<slug:slug>/', views.lista_categoria, name='lista_categoria'), 
    path('buscar/', views.buscar_entradas, name='buscar_entradas'),
    path('noticia/<slug:slug>/', views.detalle_entrada, name='detalle_entrada'),
]
