import urllib.request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .filters import PeopleFilter
from .forms import RestForm
import requests

from bs4 import BeautifulSoup as BS
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

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RestForm()
    context = {'form': form}
    return render(request, 'homePage.html', context)

#func to return top three matching orders
def restaurant_filter(rest, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  
}
    base_url = 'https://www.nutritionix.com/i/dominos/5-cheese-oven-baked-dip'
    
    info = requests.get(base_url, headers)
    print(info.text)
    #we have html, use Bsoup to parse
    
    soup = BS(info.text, 'html.parser')

    
   
    return 