from django import forms

class BuscarForm(forms.Form):
    palabra_clave = forms.CharField(
        label="Palabra clave",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    enviar_email = forms.BooleanField(
        label="Enviar resultados por email",
        required=False
    )
