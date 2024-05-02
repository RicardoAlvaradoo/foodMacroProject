import urllib.request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import requests
from .forms import RestForm
from requests.auth import HTTPBasicAuth
import heapq
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

            rest_heap = restaurant_filter(restaurant, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max)
            context = {'rest_heap' : rest_heap}
            return render(request, 'display.html', )
            # redirect to a new URL:
            
 
    # if a GET (or any other method) we'll cr eate a blank form
    else:
        form = RestForm()
    context = {'form': form}
    return render(request, 'homePage.html', context)

#func to return top three matching orders
def restaurant_filter(rest, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max):
    rest_heap = []
    heapq.heapify(rest_heap)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "x-app-id": "2ba0e341",
        "x-app-key": "b0e46c58fe70675746ac7024ee6018a7"
    }
    url_query =  '?query=wingstop'
    url = 'https://trackapi.nutritionix.com/v2/search/instant/'
    rsp = requests.get(url + url_query, headers=headers)
    for order_item in rsp.json()['branded']:
        param = order_item['nix_item_id']
        url =  'https://trackapi.nutritionix.com/v2/search/item/' 
       
        params = {
        'nix_item_id': param  # Use the variable nix_item_id here
}

        item_dict = requests.get(url, headers=headers, params=params)
        #tuple will be (score, name, [order_details])
        print(item_dict.json())
        food_info = item_dict.json()['foods'][0]
        if (not(cal_min <= food_info['nf_calories'] <= cal_max )):
            continue

        food_score = abs(food_info['nf_total_fat'] - ((fat_max + fat_min) // 2) ) + abs(food_info['nf_protein'] - ((pro_max + pro_min) // 2)) + abs(food_info['nf_total_carbohydrate'] - ((carb_max + carb_min) // 2))
        heapq.heappush(rest_heap, (food_score, food_info['food_name'],[food_info['nf_calories'], food_info['nf_total_fat'], food_info['nf_total_carbohydrate'], food_info['nf_protein'] ] ))
        if len(rest_heap) > 3:
            heapq.heappop(rest_heap)
        
        
        
    return rest_heap

