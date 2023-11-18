import jwt
from .models import USER_Entry, Driver_Entry, Hospital
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from bson import ObjectId

JWT_SECRET_KEY = 'django-insecure-6i9o@jxm94t!sao=x%*6yhx9fyht^62ir(wzw5sre^*a%lk02'
JWT_ACCESS_TOKEN_EXPIRATION = 60
JWT_REFRESH_TOKEN_EXPIRATION = 1440
JWT_ALGORITHM = 'HS256'

class JWTAuthentication(BaseAuthentication):
    """
    Allows access only to authenticated users with valid JWT tokens.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        try:
            _, token = auth_header.split()
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except (ValueError, jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            raise AuthenticationFailed('Invalid token.')
        
        # Check for USER_Entry
        try:
            user = USER_Entry.objects.get(_id=ObjectId(payload['user_id']))
            return (user, None)
        except USER_Entry.DoesNotExist:
            pass
        
        # Check for Driver_Entry
        try:
            driver = Driver_Entry.objects.get(_id=ObjectId(payload['user_id']))
            return (driver, None)
        except Driver_Entry.DoesNotExist:
            pass
        
        # Check for Hospital
        try:
            hospital = Hospital.objects.get(_id=ObjectId(payload['user_id']))
            return (hospital, None)
        except Hospital.DoesNotExist:
            pass
        
        raise AuthenticationFailed('User not found.')






 