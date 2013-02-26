from django.shortcuts import render

def my_custom_404_view(request):
    return render(request, '404')


def my_custom_500_view(request):
    return render(request, '500')

