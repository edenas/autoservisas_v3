from django.shortcuts import render
from .models import Car, Service, Order, OrderLine
# Create your views here.

def index(request):
    context = {
        'num_cars': Car.objects.count(),
        'num_service': Service.objects.count(),
        'num_orders_done': Order.objects.filter(status='c').count(),
    }
    return  render(request, template_name="index.html", context=context)