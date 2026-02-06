from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_discos, name='lista_discos'),
    path('crear/', views.crear_disco, name='crear_disco'),
]