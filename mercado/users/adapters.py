# users/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        # Si no existe username, generar uno
        if not user.username:
            base = data.get("name") or data.get("email").split("@")[0]
            username = base.replace(" ", "").lower()
            
            # evitar duplicados
            original = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{original}{counter}"
                counter += 1
            
            user.username = username

        return user
