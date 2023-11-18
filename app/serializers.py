from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from .models import USER_Entry, Driver_Entry, Hospital

class USER_EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_Entry
        fields = '__all__'  # Serialize all fields

class Driver_EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver_Entry
        fields = '__all__'

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'
