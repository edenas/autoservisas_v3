from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, reverse
from django.urls import reverse_lazy

from .models import Car, Service, Order, OrderLine
from django.views import generic
from .forms import OrderCreateUpdateForm
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

class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    template_name = "order_from.html"
    form_class = OrderCreateUpdateForm
    success_url = reverse_lazy('userorders')

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.save()
        return super().form_valid(form)

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    template_name = "order_from.html"
    form_class = OrderCreateUpdateForm

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.get_object().client == self.request.user

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    template_name = "orders_delete.html"
    context_object_name = "order"
    success_url = reverse_lazy('userorders')

    def test_func(self):
        return self.get_object().client == self.request.user

class OrderLineCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = OrderLine
    template_name = "orderline_form.html"
    fields = ['service', 'quantity']

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.kwargs['pk']})

    def test_func(self):
        return Order.objects.get(pk=self.kwargs['pk']).client == self.request.user

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

class OrderLineUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = OrderLine
    template_name = "orderline_form.html"
    fields = ['service', 'quantity']

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.order.pk})

    def test_func(self):
        return self.get_object().order.client == self.request.user

class OrderLineDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = OrderLine
    template_name = "orderline_delete.html"
    context_object_name = "orderline"

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.order.pk})

    def test_func(self):
        return self.get_object().order.client == self.request.user