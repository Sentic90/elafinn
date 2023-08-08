from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import Booking


def panel(request):

    return render(request, 'customer/customer_panel.html', {})


def customer_booking(request):
    bookings = Booking.objects.all()
    return render(request, 'customer/customer_booking.html', {'bookings':bookings})