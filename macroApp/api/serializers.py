
from rest_framework import serializers
from .forms import RestForm
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kward={"password": {"write_only": True}}
        def create(self, validate_data):
            user = User.objects.create_user(**validate_data)
            return user