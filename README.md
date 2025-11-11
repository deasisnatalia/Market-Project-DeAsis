DEPENDENCIAS

Python 3.8+
django
pillow
djangorestframework
psycopg2-binary
requests beautifulsoup4
django-allauth
PyJWT
criptography
mercadopago

INSTALACION Y CONFIGURACION

Clonar el repositorio git clone https://github.com/deasisnatalia/Market-Project-DeAsis.git
Crear entorno virtual python -m venv venv venv\Scripts\activate
Instalar dependencias
Aplicar migraciones python manage.py makemigrations python manage.py migrate
Crear Superusuario python manage.py createsuperuser
Iniciar el servidor python manage.py runserver
