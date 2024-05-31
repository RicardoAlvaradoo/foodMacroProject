import urllib.request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import requests
from .forms import RestForm
from requests.auth import HTTPBasicAuth
import heapq
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import json
import pdb;
# Create your views here.

data = {} 
def searchTool(request):
    
    form = RestForm()              
       
    
    if request.method == "POST":
        
       
        if  request.POST.get('macros') == 'Enter Macros' :
            # create a form instance and populate it with data from the request:
            form = RestForm(request.POST)
            #pdb.set_trace()
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...)
                print("Inside main")
                cal_min = form.cleaned_data['cal_min']
                cal_max = form.cleaned_data['cal_max']
                pro_min = form.cleaned_data['pro_min']
                pro_max = form.cleaned_data['pro_max']
                carb_min = form.cleaned_data['carb_min']
                carb_max = form.cleaned_data['carb_max']
                fat_min = form.cleaned_data['fat_min']
                fat_max = form.cleaned_data['fat_max']
                #get restaurants
                print(data)
                restaurant_list = find_nearby_places(data['latitude'], data['longitude'], 5 )
                print(restaurant_list)

                #get top 3 orders
                rest_heap = restaurant_filter(restaurant_list, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max)
                context = {'rest_heap' : rest_heap}
                print(rest_heap)
                return render(request, 'display.html',context )
                # redirect to a new URL:
        
           
        else:
            location_info = request.body.decode("utf-8")
            location_info = json.loads(location_info)
            print(location_info)
            data['latitude'] = location_info['lat']
            data['longitude'] = location_info['lon']
            print(data)
    
   
    context = {'form': form}
    return render(request, 'homePage.html', context)

#func to return top three matching orders
def restaurant_filter(rest, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max):
    rest_heap = []
    
    heapq.heapify(rest_heap)
    
    #tuple will be (score, name, [order_details])

    food_info = pd.read_excel("ms_annual_data_2022.xlsx", usecols='E, F, L:U' )
    #restaurant, item_name, calories, total
    # _fat, carbohydrates, protein
    for rest in restaurant_filter:
        for index, row in food_info.iterrows():
                if row['restaurant'] == rest:
                    print( row['item_name'], row['calories'],row['total_fat'], row['carbohydrates'], row['protein'])
                    if (not(cal_min <= row['calories'] <= cal_max )):
                        food_score = abs(row['total_fat'] - ((fat_max + fat_min) // 2) ) + abs(row['protein'] - ((pro_max + pro_min) // 2)) + abs(row['carbohydrates'] - ((carb_max + carb_min) // 2))
                        heapq.heappush(rest_heap, (food_score,[rest,  row['item_name'],row['calories'], row['total_fat'], row['carbohydrates'],row['protein'] ]))
                        if len(rest_heap) > 3:
                            heapq.heappop(rest_heap)

    
        
    return rest_heap


def find_nearby_places(lat, lon, radius):
    geolocator = Nominatim(user_agent="Food Macro")
    location = geolocator.reverse((lat, lon))
    print(f"\nYour current location: {location}\n")
    
    query = f"{'restaurant'} near {lat}, {lon}"
    try:
        places = geolocator.geocode(query, exactly_one=False, limit=None)
        if places:
            for place in places:
                place_coords = (place.latitude, place.longitude)
                place_distance = geodesic((lat, lon), place_coords).kilometers
                if place_distance <= radius:
                    print(f"{place.address} ({place_distance:.2f} km)")
        else:
            print("No nearby places found for the given type.")
    except:
        print("Error: Unable to fetch nearby places.")

