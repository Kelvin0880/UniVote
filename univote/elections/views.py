from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from .models import Election, Candidate, Vote
from .forms import ElectionForm, CandidateForm, VoteForm

def election_list(request):
    """Vista para listar todas las elecciones."""
    now = timezone.now()
    
    # Filtramos las elecciones en diferentes categorías
    active_elections = Election.objects.filter(is_active=True, start_date__lte=now, end_date__gt=now)
    upcoming_elections = Election.objects.filter(is_active=True, start_date__gt=now)
    past_elections = Election.objects.filter(end_date__lt=now)
    
    context = {
        'active_elections': active_elections,
        'upcoming_elections': upcoming_elections,
        'past_elections': past_elections,
    }
    return render(request, 'elections/election_list.html', context)

@login_required
def election_detail(request, election_id):
    """Vista para mostrar los detalles de una elección específica."""
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)
    
    # Verificar si el usuario ya ha votado en esta elección
    user_has_voted = Vote.objects.filter(election=election, voter=request.user).exists()
    
    context = {
        'election': election,
        'candidates': candidates,
        'user_has_voted': user_has_voted,
        'can_vote': election.is_ongoing and not user_has_voted,
    }
    return render(request, 'elections/election_detail.html', context)

@login_required
def election_create(request):
    """Vista para crear una nueva elección. Solo disponible para administradores."""
    if request.user.role != 'ADMIN':
        messages.error(request, "No tienes permiso para crear elecciones.")
        return redirect('election_list')
    
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save(commit=False)
            election.created_by = request.user
            election.save()
            messages.success(request, f"La elección '{election.title}' ha sido creada exitosamente.")
            return redirect('election_detail', election_id=election.id)
    else:
        form = ElectionForm()
        
    return render(request, 'elections/election_form.html', {'form': form, 'is_create': True})

@login_required
def election_edit(request, election_id):
    """Vista para editar una elección existente. Solo disponible para administradores."""
    if request.user.role != 'ADMIN':
        messages.error(request, "No tienes permiso para editar elecciones.")
        return redirect('election_list')
    
    election = get_object_or_404(Election, id=election_id)
    
    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, f"La elección '{election.title}' ha sido actualizada exitosamente.")
            return redirect('election_detail', election_id=election.id)
    else:
        form = ElectionForm(instance=election)
        
    return render(request, 'elections/election_form.html', {'form': form, 'election': election, 'is_create': False})

@login_required
def election_delete(request, election_id):
    """Vista para eliminar una elección. Solo disponible para administradores."""
    if request.user.role != 'ADMIN':
        messages.error(request, "No tienes permiso para eliminar elecciones.")
        return redirect('election_list')
    
    election = get_object_or_404(Election, id=election_id)
    
    if request.method == 'POST':
        election_title = election.title
        election.delete()
        messages.success(request, f"La elección '{election_title}' ha sido eliminada exitosamente.")
        return redirect('election_list')
    
    return render(request, 'elections/election_confirm_delete.html', {'election': election})

@login_required
def candidate_create(request):
    """Vista para crear un nuevo candidato. Solo disponible para administradores."""
    if request.user.role != 'ADMIN':
        messages.error(request, "No tienes permiso para crear candidatos.")
        return redirect('election_list')
    
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, f"El candidato '{candidate.name}' ha sido creado exitosamente.")
            return redirect('election_detail', election_id=candidate.election.id)
    else:
        form = CandidateForm()
        
    return render(request, 'elections/candidate_form.html', {'form': form, 'is_create': True})

@login_required
def candidate_edit(request, candidate_id):
    """Vista para editar un candidato existente. Solo disponible para administradores."""
    if request.user.role != 'ADMIN':
        messages.error(request, "No tienes permiso para editar candidatos.")
        return redirect('election_list')
    
    candidate = get_object_or_404(Candidate, id=candidate_id)
    
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, f"El candidato '{candidate.name}' ha sido actualizado exitosamente.")
            return redirect('election_detail', election_id=candidate.election.id)
    else:
        form = CandidateForm(instance=candidate)
        
    return render(request, 'elections/candidate_form.html', {'form': form, 'candidate': candidate, 'is_create': False})

@login_required
def candidate_delete(request, candidate_id):
    """Vista para eliminar un candidato. Solo disponible para administradores."""
    if request.user.role != 'ADMIN':
        messages.error(request, "No tienes permiso para eliminar candidatos.")
        return redirect('election_list')
    
    candidate = get_object_or_404(Candidate, id=candidate_id)
    election_id = candidate.election.id
    
    if request.method == 'POST':
        candidate_name = candidate.name
        candidate.delete()
        messages.success(request, f"El candidato '{candidate_name}' ha sido eliminado exitosamente.")
        return redirect('election_detail', election_id=election_id)
    
    return render(request, 'elections/candidate_confirm_delete.html', {'candidate': candidate})

@login_required
def vote(request, election_id):
    """Vista para que un usuario emita su voto en una elección específica."""
    election = get_object_or_404(Election, id=election_id)
    
    # Verificar si la elección está activa y en curso
    if not election.is_ongoing:
        messages.error(request, "Esta elección no está disponible para votar en este momento.")
        return redirect('election_detail', election_id=election_id)
    
    # Verificar si el usuario ya ha votado
    if Vote.objects.filter(election=election, voter=request.user).exists():
        messages.error(request, "Ya has emitido tu voto en esta elección.")
        return redirect('election_detail', election_id=election_id)
    
    if request.method == 'POST':
        form = VoteForm(election, request.POST)
        if form.is_valid():
            try:
                # Registrar el voto
                candidate = form.cleaned_data['candidate']
                vote = Vote(
                    election=election,
                    candidate=candidate,
                    voter=request.user
                )
                vote.save()
                messages.success(request, "¡Tu voto ha sido registrado exitosamente!")
                return redirect('election_detail', election_id=election_id)
            except IntegrityError:
                messages.error(request, "Ya has emitido tu voto en esta elección.")
                return redirect('election_detail', election_id=election_id)
    else:
        form = VoteForm(election)
    
    return render(request, 'elections/vote_form.html', {'form': form, 'election': election})
