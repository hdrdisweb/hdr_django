from django.contrib import admin
# from blog.models import Post, Categoria 
from panel_admin.models import Categoria


 # @admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion', 'publicado')
    list_filter = ('publicado', 'categorias', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}

# @admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    prepopulated_fields = {'slug': ('nombre',)}

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')  # 👈 Agregamos 'descripcion'

admin.site.register(Categoria, CategoriaAdmin)