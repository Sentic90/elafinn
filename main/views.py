from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q, Sum
from datetime import datetime, timedelta
from .models import Reservation
from dashboard.models import Hotel, Room, Order
from .forms import SearchForm, RoomSearchForm
from django.shortcuts import render
from itertools import groupby
from django.db.models import Count
from django.http import HttpResponse


def index(request):
    return render(request, 'main/home.html')


def result(request):
    # GET:  hotels/
    queryset = Hotel.objects.filter(is_active=True)

    # Queries params 
    city = request.GET.get('city', '')
    guests = request.GET.get("guests", '')
    nationality = request.GET.get("nationality")#TODO
    # datefilter = request.GET.get("datefilter")#TODO    

    """
      Search Algorithm
        - filter by city -> nationality -> number of guests
    """
    if city:
        queryset = queryset.filter(city=city)
    if nationality: 
        queryset = queryset.filter(nationality__contains=nationality)
    if guests:
        # Avaliabe accomadion space in hotels
        request.session['guests_number'] = guests
        queryset = queryset.filter(Q(room__capacity__gte=int(guests)) & Q(room__status=2))
        
        return render(request, 'main/result.html', {'hotels': queryset})    
    return render(request, 'main/result.html', {'hotels': queryset})    
    


def hotel_detail(request, slug):
    hotel = Hotel.objects.get(slug=slug)
    # hotels/hotel_detail
    return render(request, 'main/hotel_detail.html', {'hotel': hotel})


def order_add(request, slug, roomId):
    # hotels/hotel_detail/<slug:slug>/orders/add/<int:roomId>
    if request.method == 'GET':
        hotel = Hotel.objects.filter(slug=slug)[0]
        room = Room.objects.filter(id=roomId)[0]
        return render(request, 'main/order-add.html', {'hotel': hotel, 'room':room})
        


def booking_add(request, slug):
    if request.method=='POST':
        hotel = Hotel.objects.get(slug=slug)
        
        # Order.objects.create(
        #     hotel=hotel, 
        #     room=room,
        #     total_with_vat=150
        # )
        return render(request, 'main/booking_submited.html')
        

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "تم إنشاء الحساب بنجاح.")
            return redirect("main:login")
        messages.error(
            request, "لم يتم إنشاء الحساب. الرجاء التأكد من المعلومات المدخلة.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"تم تسجيل دخولك بنجاح {username}.")
                return redirect("my-hotel")
            else:
                messages.error(
                    request, "خطأ في البريد الإلكتروني أو كلمة المرور.")
        else:
            messages.error(request, "خطأ في البريد الإلكتروني أو كلمة المرور.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "تم تسجيل الخروج بنجاح.")
    return redirect("main:login")


# Chat GPT

# from django.shortcuts import render
# from django.db.models import Q
# from .models import Room, Reservation, Hotel
# from .forms import RoomSearchForm
#
#
# def room_search(request):
#     form = RoomSearchForm(request.GET or None)
#     available_rooms = None
#     available_hotels = None
#
#     if form.is_valid():
#         city = form.cleaned_data.get('city')
#         num_rooms = form.cleaned_data.get('num_rooms')
#         num_guests = form.cleaned_data.get('num_guests')
#         start_date = form.cleaned_data.get('start_date')
#         end_date = form.cleaned_data.get('end_date')
#         nationality = form.cleaned_data.get('nationality')
#
#         rooms = Room.objects.all()
#
#         if city:
#             rooms = rooms.filter(hotel__city__icontains=city)
#
#         if start_date and end_date:
#             reservations = Reservation.objects.filter(
#                 Q(start_date__lte=end_date) & Q(end_date__gte=start_date),
#                 room__in=rooms,
#             )
#             reserved_rooms = reservations.values_list('room__id', flat=True)
#             available_rooms = Room.objects.filter(
#                 id__in=reserved_rooms,
#                 capacity__gte=num_guests,
#             ).exclude(id__in=reserved_rooms)[:num_rooms]
#         else:
#             available_rooms = rooms.filter(capacity__gte=num_guests)[:num_rooms]
#
#         if nationality:
#             available_rooms = available_rooms.filter(hotel__nationality=nationality)
#
#         available_hotels = Hotel.objects.filter(rooms__in=available_rooms).distinct()
#
#     context = {
#         'form': form,
#         'available_hotels': available_hotels,
#     }
#
#     return render(request, 'room_search.html', context)

def home(request):
    return render(request, 'main/search/home.html')


def search(request):
    form = RoomSearchForm
    context = {
        'form': form
    }
    return render(request, 'main/search/search.html', context)


def search_rooms(request):
    if request.method == 'GET':
        form = RoomSearchForm(request.GET)
        if form.is_valid():
            city = form.cleaned_data.get('city')
            num_rooms = form.cleaned_data.get('num_rooms')
            num_guests = form.cleaned_data.get('num_guests')
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')
            guest_nationality = form.cleaned_data.get('guest_nationality')

            hotels = Hotel.objects.filter(
                city__icontains=city, nationality__icontains=guest_nationality)

            available_rooms = []
            for hotel in hotels:
                rm = Room.objects.filter(
                    hotel=hotel, room_capacity__gte=num_guests, is_available=True)
                rooms = rm.values('hotel__name', 'room_number', 'room_capacity').annotate(
                    num_rooms=Count('hotel__id'))
                for room in rooms:
                    reservations = Reservation.objects.filter(
                        room__room_number=room)
                    reserved_dates = []
                    for reservation in reservations:
                        check_in = reservation.check_in_date
                        check_out = reservation.check_out_date
                        if from_date <= check_in <= to_date or from_date <= check_out <= to_date:
                            reserved_dates.append(reservation)

                    if len(reserved_dates) == 0:
                        available_rooms.append(room)

            context = {'available_rooms': available_rooms}
            return render(request, 'main/search/room_search.html', context)
    else:
        form = RoomSearchForm()

    context = {'form': form}
    return render(request, 'main/search/search.html', context)
