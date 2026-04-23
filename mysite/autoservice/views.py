from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Car, Service, Order, OrderLine
from django.views import generic
# Create your views here.

def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_cars': Car.objects.count(),
        'num_service': Service.objects.count(),
        'num_orders_done': Order.objects.filter(status='c').count(),
        'num_visits': num_visits,
    }
    return  render(request, template_name="index.html", context=context)

def cars(request):
    context = {
        'cars': Car.objects.all(),
    }
    return render(request, template_name="cars.html", context=context)

def car(request, pk):
    context = {
        'car': Car.objects.get(pk=pk),
    }
    return render(request, template_name="car.html", context=context)

class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"

class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "users_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

