from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import UserLoginForm, UserRegistrationForm, ProfileUpdateForm
from .models import User
from elections.models import Election, Vote

def home(request):
    """Vista para la página de inicio."""
    ongoing_elections = Election.objects.filter(is_active=True).order_by('-start_date')[:3]
    total_users = User.objects.filter(role='STUDENT').count()
    total_elections = Election.objects.count()
    total_votes = Vote.objects.count()
    
    context = {
        'ongoing_elections': ongoing_elections,
        'total_users': total_users,
        'total_elections': total_elections,
        'total_votes': total_votes,
    }
    return render(request, 'authentication/home.html', context)

def register(request):
    """Vista para el registro de usuarios."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'STUDENT'  # Por defecto, todos los registros son estudiantes
            user.save()
            messages.success(request, "¡Registro exitoso! Ahora puedes iniciar sesión.")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
        
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    """Vista para el inicio de sesión."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido/a, {user.first_name}!")
                return redirect('home')
            else:
                messages.error(request, "Correo electrónico o contraseña incorrectos.")
        else:
            messages.error(request, "Correo electrónico o contraseña incorrectos.")
    else:
        form = UserLoginForm()
        
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    """Vista para cerrar sesión."""
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')

@login_required
def profile(request):
    """Vista para gestionar el perfil de usuario."""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado correctamente.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
        
    return render(request, 'authentication/profile.html', {'form': form})

@login_required
def my_votes(request):
    """Vista para mostrar los votos emitidos por el usuario."""
    user_votes = Vote.objects.filter(voter=request.user).select_related('election', 'candidate')
    
    return render(request, 'authentication/my_votes.html', {'votes': user_votes})
