from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'dashboard.html')
def products(request):
    return render(request, 'products.html')
def customer(request):
    return render(request, 'customers.html')