from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Vendor(models.Model):
    name = models.CharField(max_length=120)


class Meal(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    vendor = models.ForeignKey(Vendor, null=False)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True, blank=True)


class Event(models.Model):
    owner = User
    date_created = models.DateTimeField()
    vendor = models.ForeignKey(Vendor)
    close_date = models.DateTimeField()


class OrderedMeal(models.Model):
    requester = User
    event = models.ForeignKey(Event)
    meal = models.ForeignKey(Meal)


