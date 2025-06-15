# UniVote - Sistema de Votación Universitaria

UniVote es una plataforma de votación electrónica diseñada específicamente para la Universidad Nacional Pedro Henríquez Ureña (UNPHU). El sistema permite la organización y ejecución de elecciones estudiantiles de manera segura, transparente y accesible.

## Características

- **Autenticación segura**: Acceso exclusivo para miembros de la comunidad universitaria con correo institucional (@unphu.edu.do)
- **Roles de usuario**: Administradores y estudiantes con diferentes niveles de permisos
- **Gestión completa de elecciones**: Crear, editar y eliminar elecciones
- **Gestión de candidatos**: Añadir candidatos con fotografía y biografía
- **Sistema de votación**: Proceso de votación sencillo y seguro
- **Resultados en tiempo real**: Visualización gráfica de los resultados 
- **Exportación de datos**: Posibilidad de exportar resultados en formato PDF y CSV
- **Diseño responsivo**: Interfaz adaptable a dispositivos móviles

## Requisitos técnicos

- Python 3.8 o superior
- Django 5.2.3
- MySQL 8.0 o superior
- Librería Pillow para el manejo de imágenes
- ReportLab para generación de PDFs
- Crispy Forms para mejorar los formularios
- Bootstrap 5 para el diseño frontend

## Instalación

### 1. Preparar el entorno

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/univote.git
cd univote

# Crear y activar un entorno virtual
# En Windows:
python -m venv venv
venv\Scripts\activate

# En macOS/Linux:
python3 -m venv venv
source venv/bin/activate

 # Ejecutar el servidor de desarrollo 

 python manage.py runserver



 -------------------------------------------------------------------------------------------------

 Acceso al sistema
Una vez que el servidor esté corriendo, puedes acceder a:

Interfaz principal: http://127.0.0.1:8000/
Panel de administración: http://127.0.0.1:8000/admin/
Credenciales predeterminadas del administrador
Email: admin@unphu.edu.do
Contraseña: admin1234

Uso del sistema
Administradores
Como administrador puedes:

Crear y gestionar elecciones
Añadir candidatos a las elecciones
Ver estadísticas y resultados en tiempo real
Exportar los resultados de las elecciones a PDF o CSV

Acceder al dashboard de resultados
Estudiantes
Como estudiante puedes:

Ver las elecciones disponibles
Votar en elecciones activas (una vez por elección)
Ver tus votos emitidos
Ver resultados de elecciones finalizadas