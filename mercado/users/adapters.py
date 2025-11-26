from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get('email') or sociallogin.user.email
        if not email:
            return
        try:
            user = User.objects.get(email=email)
            #mostrar error y redirigir.
            messages.error(
                request, 
                f"Ya existe una cuenta registrada con el correo {email}. "
                "Por favor, inicia sesión con tu contraseña"
            )
            #al login
            raise ImmediateHttpResponse(redirect('account_login'))
        except User.DoesNotExist:
            pass

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        if not user.username:
            if user.first_name:
                base = user.first_name
            elif data.get("name"):
                base = data.get("name").split()[0]
            else:
                base = user.email.split("@")[0]
            
            base = str(base)
            username = base.replace(" ", "").lower()
            
            original = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{original}{counter}"
                counter += 1
            
            user.username = username

        return user