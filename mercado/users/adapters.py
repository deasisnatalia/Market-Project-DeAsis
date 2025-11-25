from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_username
import unicodedata
import re

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        if user.username:
            return user

        raw = data.get("name") or data.get("email").split("@")[0]

        #Normalize quita acentos, espacios, caracteres
        raw = unicodedata.normalize('NFKD', raw).encode('ascii', 'ignore').decode('ascii')
        raw = re.sub(r'[^a-zA-Z0-9_.-]', '', raw).lower()

        if not raw:
            raw = "user"

        user_username(user, raw) 

        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        return True
