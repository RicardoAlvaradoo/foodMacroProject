import urllib.request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .forms import RestForm

# Create your views here.

def searchTool(request):
    
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = RestForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...)
            restaurant = form.cleaned_data['restaurant']
            cal_min = form.cleaned_data['cal_min']
            cal_max = form.cleaned_data['cal_max']
            pro_min = form.cleaned_data['pro_min']
            pro_max = form.cleaned_data['pro_max']
            carb_min = form.cleaned_data['carb_min']
            carb_max = form.cleaned_data['carb_max']
            fat_min = form.cleaned_data['fat_min']
            fat_max = form.cleaned_data['fat_max']

            restaurant_filter(restaurant, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max)
            
            # redirect to a new URL:
            return  redirect('/')
 
    # if a GET (or any other method) we'll cr eate a blank form
    else:
        form = RestForm()
    context = {'form': form}
    return render(request, 'homePage.html', context)

#func to return top three matching orders
def restaurant_filter(rest, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max):
   
   
    return 