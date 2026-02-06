from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Disco, Artista
from .forms import DiscoForm

# --- VISTA 1: LISTAR LOS DISCOS ---
@login_required
def listar_discos(request):
    discos = Disco.objects.all()
    return render(request, 'coleccion/lista.html', {'discos': discos})

# --- VISTA 2: CREAR UN NUEVO DISCO (Con autocompletado de Géneros) ---
@login_required
def crear_disco(request):
    # 1. Obtener lista de géneros únicos para el autocompletado
    # Esto busca todos los géneros que ya existen para sugerírtelos
    lista_generos = Disco.objects.values_list('genero', flat=True).distinct().order_by('genero')

    if request.method == 'POST':
        form = DiscoForm(request.POST, request.FILES)
        if form.is_valid():
            # 2. Preparamos el disco
            disco = form.save(commit=False)
            
            # 3. Lógica del Artista (Nuevo vs Existente)
            artista_existente = form.cleaned_data.get('artista')
            # .strip() quita espacios extra
            nuevo_artista_nombre = form.cleaned_data.get('nuevo_artista', '').strip()

            if nuevo_artista_nombre:
                # Crear artista nuevo si no existe
                artista_obj, created = Artista.objects.get_or_create(nombre=nuevo_artista_nombre)
                disco.artista = artista_obj
            elif artista_existente:
                # Usar el seleccionado
                disco.artista = artista_existente
            else:
                # Si algo falla, recargamos el form enviando la lista de géneros de nuevo
                return render(request, 'coleccion/form_disco.html', {
                    'form': form, 
                    'generos': lista_generos
                })
            
            # 4. Guardar
            disco.save()
            return redirect('lista_discos')
    else:
        form = DiscoForm()

    # Enviamos tanto el formulario como la lista de géneros al HTML
    return render(request, 'coleccion/form_disco.html', {
        'form': form, 
        'generos': lista_generos
    })