from django.test import TestCase, Client

# Create your tests here.
class UserTests(TestCase):
    def test_1(self):
        self.assertTrue(1==1)
        print(response)
        response = self.client.post(self.searchTool, {
            'cal_min': 0,
            'cal_max': 500,
    
            'fat_min' : 0 ,
            'fat_max': 200,
    
            'pro_min' : 0 , 
            'pro_max': 200,
            
            'carb_min': 0 , 
            'carb_max' : 200
        })
        
        