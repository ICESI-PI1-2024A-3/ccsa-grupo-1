from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=200,
                               widget=forms.TextInput(
                                   attrs={'id': 'username-input', 'placeholder': 'Ingrese su nombre de usuario'})
                               )
    password = forms.CharField(label='Contraseña',
                               max_length=200,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Ingrese su contraseña'})
                               )

#class to upload file with pandas in a database before
class UploadFileForm(forms.Form):
    archivo = forms.FileField()
