from django.shortcuts import render
from .models import Disco
# 1. Importar el candado
from django.contrib.auth.decorators import login_required

# 2. Decorar la vista
@login_required
def listar_discos(request):
    discos = Disco.objects.all()
    return render(request, 'coleccion/lista.html', {'discos': discos})