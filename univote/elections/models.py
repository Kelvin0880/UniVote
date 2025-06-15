from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Election(models.Model):
    """Modelo para representar una elección o votación."""
    title = models.CharField(_('título'), max_length=255)
    description = models.TextField(_('descripción'))
    start_date = models.DateTimeField(_('fecha de inicio'))
    end_date = models.DateTimeField(_('fecha de fin'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='elections_created',
        verbose_name=_('creado por')
    )
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)
    is_active = models.BooleanField(_('activo'), default=True)
    
    @property
    def is_ongoing(self):
        """Determina si la elección está en curso actualmente."""
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    @property
    def has_ended(self):
        """Determina si la elección ha finalizado."""
        return timezone.now() > self.end_date
    
    @property
    def has_started(self):
        """Determina si la elección ha comenzado."""
        return timezone.now() >= self.start_date
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('elección')
        verbose_name_plural = _('elecciones')
        ordering = ['-start_date']

class Candidate(models.Model):
    """Modelo para representar un candidato en una elección."""
    election = models.ForeignKey(
        Election, 
        on_delete=models.CASCADE,
        related_name='candidates',
        verbose_name=_('elección')
    )
    name = models.CharField(_('nombre'), max_length=255)
    photo = models.ImageField(_('fotografía'), upload_to='candidates/', blank=True, null=True)
    position = models.CharField(_('posición/cargo'), max_length=100)
    bio = models.TextField(_('biografía'), blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.position} ({self.election.title})"
    
    class Meta:
        verbose_name = _('candidato')
        verbose_name_plural = _('candidatos')
        unique_together = ['election', 'name', 'position']

class Vote(models.Model):
    """Modelo para registrar votos de los usuarios."""
    election = models.ForeignKey(
        Election, 
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=_('elección')
    )
    candidate = models.ForeignKey(
        Candidate, 
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name=_('candidato')
    )
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='votes',
        verbose_name=_('votante')
    )
    timestamp = models.DateTimeField(_('fecha y hora'), auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Asegurar que election coincida con la election del candidato
        if not self.election_id:
            self.election = self.candidate.election
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('voto')
        verbose_name_plural = _('votos')
        unique_together = ['election', 'voter']  # Un usuario solo puede votar una vez por elección
