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

def calculate_distance(lat1, lon1, lat2, lon2):
    
    google_api="AIzaSyBO0HZnIuHmIB7qalDQ-jTsT4bXbkcFLZM"
    url= f"https://maps.googleapis.com/maps/api/directions/json?origin={lat1},{lon1}&destination={lat2},{lon2}&key={google_api}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "OK":
        distance = data["routes"][0]["legs"][0]["distance"]["text"]
        maps_link = f"https://www.google.com/maps/dir/?api=1&origin={lat1},{lon1}&destination={lat2},{lon2}"
        return distance, maps_link
    else:
        return None
    
 
