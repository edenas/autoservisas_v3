from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('cars/', views.cars, name="cars"),
    path('cars/<int:pk>/', views.car, name="car"),
    path('orders/', views.OrderListView.as_view(), name="orders"),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name="order"),
    path('myorders/', views.UserOrderListView.as_view(), name='userorders'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/update', views.OrderUpdateView.as_view(), name='orders_update'),
]