import datetime
import requests
import uuid
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import USER_Entry, Driver_Entry, Hospital
from rest_framework.exceptions import AuthenticationFailed

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Validation for email
        if not username:
            raise AuthenticationFailed("Email is required")
        
        user = (
            USER_Entry.objects.filter(email=username).first() or
            Driver_Entry.objects.filter(email=username).first() or
            Hospital.objects.filter(email=username).first()
        )

        if not user:
            raise AuthenticationFailed("Invalid email")

        # Validation for password
        if not password:
            raise AuthenticationFailed("Password is required")

        if not check_password(password, user.password):
            raise AuthenticationFailed("Invalid password")

        return user

