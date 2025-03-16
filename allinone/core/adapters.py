from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.state['process'] = 'connect'  # Ensure user is connected
                sociallogin.connect(request, user)  
                
                # Manually authenticate and log in the user
                login(request, user)  

                raise ImmediateHttpResponse(HttpResponseRedirect("/searchai"))  
            except User.DoesNotExist:
                pass
