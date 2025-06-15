from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User

class UserLoginForm(AuthenticationForm):
    """Formulario personalizado para el inicio de sesión."""
    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@unphu.edu.do'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class UserRegistrationForm(UserCreationForm):
    """Formulario personalizado para el registro de usuarios."""
    first_name = forms.CharField(
        label='Nombres', 
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Apellidos', 
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Correo electrónico institucional', 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@unphu.edu.do'})
    )
    student_id = forms.CharField(
        label='ID de estudiante', 
        max_length=10, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 20-1234'})
    )
    password1 = forms.CharField(
        label='Contraseña', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'student_id', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@unphu.edu.do'):
            raise ValidationError('Debes usar un correo electrónico institucional (@unphu.edu.do)')
        return email

class ProfileUpdateForm(forms.ModelForm):
    """Formulario para actualizar el perfil de usuario."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'student_id']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
        }