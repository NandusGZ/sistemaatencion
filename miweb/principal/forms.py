from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['id','numero_folio', 'depcon','calcon', 'sercon', 'fecha_solicitud', 'fecha_recibido','columna1', 'departamento_a_canalizar', 'solicitante', 'telefono', 'colonia_o_comunidad', 'domicilio', 'tipo_solicitud', 'fecha_atentida', 'avance', 'observaciones', 'oficios', 'columna3', 'columna4']
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control'}) for field in [
                'numero_folio', 'depcon', 'calcon', 'sercon', 'columna1',
                'solicitante', 'telefono', 'domicilio',
                'fecha_atentida', 'observaciones','oficios' , 'columna3', 'columna4'
            ]
        }
        widgets.update({
            'tipo_solicitud': forms.Select(attrs={'class': 'form-select'}),
            'colonia_o_comunidad': forms.Select(attrs={'class': 'form-select'}),
            'departamento_a_canalizar': forms.Select(attrs={'class': 'form-select'}),
            'colonia_o_comunidad': forms.Select(attrs={'class': 'form-select'}),
            'avance': forms.Select(attrs={'class': 'form-select'}),
            'fecha_solicitud': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_recibido': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_atentida': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),

            
        })

