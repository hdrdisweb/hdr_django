from django.urls import path
from . import views
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('contacto/', views.contact, name='contact'),
    path('contacto/exito/', views.contact_success, name='contact_success'),
]