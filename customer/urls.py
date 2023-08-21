from django.urls import path

from . import views

urlpatterns = [
    # panel
    path('panel/', views.panel, name='customer-panel'),
    path('panel/profile/', views.profile, name='customer-panel-profile'),

    # Custoemrs Booking 
    path('panel/customers/booking', views.customer_booking, name='customer-booking'),
    path('panel/customers/payments', views.payments_customer, name='customer-payments'),
]