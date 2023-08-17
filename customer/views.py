from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from customer.models import Customer
from dashboard.models import Booking


def panel(request):

    return render(request, 'customer/customer_panel.html', {})


def customer_booking(request):
    customer = Customer.objects.get(user=request.user)
    bookings = Booking.objects.filter(customer=customer)
    return render(request, 'customer/customer_booking.html', {'bookings':bookings})

def payments_customer(request):

    return HttpResponse('<h1>Customer Payments here!</h1>')