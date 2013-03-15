from django import forms
import models

class VendorForm(forms.ModelForm):
    class Meta:
        model = models.Vendor


class MealForm(forms.ModelForm):
    class Meta:
        model = models.Meal
        exclude = ('vendor',)


class EventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        exclude = ('owner', 'date_created', 'total')


class OrderMealForm(forms.ModelForm):
    class Meta:
        model = models.OrderedMeal
        exclude = ('requester', 'event', 'order_price')


