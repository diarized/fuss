from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime


class Vendor(models.Model):
    name = models.CharField(max_length=120)


class Meal(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    vendor = models.ForeignKey(Vendor, null=False)


class Event(models.Model):
    owner = User
    date_created = models.DateTimeField(default=datetime.datetime)
    vendor = models.ForeignKey(Vendor)
    close_date = models.TimeField()
    total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


class OrderedMeal(models.Model):
    requester = User
    event = models.ForeignKey(Event)
    meal = models.ManyToManyField(Meal)
    order_price = models.DecimalField(max_digits=5, decimal_places=2)


