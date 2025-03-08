from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Auto-link Google account to existing user with the same email
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
                raise ImmediateHttpResponse(HttpResponseRedirect("/searchai"))  # Redirect directly
            except User.DoesNotExist:
                pass