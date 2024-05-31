from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import RestForm
from django.shortcuts import render, redirect

from django.template import loader

from .forms import RestForm

import heapq
import pandas as pd

import os
import json
import pdb;
import googlemaps
import math
api_key = os.environ.get('api_key'),
@api_view(['GET'])
def getData(request):
    person = {'name':'Dennis', 'age':28}
    return Response(person)

data = {'latitude': 32.735232, 'longitude': -96.6524928 } 
@api_view(['POST'])
def orders(request):
        print(request)
        if  request.POST.get('macros') == 'Enter Macros' :
            # create a form instance and populate it with data from the request:
            print(request.POST)
            print(request)
            serializer = RestForm(request.POST)
            #pdb.set_trace()
            # check whether it's valid:
            if serializer.is_valid():
                # process the data in form.cleaned_data as required
                # ...)
                
                cal_min = serializer.cleaned_data['cal_min']
                cal_max = serializer.cleaned_data['cal_max']
                pro_min = serializer.cleaned_data['pro_min']
                pro_max = serializer.cleaned_data['pro_max']
                carb_min = serializer.cleaned_data['carb_min']
                carb_max = serializer.cleaned_data['carb_max']
                fat_min = serializer.cleaned_data['fat_min']
                fat_max = serializer.cleaned_data['fat_max']
                #get restaurants
                
                restaurant_list = find_nearby_places()
                print(restaurant_list)

                #get top 3 orders
                rest_heap = restaurant_filter(restaurant_list, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max)
                restaurant_info = {'data' : rest_heap}
                info_json = json.dumps(restaurant_info)
                return Response(info_json)
                # redirect to a new URL:
        #else:
            #location_info = request.body.decode("utf-8")
            #location_info = json.loads(location_info)
            #print("Data Value", location_info)
            #data['latitude'] = location_info['lat']
            #data['longitude'] = location_info['lon']
            
            
def restaurant_filter(rest, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max):
    rest_heap = []
    
    heapq.heapify(rest_heap)
    
    #tuple will be (score, name, [order_details])

    food_info = pd.read_excel("ms_annual_data_2022.xlsx", usecols='E, F, L:U' )
    #restaurant, item_name, calories, total
    # _fat, carbohydrates, protein
    
    for index, row in food_info.iterrows():
            if row['restaurant'] in rest:
                
                if ((cal_min <= int(row['calories']) <= cal_max )):
                    real_calories = 0 if math.isnan(float(row['calories'])) else int(row['calories'])
                    
                    real_fat = 0 if math.isnan(float(row['total_fat'])) else int(row['total_fat'])
                    real_carbs = 0 if math.isnan(float(row['carbohydrates'])) else int(row['carbohydrates'])
                    real_protein = 0 if math.isnan(float(row['protein'])) else int(row['protein'] )
                    
                    food_score = abs(real_fat- ((fat_max + fat_min) // 2) ) + abs(real_protein - ((pro_max + pro_min) // 2)) + abs(real_carbs - ((carb_max + carb_min) // 2))
                    
                 

                    food_tuple = (-food_score,(row['restaurant'],  row['item_name'],real_calories, real_fat, real_carbs,real_protein))
                    
                    heapq.heappush(rest_heap, food_tuple )
                    
                    if len(rest_heap) > 3:
                        heapq.heappop(rest_heap)
                        print(rest_heap)

    
        
    return rest_heap


def find_nearby_places():
    print("Key Value ",api_key[0])
    gmaps = googlemaps.Client(key = api_key[0])
   
   
    places_result = gmaps.places_nearby(location=data , radius = 1000, open_now = False, type = 'restaurant')
    
    locations = []
    for res in places_result['results']:
        locations.append(res['name'])
    return locations
    
