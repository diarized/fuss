# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
import forms
import models
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponseRedirect('/lunch/orders/')


def order(request, event_id=None):
    if not event_id:
        raise ValueError("Cannot process without lunch event id (should be in URL")

    if request.method == 'POST':
        form = forms.OrderMealForm(request.POST)
        if form.is_valid():
            meal_name = form.cleaned_data['name']
            event = models.Event.objects.filter(pk=event_id)
            meal = Meals.objects.filter(vendor = event.vendor, name = meal_name)
            order = models.OrderedMeal(
                requester = current_user, #TODO
                event = event,
                meal = meal,
                order_price = meal.price
            )
            order.save()
            return HttpResponseRedirect('/lunch/orders/')
    elif request.method == 'GET':
        form = forms.OrderMealForm
        return render(request, 'orders.html', { 'form': form })
        #TODO create orders.html
    else:
        raise exceptions.MethodNotKnown("Method not known: {0}".format(request.method))

@login_required
def vendor(request):
    if request.method == 'POST':
        form = forms.VendorForm(request.POST)
        if form.is_valid():
            vendor_name = form.cleaned_data['name']
            vendor = models.Vendor(name = vendor_name)
            vendor.save()
            return HttpResponseRedirect('/lunch/vendors/')
    elif request.method == 'GET':
        #TODO list vendors
        vendors = models.Vendor.objects.all()
        form = forms.VendorForm
        return render(request, 'lunch/vendors.html', { 'vendors': vendors, 'form': form })
    else:
        raise exceptions.MethodNotKnown("Method not known: {0}".format(request.method))


@login_required
def meal(request, vendor_id=None):
    if not vendor_id:
        return render(request, 'lunch/error_message.html',
            {'message': "No vendor id. What to display?"})
    if request.method == 'POST':
        form = forms.MealForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            vendor = models.Vendor.objects.get(pk=vendor_id)
            meal = models.Meal(
                name = name,
                price = price,
                vendor = vendor,
            )
            meal.save()
            #return render(request, 'lunch/error_message.html',
            #    {'message': "name = {0}, price = {1}, vendor = {3}".format(name, price, vendor_id)})
            return HttpResponseRedirect('/lunch/meals/{0}'.format(vendor_id))
        else:
            return render(request, 'lunch/error_message.html',
                {'message': "Form not valid. Panic!"})
    elif request.method == 'GET':
        form = forms.MealForm
        try:
            vendor = models.Vendor.objects.get(pk=vendor_id)
            meals = models.Meal.objects.filter(vendor=vendor)
        except Exception as e:
            return render(request, 'lunch/error_message.html', {'message': e})
        return render(request, 'lunch/meals.html',
        {
            'vendor': vendor,
            'meals': meals,
            'form': form
        })
    else:
        raise exceptions.MethodNotKnown("Method not known: {0}".format(request.method))


def event(request):
    if request.method == 'POST':
        form = forms.EventForm(request.POST)
        if form.is_valid():
            owner = current_user #TODO
            vendor = form.cleaned_data['vendor']
            close_date = form.cleaned_data['close_date']
            event = models.Event(
                name = name,
                price = price,
                vendor = vendor_id
            )
            event.save()
    elif request.method == 'GET':
        form = forms.EventForm
        return render(request, 'events.html', { 'form': form })
        #TODO create events.html
    else:
        raise exceptions.MethodNotKnown("Method not known: {0}".format(request.method))


def register_user():
    recipients = ['new_user', 'admin']
    sender = 'admin'
    subject = 'New user'
    message = 'Witamy na pokładzie.'
    from django.core.mail import send_mail
    send_mail(subject, message, sender, recipients)


