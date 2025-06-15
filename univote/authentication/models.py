from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re

def validate_unphu_email(value):
    if not value.endswith('@unphu.edu.do'):
        raise ValidationError(
            _('El correo electrónico debe ser institucional (@unphu.edu.do)'),
            code='invalid_email'
        )

class UserManager(BaseUserManager):
    """Define un gestor de modelo para Usuario con email como identificador único."""
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un Usuario con el email y contraseña dados."""
        if not email:
            raise ValueError(_('El correo electrónico es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un SuperUsuario con el email y contraseña dados."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('El superusuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('El superusuario debe tener is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Modelo de usuario personalizado con email como identificador único."""
    ROLE_CHOICES = (
        ('STUDENT', 'Estudiante'),
        ('ADMIN', 'Administrador'),
    )
    
    username = None
    email = models.EmailField(_('correo electrónico'), unique=True, validators=[validate_unphu_email])
    first_name = models.CharField(_('nombres'), max_length=150)
    last_name = models.CharField(_('apellidos'), max_length=150)
    role = models.CharField(_('rol'), max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    student_id = models.CharField(_('ID de estudiante'), max_length=10, blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def clean(self):
        super().clean()
        if self.role == 'STUDENT' and not self.student_id:
            raise ValidationError(_('Los estudiantes deben proporcionar su ID de estudiante.'))
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
        
    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
