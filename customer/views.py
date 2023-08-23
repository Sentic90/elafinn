from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from core.models import Notification
from customer.forms import CustomerForm
from main.forms import BookingForm as BookingCustomerForm
from customer.models import Customer
from dashboard.models import Booking


def panel(request):

    messages_list = messages.get_messages(request)
    notifications = Notification.objects.filter(recipient=request.user)
    context = {
        'messages':messages_list,
        'notifications':notifications
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
    notifications = Notification.objects.filter(recipient=request.user)
    bookings = Booking.objects.filter(customer=customer).order_by('-created')

    bookings = customer.booking_set.all()
    booking_and_forms = []

    for booking in bookings:
        form = BookingCustomerForm(instance=booking)
        booking_and_forms.append((booking, form))

    context = {
        
        'booking_and_forms':booking_and_forms,
        'notifications':notifications
        
        }
    return render(request, 'customer/customer_booking.html', context)

@login_required
def payments_customer(request):
    customer = Customer.objects.get(user=request.user)
    instance = Booking.objects.filter(customer=customer).first()
    form = BookingCustomerForm(instance=instance)
    if request.method == 'POST':
        form = BookingCustomerForm(request.POST, request.FILES)
        # if form.is_valid():
        instance.payment_receipt = request.FILES['payment_receipt']
        instance.document = request.FILES['document']
        instance.save()

    
    context = {'form':form}
    return render(request, 'customer/customer_payments.html', context)