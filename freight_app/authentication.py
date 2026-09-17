from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        if not username or not password:
            return None

        # Allow login via username or email (case-insensitive)
        user = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        ).first()

        if user is None:
            User().set_password(password) # Mitigate timing attacks
            return None
            
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
