from django import forms


class UserForm(forms.Form):
    name = forms.CharField(label="Nombre de usuario",
                           max_length=200,
                           widget=forms.TextInput(
                               attrs={'class': '', 'placeholder': 'Ingrese su nombre de usuario'})
                           )
    password = forms.CharField(label="Contraseña",
                               max_length=200,
                               widget=forms.TextInput(attrs={'class': '', 'placeholder': 'Ingrese su contraseña'})
                               )
