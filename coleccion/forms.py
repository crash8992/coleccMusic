from django import forms
from .models import Disco, Artista  # <--- ASEGÚRATE DE IMPORTAR ARTISTA

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
            'genero': forms.TextInput(attrs={'class': 'form-control'}),
            'formato': forms.Select(attrs={'class': 'form-select'}),
            'portada': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que el desplegable sea opcional para que no falle si escribimos uno nuevo
        self.fields['artista'].required = False
        self.fields['artista'].label = "Seleccionar Artista existente"

    # Validación personalizada: Al menos uno de los dos debe tener datos
    def clean(self):
        cleaned_data = super().clean()
        artista = cleaned_data.get('artista')
        nuevo_artista = cleaned_data.get('nuevo_artista')

        if not artista and not nuevo_artista:
            raise forms.ValidationError("Debes seleccionar un artista de la lista O escribir uno nuevo.")
        
        return cleaned_data