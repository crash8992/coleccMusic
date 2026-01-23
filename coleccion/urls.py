from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_discos, name='lista_discos'),
]