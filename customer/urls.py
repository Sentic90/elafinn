from django.urls import path

from . import views

urlpatterns = [
    # panel
    path('panel/', views.panel, name='customer-panel'),

    # Custoemrs Booking 
    path('panel/customers/booking', views.customer_booking, name='customer-booking'),
    path('panel/customers/payments', views.payments_customer, name='payments-customer'),
]