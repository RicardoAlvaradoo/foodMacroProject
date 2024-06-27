
from rest_framework import serializers
from .forms import RestForm
from django.contrib.auth.models import User
from .models import Profiles, Favorites
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs={"password": {"write_only": True}}
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
            
        return user
    
class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles 
        fields = ["id","user", "name","cal_min", "cal_max", "protein_min", "protein_max", "fat_min","fat_max",  "carb_min", "carb_max"]
        extra_kwargs = {"user":{"read_only" : True}}
class Favorite_Serializer(serializers.ModelSerializer):
      class Meta:
        model = Favorites
        fields = ["id","user", "restaurant","order_name", "fat", "carb", "calories"]
        extra_kwargs = {"user":{"read_only" : True}}