from django import forms
from .models import Disco, Artista

class DiscoForm(forms.ModelForm):
    # Campo extra para escribir un artista nuevo
    nuevo_artista = forms.CharField(
        label="¿Artista nuevo?",
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Escribe el nombre aquí si no está en la lista'
        })
    )

    class Meta:
        model = Disco
        fields = ['titulo', 'artista', 'nuevo_artista', 'anio', 'genero', 'formato', 'portada']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'artista': forms.Select(attrs={'class': 'form-select'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'genero': forms.TextInput(attrs={
            'class': 'form-control', 
            'list': 'listado-generos',  # <--- ESTO ES LA MAGIA: Vincula con el ID del HTML
            'autocomplete': 'off' }),      # Apaga el autocompletado feo del navegador
            'formato': forms.Select(attrs={'class': 'form-select'}),
            'portada': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos el campo de la lista opcional para que no bloquee el formulario
        # si queremos escribir uno nuevo.
        self.fields['artista'].required = False
        self.fields['artista'].label = "Seleccionar Artista existente"

    # --- ESTA ES LA PARTE CLAVE QUE EVITA EL ERROR ---
    def clean(self):
        cleaned_data = super().clean()
        artista_seleccionado = cleaned_data.get('artista')
        nuevo_artista_escrito = cleaned_data.get('nuevo_artista')

        # Si los dos están vacíos -> ERROR
        if not artista_seleccionado and not nuevo_artista_escrito:
            raise forms.ValidationError("¡Cuidado! Debes seleccionar un artista de la lista O escribir uno nuevo.")
        
        return cleaned_data