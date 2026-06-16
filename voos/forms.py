from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Voo, Passageiro, Reserva


class VooForm(forms.ModelForm):
    """
    Formulário para criar/editar um Voo (admin).
    """
    class Meta:
        model  = Voo
        fields = ['numero', 'companhia', 'origem', 'destino',
                  'data_partida', 'data_chegada', 'lugares_disponiveis', 'preco']
        widgets = {
            'numero':              forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ex: TP123'}),
            'companhia':           forms.Select(attrs={'class': 'select'}),
            'origem':              forms.Select(attrs={'class': 'select'}),
            'destino':             forms.Select(attrs={'class': 'select'}),
            'data_partida':        forms.DateTimeInput(attrs={'class': 'input', 'type': 'datetime-local'}),
            'data_chegada':        forms.DateTimeInput(attrs={'class': 'input', 'type': 'datetime-local'}),
            'lugares_disponiveis': forms.NumberInput(attrs={'class': 'input', 'min': '1'}),
            'preco':               forms.NumberInput(attrs={'class': 'input', 'step': '0.01', 'min': '0'}),
        }


class PassageiroForm(forms.ModelForm):
    """
    Formulário para criar/editar um Passageiro.
    """
    class Meta:
        model  = Passageiro
        fields = ['nome', 'email', 'telefone', 'documento']
        widgets = {
            'nome':      forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nome completo'}),
            'email':     forms.EmailInput(attrs={'class': 'input', 'placeholder': 'email@example.com'}),
            'telefone':  forms.TextInput(attrs={'class': 'input', 'placeholder': '+351 XXX XXX XXX'}),
            'documento': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Número do passaporte'}),
        }


class ReservaForm(forms.ModelForm):
    """
    Formulário para criar/editar uma Reserva manualmente (admin).
    """
    class Meta:
        model  = Reserva
        fields = ['voo', 'passageiro', 'numero_assento', 'classe_voo', 'status']
        widgets = {
            'voo':            forms.Select(attrs={'class': 'select'}),
            'passageiro':     forms.Select(attrs={'class': 'select'}),
            'numero_assento': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ex: 1A'}),
            'classe_voo':     forms.Select(attrs={'class': 'select'}),
            'status':         forms.Select(attrs={'class': 'select'}),
        }


class RegisterForm(UserCreationForm):
    """
    Formulário de registo de nova conta de utilizador.

    Estende o UserCreationForm do Django para incluir email
    e aplicar a classe CSS 'input' a todos os campos.
    """
    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica estilos CSS e placeholders a todos os campos
        self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Nome de utilizador'})
        self.fields['email'].widget.attrs.update({'class': 'input', 'placeholder': 'O seu e-mail'})
        self.fields['password1'].widget.attrs.update({'class': 'input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'input', 'placeholder': 'Confirmar password'})
        self.fields['email'].required = True

    def clean_email(self):
        # Garante que não há dois utilizadores com o mesmo email — essencial,
        # pois a ligação Utilizador → Passageiro (AccountView) é feita por email.
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe uma conta registada com este e-mail.')
        return email
