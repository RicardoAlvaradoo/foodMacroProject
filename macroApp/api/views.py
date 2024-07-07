from rest_framework.response import Response

from rest_framework import generics
from .serializers import UserSerializer, ProfileSerializer, FavoriteSerializer
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.views import APIView
from rest_framework import status

import heapq
import pandas as pd
import pdb;
import os
import json
from rest_framework import status
import googlemaps
import math
from rest_framework.settings import api_settings
from .models import Profile, Favorite
import geopy.distance
from geopy.geocoders import GoogleV3
api_key = os.environ.get('api_key'),


def getData(request):
    person = {'name':'Dennis', 'age':28}
    return Response(person)

data = {'latitude': 32.735232, 'longitude': -96.6524928 } 





class Profile_Create(generics.ListCreateAPIView):
    print("correct")
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
   
    def get_queryset(self):

        user = self.request.user
        print("Current", user, "orders ", Profile.objects.filter(user=user))
        return Profile.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        
        data =  self.get_serializer(data=request.data)
        print(data)
        data.is_valid(raise_exception=True)
        self.perform_create(data)
        headers = self.get_success_headers(data)
        return Response(data.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class Profile_Delete(generics.DestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)
     
#favorites views




class Favorite_Create(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
         user = self.request.user
         return Favorite.objects.filter(user=user)
    def create(self, request, *args, **kwargs):
        
        data =  self.get_serializer(data=request.data)
        
        print(data)
        data.is_valid(raise_exception=True)
        print("SANITY CHECK1")
        self.perform_create(data)
        print("SANITY CHECK2")
        headers = self.get_success_headers(data)
        return Response(data.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class Favorite_Delete(generics.DestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
         user = self.request.user
         return Favorite.objects.filter(user=user)
#getting order logic
class Nearby_Restaurant(APIView):
    permission_classes = [AllowAny]
    def get(self, request, restaurant, latitude, longitude ):
        
        restaurant = self.kwargs["restaurant"]
        data = {'latitude': latitude, 'longitude': longitude } 
        nearby_restaurant_list = find_nearby_places(data)
        
        if restaurant in nearby_restaurant_list[0]:
            
            restaurant_index =  nearby_restaurant_list[0].index(restaurant)
            place_coord = nearby_restaurant_list[1][restaurant_index]
            
            distance_away = geopy.distance.geodesic((latitude, longitude), (place_coord['lat'], place_coord['lng']))
            geolocator = GoogleV3(api_key[0])
            restaurant_latitude = str(place_coord['lat'])
            restaurant_longitude = str(place_coord['lng'])
            
            print("HARRO",  restaurant_latitude )
            
            location = geolocator.reverse((restaurant_latitude,  restaurant_longitude ))
            return Response({"data": {'distance': distance_away, 'address':location}})
        else:{
            Response({"data": "Not Found"})
        }

class Orders(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
           
            
            post_data =  json.loads(request.body.decode('utf-8'))
            print("Current Request in Orders:",post_data)
            if  'cal_min' in post_data :
                # create a form instance and populate it with data from the request:
              
                
                #pdb.set_trace()
                # check whether it's valid:
            
                    # process the data in form.cleaned_data as required
                    # ...)
               
                cal_min = int(post_data['cal_min'])
                cal_max = int(post_data['cal_max'])
                pro_min = int(post_data['pro_min'])
                pro_max = int(post_data['pro_max'])
                carb_min = int(post_data['carb_min'])
                carb_max = int(post_data['carb_max'])
                fat_min = int(post_data['fat_min'])
                fat_max = int(post_data['fat_max'])
                #get restaurants
                location = {"latitude" : float(post_data['location']['latitude']), "longitude":float(post_data['location']['longitude'])}
                restaurant_list = find_nearby_places(location)
             

                #get top 3 orders
                rest_heap = restaurant_filter(restaurant_list, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max)
                response = []
                for i, j in rest_heap:

                    food_info =  dict(j)
                    response.append({ "food_score": i, "info":food_info, })
                  
                info_json = json.dumps(response)
                print("Data to be sent, ",info_json)
                return Response( {"data": info_json})
                
            #else:
                #location_info = request.body.decode("utf-8")
                #location_info = json.loads(location_info)
                #print("Data Value", location_info)
                #data['latitude'] = location_info['lat']
                #data['longitude'] = location_info['lon']
                
            return Response("I DK")

def restaurant_filter(rest, carb_min, carb_max, cal_min, cal_max, fat_min, fat_max, pro_min, pro_max):
    rest_heap = []
    
    heapq.heapify(rest_heap)
    
    #tuple will be (score, name, [order_details])

    food_info = pd.read_excel("ms_annual_data_2022.xlsx", usecols='E, F, L:U' )
    #restaurant, item_name, calories, total
    # _fat, carbohydrates, protein
    
    for index, row in food_info.iterrows():
            if row['restaurant'] in rest[0]:
                
                if ((cal_min <= int(row['calories']) <= cal_max )):
                    real_calories = 0 if math.isnan(float(row['calories'])) else int(row['calories'])
                    
                    real_fat = 0 if math.isnan(float(row['total_fat'])) else int(row['total_fat'])
                    real_carbs = 0 if math.isnan(float(row['carbohydrates'])) else int(row['carbohydrates'])
                    real_protein = 0 if math.isnan(float(row['protein'])) else int(row['protein'] )
                    
                    food_score = abs(real_fat- ((fat_max + fat_min) // 2) ) + abs(real_protein - ((pro_max + pro_min) // 2)) + abs(real_carbs - ((carb_max + carb_min) // 2))
                    
                
                    food_dict = {'restaurant': row['restaurant'], 'item_name' : row['item_name'], 'calories':real_calories, 'fat':  real_fat, 'carb': real_carbs, 'protein': real_protein }
                    food_tuple = (-food_score,  list(food_dict.items()))
                    
                    print("Food tuple ", food_tuple)
                    heapq.heappush(rest_heap, food_tuple )
                    
                    if len(rest_heap) > 3:
                        heapq.heappop(rest_heap)
                        print("current rest heap ",rest_heap)

    
        
    return rest_heap


def find_nearby_places(data):
    print("Key Value ",api_key[0])
    gmaps = googlemaps.Client(key = api_key[0])


    places_result = gmaps.places_nearby(location=data , radius = 1000, open_now = False, type = 'restaurant')
    
    locations = [[], []]
    for res in places_result['results']:
        locations[0].append((res['name'] ))
        locations[1].append(res['geometry']['location'])
    return locations
    
class CreateUserView(generics.CreateAPIView):
     queryset = User.objects.all()
     serializer_class = UserSerializer
     permission_classes = [AllowAny]