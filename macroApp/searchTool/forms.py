from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class RestForm(forms.Form):
    restaurant = forms.CharField( max_length=100)
    cal_min = forms.IntegerField()
    cal_max = forms.IntegerField() 
    
    fat_min = forms.IntegerField() 
    fat_max = forms.IntegerField() 
    
    pro_min = forms.IntegerField() 
    pro_max= forms.IntegerField() 

    carb_min = forms.IntegerField() 
    carb_max = forms.IntegerField() 