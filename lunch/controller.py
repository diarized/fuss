from django.shortcuts import render
from django.http import HttpResponseRedirect
import forms
import models
import logging
logger = logging.getLogger(__name__)

def index(request):
    pass


def vendor(request):
    pass


def meal(request, vendor_id=None):
    if not vendor:
        raise ValueError("No ")
    if request.method == 'POST':
        form = forms.MealForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            new_meal = models.Meal(
                    name = name,
                    price = price,
                    vendor = vendor_id,
                )
            new_meal.save()
            return HttpResponseRedirect('/lunch/meals/{0}'.format(vendor_id))
    else:
        form = forms.MealForm()

    meals = models.Meal.objects.all()
    return render(request, 'meals.html',
            { 'form': form, 'meals': meals, 'vendor': vendor_id })


def order(request, order=1):
    pass

def event(request):
    pass
