from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from blog import views
from blog.views import lista_categoria  # ✅ Importa la función correcta


urlpatterns = [
    path('', include('principal.urls')),
    path('admin/', admin.site.urls),
    path('admin-panel/', include('panel_admin.urls')), # Incluye las URLs de la aplicación panel admin
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'), # Asegurar que login/logout se capturen antes que el blog
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('blog.urls')), # Incluye las URLs de la aplicación blog
    path('categorias/', lista_categoria, name='lista_categoria'),  # ✅ Llamamos la vista correcta
    path('ckeditor5/', include('django_ckeditor_5.urls')), #CKEditor 5 

  
    ]

if settings.DEBUG:  # Solo en modo desarrollo
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Agrega esta línea