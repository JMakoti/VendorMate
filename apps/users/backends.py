import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        logger.debug("Email authentication attempt")
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None