from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=30)

    carb_min = models.IntegerField()
    carb_max = models.IntegerField()

    cal_min = models.IntegerField()
    cal_max = models.IntegerField()

    protein_min = models.IntegerField()
    protein_max = models.IntegerField()

  
    fat_min = models.IntegerField()
    fat_max = models.IntegerField()


    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    restaurant = models.CharField(max_length=30)
    order_name = models.CharField(max_length=30)
    fat = models.IntegerField()
    carb = models.IntegerField()
    protein = models.IntegerField() 
    calories = models.IntegerField()
    def __str__(self):
        return self.order_name
