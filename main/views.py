from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.urls import reverse
from .forms import BookingForm, NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q, Sum
from datetime import datetime, timedelta
from .models import Reservation
from customer.models import Customer
from django.contrib.auth.decorators import login_required
from dashboard.models import Hotel, HotelLocation, PaymentMethod, Room, Booking, Season
from .forms import SearchForm, RoomSearchForm
from django.shortcuts import render
from itertools import groupby
from django.db.models import Count
from .filters import HotelSidebarFilter

def index(request):
    seasons = Season.objects.all().order_by('-created')
    # nationality = Hotel.objects.all().values_list('nationality')
    form = SearchForm()
    return render(request, 'main/home.html', {'seasons':seasons, 'form':form})

def result(request):
    # Initial queryset with active hotels
    queryset = Hotel.objects.filter(is_active=True)
    
    # Main search parameters
    main_search_params = {
        'city': request.GET.get('city', ''),
        'nationality': request.GET.get('nationality', ''),
        'guests': request.GET.get('guests', 0),
        'datefilter': request.GET.get('datefilter', ''),
    }
    # if 'both' and 'all' and 0 in main_search_params.values():
    # # No main search parameters provided, return all hotels
    #     return render(request, 'main/result.html', {'hotels': queryset})
    # assining to User session #TODO Room in cookies
    # Convert start and end date strings to datetime objects
    start_date = None
    end_date = None
    if main_search_params['datefilter']:
        date_range = main_search_params['datefilter'].split(" ")
        if date_range:
            start_date_str = date_range[0]
            end_date_str = date_range[3]
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
            main_search_params['start_date'] = str(start_date.strftime('%d/%m/%Y'))
            main_search_params['end_date'] = str(end_date.strftime('%d/%m/%Y'))

    # Apply filters based on main search parameters
    if main_search_params['city']:
        queryset = queryset.filter(city=main_search_params['city'])

    if main_search_params['nationality'] != 'all':
        queryset = queryset.filter(nationality__contains=main_search_params['nationality'])

    if main_search_params['guests']:
        guests_number = int(main_search_params['guests'])
        queryset = queryset.filter(room__capacity__gte=guests_number, room__status=2)

    if start_date and end_date:
        queryset = queryset.filter(
            Q(room__booking__start_date__lte=start_date) &
            Q(room__booking__end_date__gte=end_date) &
            Q(room__status=2)
        )
    
    
    
    payment_methods_choices = PaymentMethod.objects.values_list('type', flat=True).distinct()
    request.session['main_search_params'] = main_search_params
    
    request.session['payment_methods_choices'] = list(payment_methods_choices)

    # paginations
    queryset = Hotel.objects.all()
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # end pagination
    context = {
        'hotels': page_obj,
        'guests_number': main_search_params['guests'] if main_search_params['guests'] else None,
        'start_date': start_date.strftime('%m/%d/%Y') if start_date else '',
        'end_date': end_date.strftime('%m/%d/%Y') if end_date else '',
        'city': main_search_params['city'],
        'main_search_params': main_search_params,
        'payment_methods_choices': payment_methods_choices
    }

    return render(request, 'main/result.html', context)

def filtered_sidebar(request):
    queryset = Hotel.objects.filter(is_active=True)

    hotel_sidebar_filter = HotelSidebarFilter(request.GET, queryset=queryset)
    hotels = hotel_sidebar_filter.qs

    context = {
        'hotels':hotels,
        'hotel_sidebar_filter':hotel_sidebar_filter
    }
    return render(request, 'main/result.html', context)

def hotel_details(request, slug):

    customer = Customer.objects.get(user=request.user)
    hotel = Hotel.objects.get(slug=slug)
    main_search_params = request.session.get('main_search_params', {})
    if request.method == 'GET':
        
        form = BookingForm()
        context = {
            'hotel': hotel,
            'main_search_params':main_search_params, 
            'customer':customer,
            'form':form
        }
        return render(request, 'main/hotel_detail.html', context)

    if request.method == 'POST':

        rooms = Room.objects.values_list('id')[:2]
        hotel = Hotel.objects.get(slug=slug)
        booking = Booking.objects.create(
            customer=customer, hotel=hotel,start_date = datetime.now(),end_date = datetime.now()
            )
        booking.room.set([1,4])
        return redirect(reverse('customer-panel'))

def room_details(request, slug, roomId):
    # hotels/hotel_detail/<slug:slug>/rooms/<int:roomId>
    hotel = Hotel.objects.get(slug=slug)
    room = Room.objects.get(id=roomId)

    context = {
        'hotel': hotel,
        'room': room

    }

    return render(request, 'main/room_details.html', context)

def booking_add(request, slug):
    if request.method=='POST':
        
        customer = Customer.objects.get(user=request.user) #TODO handle execptions
        rooms = Room.objects.values_list('id')[:2]
        hotel = Hotel.objects.get(slug=slug)
        booking = Booking.objects.create(
            customer=customer, 
            hotel=hotel,
            start_date = datetime.now(),
            end_date = datetime.now(),
            package_id=4
            )
        booking.room.set([1,4])
        return redirect(reverse('customer-booking'))

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
                
                next_ = request.GET.get('next')
                next_post = request.POST.get('next')
                redirect_url = next_ or next_post
                if is_safe_url(redirect_url, request.get_host()):
                    return redirect(redirect_url)

                if user.is_staff:
                    return redirect("my-hotel")
                # elif user.is_customer:
                return redirect("customer-panel")
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
