from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from datetime import datetime, timedelta
from dashboard.models import AnnualRent

from django.shortcuts import render
from itertools import groupby
from django.db.models import Count


def index(request):
    return render(request, 'virtual/home.html')


def annual_offer_list(request):
    annual_rent_offers = AnnualRent.objects.filter(status=2)
    context = {
        'annual_rent_offers': annual_rent_offers
    }
    return render(request, 'virtual/annual_rental_offers/annual_rent_offers_list.html', context)
