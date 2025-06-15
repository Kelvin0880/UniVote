from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from django.utils import timezone
from elections.models import Election, Candidate, Vote
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

@login_required
def result_dashboard(request):
    """Vista para mostrar un dashboard de resultados de todas las elecciones."""
    if request.user.role != 'ADMIN':
        messages.error(request, "No tienes permiso para acceder al dashboard de resultados.")
        return redirect('home')
    
    # Obtener todas las elecciones finalizadas
    ended_elections = Election.objects.filter(end_date__lt=timezone.now()).order_by('-end_date')
    ongoing_elections = Election.objects.filter(
        start_date__lte=timezone.now(),
        end_date__gt=timezone.now()
    ).order_by('end_date')
    upcoming_elections = Election.objects.filter(start_date__gt=timezone.now()).order_by('start_date')
    
    # Estadísticas generales
    total_votes = Vote.objects.count()
    total_candidates = Candidate.objects.count()
    
    context = {
        'ended_elections': ended_elections,
        'ongoing_elections': ongoing_elections,
        'upcoming_elections': upcoming_elections,
        'total_votes': total_votes,
        'total_candidates': total_candidates,
    }
    
    return render(request, 'results/result_dashboard.html', context)

@login_required
def election_results(request, election_id):
    """Vista para mostrar los resultados detallados de una elección específica."""
    election = get_object_or_404(Election, id=election_id)
    
    # Si la elección aún no ha terminado y el usuario no es administrador, redirigir
    if not election.has_ended and request.user.role != 'ADMIN':
        messages.error(request, "Los resultados de esta elección aún no están disponibles.")
        return redirect('election_detail', election_id=election_id)
    
    # Obtener los resultados de la votación
    candidates = Candidate.objects.filter(election=election).annotate(
        votes_count=Count('votes')
    ).order_by('-votes_count')
    
    # Calcular el total de votos y el porcentaje para cada candidato
    total_votes = Vote.objects.filter(election=election).count()
    for candidate in candidates:
        candidate.percentage = (candidate.votes_count / total_votes * 100) if total_votes > 0 else 0
    
    context = {
        'election': election,
        'candidates': candidates,
        'total_votes': total_votes,
    }
    
    return render(request, 'results/election_results.html', context)

@login_required
def election_results_pdf(request, election_id):
    """Vista para generar un informe PDF con los resultados de la elección."""
    election = get_object_or_404(Election, id=election_id)
    
    # Permitir exportación en cualquier momento, manteniendo la restricción para no administradores
    if not election.has_ended and request.user.role != 'ADMIN':
        messages.error(request, "Los resultados de esta elección aún no están disponibles.")
        return redirect('election_detail', election_id=election_id)
    
    # Obtener los resultados de la votación
    candidates = Candidate.objects.filter(election=election).annotate(
        votes_count=Count('votes')
    ).order_by('-votes_count')
    
    # Calcular el total de votos y el porcentaje para cada candidato
    total_votes = Vote.objects.filter(election=election).count()
    
    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Título
    elements.append(Paragraph(f"Resultados: {election.title}", title_style))
    elements.append(Paragraph(f"Fecha de inicio: {election.start_date.strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Paragraph(f"Fecha de fin: {election.end_date.strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Paragraph(f"Total de votos: {total_votes}", normal_style))
    elements.append(Paragraph(" ", normal_style))  # Espacio en blanco
    
    # Tabla de resultados
    data = [['Candidato', 'Cargo', 'Votos', 'Porcentaje']]
    for candidate in candidates:
        percentage = (candidate.votes_count / total_votes * 100) if total_votes > 0 else 0
        data.append([
            candidate.name,
            candidate.position,
            str(candidate.votes_count),
            f"{percentage:.2f}%"
        ])
    
    # Crear tabla
    table = Table(data, colWidths=[120, 120, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Generar PDF
    doc.build(elements)
    buffer.seek(0)
    
    # Crear respuesta
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resultados_{election.id}.pdf"'
    
    return response

@login_required
def election_results_export(request, election_id):
    """Vista para exportar los resultados de la elección a CSV."""
    election = get_object_or_404(Election, id=election_id)
    
    # Permitir exportación en cualquier momento, manteniendo la restricción para no administradores
    if not election.has_ended and request.user.role != 'ADMIN':
        messages.error(request, "Los resultados de esta elección aún no están disponibles.")
        return redirect('election_detail', election_id=election_id)
    
    # Obtener los resultados de la votación
    candidates = Candidate.objects.filter(election=election).annotate(
        votes_count=Count('votes')
    ).order_by('-votes_count')
    
    # Calcular el total de votos y el porcentaje para cada candidato
    total_votes = Vote.objects.filter(election=election).count()
    
    # Crear respuesta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="resultados_{election.id}.csv"'
    
    # Crear el escritor CSV
    writer = csv.writer(response)
    writer.writerow(['Candidato', 'Cargo', 'Votos', 'Porcentaje'])
    
    for candidate in candidates:
        percentage = (candidate.votes_count / total_votes * 100) if total_votes > 0 else 0
        writer.writerow([
            candidate.name,
            candidate.position,
            candidate.votes_count,
            f"{percentage:.2f}%"
        ])
    
    return response
