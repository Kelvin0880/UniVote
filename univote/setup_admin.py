"""
Script para configurar un usuario administrador inicial en el sistema UniVote.
Ejecutar con: python manage.py shell < setup_admin.py
"""

from authentication.models import User

# Definir credenciales del administrador
admin_email = 'admin@unphu.edu.do'
admin_password = 'admin1234'
admin_first_name = 'Administrador'
admin_last_name = 'Sistema'

# Verificar si el administrador ya existe
if not User.objects.filter(email=admin_email).exists():
    print(f"Creando usuario administrador: {admin_email}")
    
    # Crear superusuario
    admin_user = User.objects.create_superuser(
        email=admin_email,
        password=admin_password,
        first_name=admin_first_name,
        last_name=admin_last_name,
        role='ADMIN'
    )
    
    print("¡Usuario administrador creado exitosamente!")
    print(f"Email: {admin_email}")
    print(f"Contraseña: {admin_password}")
else:
    print(f"El usuario administrador {admin_email} ya existe.")