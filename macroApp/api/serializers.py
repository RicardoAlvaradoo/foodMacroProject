
from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Profile, Favorite
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs={"password": {"write_only": True}}
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
            
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","user", "profile_name","cal_min", "pro_min" ,"carb_min", "fat_min", "cal_max", "pro_max",  "carb_max" , "fat_max"]
        extra_kwargs = {"user":{"read_only" : True}}
    
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id","user", "restaurant","order_name", "fat", "carb", "protein", "calories"]
        extra_kwargs = {"user":{"read_only" : True}}
   