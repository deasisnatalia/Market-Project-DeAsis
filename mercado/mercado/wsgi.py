import os
from django.contrib.auth import get_user_model
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado.settings')

application = get_wsgi_application()

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="Admin123!"
    )