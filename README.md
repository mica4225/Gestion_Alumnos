#Sistema de Gestión Educativa#

Este proyecto es un sistema web modular desarrollado en Django (Python) para la gestión integral de datos de alumnos. Permite a los docentes (usuarios autenticados) registrar, actualizar y eliminar fichas de alumnos, generando y enviando reportes en formato PDF por correo electrónico.

Render: https://gestion-alumnos-8bdh.onrender.com

🚀 Funcionalidades Principales

Autenticación de Usuarios: Registro, inicio de sesión y cierre de sesión seguro.

Gestión de Alumnos (CRUD): Creación, lectura, actualización y eliminación de registros de alumnos.

Generación de PDF: Creación de fichas detalladas de alumnos usando la librería ReportLab.

Servicio de Email: Envío de las fichas PDF por correo electrónico utilizando el servicio SMTP de Brevo (Sendinblue).

Web Scraper: Módulo para la obtención de datos externos (ej. notas educativas o información curricular).

Despliegue en Render: Configuración completa para producción usando PostgreSQL y Gunicorn.

🛠️ Tecnologías Utilizadas

Backend: Python 3.11+

Framework: Django 4.2+

Base de Datos (Producción): PostgreSQL (en Render)

Reportes: ReportLab

Despliegue: Render, Gunicorn

Servicio de Correo: Brevo (SMTP)

💻 Configuración y Ejecución Local

Sigue estos pasos para configurar el proyecto en tu máquina local.

1. Clonar el Repositorio

git clone [https://github.com/mica4225/Gestion_Alumnos.git](https://github.com/mica4225/Gestion_Alumnos.git)
cd Gestion_Alumnos


2. Crear y Activar el Entorno Virtual

Se recomienda usar un entorno virtual para aislar las dependencias del proyecto.

# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual (Windows)
.\venv\Scripts\activate


3. Instalar Dependencias

Instala todas las librerías necesarias especificadas en requirements.txt.

pip install -r requirements.txt


4. Configurar Variables de Entorno (.env)

Crea un archivo llamado .env en la raíz del proyecto. Este archivo contendrá las credenciales sensibles, las cuales no se suben a GitHub gracias al archivo .gitignore.

Reemplaza los valores de ejemplo con tus credenciales reales (incluyendo la Clave Maestra de Brevo):

# Archivo: .env
SECRET_KEY='TU_CLAVE_SECRETA_LARGA_AQUI' 
DEBUG=True

# CONFIGURACIÓN DE CORREO ELECTRÓNICO (BREVO/SMTP)
EMAIL_HOST="smtp-relay.brevo.com"
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="TU_USUARIO_SMTP_BREVO" 
EMAIL_HOST_PASSWORD="TU_CLAVE_MAESTRA_BREVO" 

# Dirección de correo del remitente (debe estar validado en Brevo)
DEFAULT_FROM_EMAIL="maf.micaela@gmail.com"


5. Configurar la Base de Datos y el Superusuario

Ejecuta las migraciones y crea un usuario administrador para acceder al panel.

python manage.py migrate
python manage.py createsuperuser


6. Ejecutar el Servidor

python manage.py runserver
