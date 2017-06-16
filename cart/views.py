from django.shortcuts import render
from django.contrib import messages
# Create your views here.


def cart_home(request):
    return render(request, "cart_home.html")


def add_cart(request):
    messages.success(request, "Book has been added to your cart!")
    return render(request, "cart_home.html")


def check_out(request):
    return render(request, "cart_checkout.html")