from django.contrib.auth.backends import ModelBackend
from .models import manageUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print(f"Authenticating: {email}")
        if email is None or password is None:
            return None
        try:
            user = manageUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except manageUser.DoesNotExist:
            return None