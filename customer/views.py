from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from customer.forms import CustomerForm
from customer.models import Customer
from dashboard.models import Booking


def panel(request):
    messages_list = messages.get_messages(request)
    context = {
        'messages':messages_list
    }
    return render(request, 'customer/customer_panel.html', context)

def profile(request):
    customer = Customer.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()

            messages.success(request, 'تم تعديل الملف الشخصي بنجاح')
            return redirect(reverse('customer-panel'))
        print(form.errors)
    form = CustomerForm(instance=customer)

    context = {
        'form':form
    }
    return render(request, 'customer/profile.html', context)
    

def customer_booking(request):
    customer = Customer.objects.get(user=request.user)
    bookings = Booking.objects.filter(customer=customer)
    return render(request, 'customer/customer_booking.html', {'bookings':bookings})

def payments_customer(request):

    return HttpResponse('<h1>Customer Payments here!</h1>')