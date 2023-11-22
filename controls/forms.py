from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
    """"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Usuario")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirme Contraseña")
# - Authetication User

class LoginForm(AuthenticationForm):
    """"""
    username = forms.CharField(widget=TextInput(attrs={'class': 'user-input'}), label="Usuario")
    password = forms.CharField(widget=PasswordInput(), label="Contraseña")

class Scores(forms.Form):
    CHOICES_TIME = [
        ("", "-- Seleccione --"),
        ('Muy rápido', 'Muy rápido'),
        ('Rápido', 'Rápido'),
        ('Normal', 'Normal'),
        ('Lento', 'Lento'),
        ('Muy Lento', 'Muy Lento'),
    ]

    CHOICES_ATT = [
        ('', '-- Selecciona --'),
        ('Excelente', 'Excelente'),
        ('Bueno', 'Bueno'),
        ('Normal', 'Normal'),
        ('Regular', 'Regular'),
        ('Malo', 'Malo'),
    ]

    CHOICES_SERVICE = [
        ('', '-- Selecciona --'),
        ('Si', 'Si'),
        ('No', 'No'),
    ]

    CHOICES_REC = [
        ('', '-- Selecciona --'),
        ('Si', 'Si'),
        ('Tal vez', 'Tal vez'),
        ('No', 'No'),
    ]

    time = forms.ChoiceField(choices=CHOICES_TIME, label="Tiempo espera?", widget=forms.Select(attrs={'class': 'scores-select'}))
    attention = forms.ChoiceField(choices=CHOICES_ATT, label="Servicio brindado?", widget=forms.Select(attrs={'class': 'scores-select'}))
    service = forms.ChoiceField(choices=CHOICES_SERVICE, label="Solicitud atendida?", widget=forms.Select(attrs={'class': 'scores-select'}))
    recomment = forms.ChoiceField(choices=CHOICES_REC, label="Recomendaria Coovitel?", widget=forms.Select(attrs={'class': 'scores-select'}))
    
    def __init__(self, *args, **kwargs):
        """"""
        super(Scores, self).__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'scores_date'})