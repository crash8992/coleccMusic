from django.shortcuts import render, redirect
from .models import Disco
from .forms import DiscoForm
from django.contrib.auth.decorators import login_required
from .models import Disco, Artista  # <--- IMPORTANTE: Importar Artista

@login_required
def crear_disco(request):
    if request.method == 'POST':
        form = DiscoForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Obtenemos el objeto disco pero NO lo guardamos aún en la BD
            disco = form.save(commit=False)
            
            # 2. Capturamos los datos
            artista_existente = form.cleaned_data.get('artista')
            nuevo_artista_nombre = form.cleaned_data.get('nuevo_artista')

            # 3. Lógica de decisión
            if nuevo_artista_nombre:
                # Creamos el artista (get_or_create evita duplicados si ya existía el nombre)
                artista, created = Artista.objects.get_or_create(nombre=nuevo_artista_nombre)
                disco.artista = artista
            else:
                # Usamos el de la lista
                disco.artista = artista_existente
            
            # 4. Ahora sí guardamos el disco
            disco.save()
            return redirect('lista_discos')
    else:
        form = DiscoForm()

    return render(request, 'coleccion/form_disco.html', {'form': form})
# --- VISTA 1: LISTAR LOS DISCOS ---
@login_required
def listar_discos(request):
    discos = Disco.objects.all()
    return render(request, 'coleccion/lista.html', {'discos': discos})

# --- VISTA 2: CREAR UN NUEVO DISCO ---
@login_required
def crear_disco(request):
    if request.method == 'POST':
        # Cargamos los datos y la imagen (FILES)
        form = DiscoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_discos') # Vuelve al inicio al terminar
    else:
        form = DiscoForm() # Formulario vacío

    return render(request, 'coleccion/form_disco.html', {'form': form})