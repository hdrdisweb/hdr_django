from django.urls import path
from . import views
from panel_admin import views
from blog.views import detalle_entrada  # ✅ Importar correctamente
from blog.views import lista_categoria
from .views import lista_categorias, crear_categoria, editar_categoria, eliminar_categoria

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    
    # CRUD de Posts
    path('posts/', views.lista_posts, name='lista_posts'),
    path('posts/crear/', views.crear_post, name='crear_post'),
    path('posts/editar/<int:post_id>/', views.editar_post, name='editar_post'),
    path('posts/eliminar/<int:post_id>/', views.eliminar_post, name='eliminar_post'),
    # path('<slug:slug>/', detalle_entrada, name='detalle_entrada'),  # ✅ Ahora viene de blog.views
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),  
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'), 
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('categorias/', lista_categorias, name='lista_categorias'),
    path('categorias/crear/', crear_categoria, name='crear_categoria'),
    path('categorias/editar/<slug:slug>/', editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<slug:slug>/', eliminar_categoria, name='eliminar_categoria'),
    path('medios/', views.lista_medios, name='lista_medios'),
    path('medios/subir/', views.subir_medio, name='subir_medio'),
    path('medios/eliminar/<str:nombre_archivo>/', views.eliminar_medio_archivo, name='eliminar_medio_archivo'),

    
]