from django import forms
from .models import Viatic

class UserForm(forms.Form):
    username = forms.CharField(max_length=200,
                               widget=forms.TextInput(
                                   attrs={'id': 'username-input', 'placeholder': 'Ingrese su nombre de usuario'})
                               )
    password = forms.CharField(label='Contraseña',
                               max_length=200,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Ingrese su contraseña'})
<<<<<<< HEAD
                               )

#class to upload file with pandas in a database before
class UploadFileForm(forms.Form):
    archivo = forms.FileField()

=======
                               )
>>>>>>> 6c8d271d600ab75c6e70c4f529c9fa69aa3ce15c
