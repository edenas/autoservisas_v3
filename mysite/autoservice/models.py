from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

# Create your models here.

class Car(models.Model):
    make = models.CharField()
    model = models.CharField()
    license_plate = models.CharField()
    vin_code = models.CharField()
    client_name = models.CharField()
    description = HTMLField(default="")

    def __str__(self):
        return f"{self.make} {self.model}"

class Service(models.Model):
    name = models.CharField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    car = models.ForeignKey(to="Car", on_delete=models.CASCADE)
    client = models.ForeignKey(to=User, on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = [
        ('a', 'Administered'),
        ('k', 'Cancelled'),
        ('i', 'In Progress'),
        ('c', 'Completed'),
    ]

    status = models.CharField(choices=STATUS_CHOICES, default='a')

    def is_overdue(self):
        return self.deadline and timezone.now() > self.deadline

    def total(self):
        lines = self.lines.all()
        total = 0
        for line in lines:
            total += line.service.price * line.quantity
        return total

    def __str__(self):
        return f"{self.car} {self.date}"

class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name='lines')
    service = models.ForeignKey(to="Service", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def line_sum(self):
        return self.service.price * self.quantity

    def __str__(self):
        return f"{self.service} - {self.quantity}"