from django.shortcuts import render, redirect
from management.forms import EmployeeForm, ExpenseForm, StockForm

from management.models import Employee, Expense, Invoice, Stock
from .models import *
from .forms import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.contrib import messages, auth
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from geopy.distance import distance as geopy_distance
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'dashboard/hotel_information/image.html'
    success_url = reverse_lazy('hotel_image')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        hotel_id = request.POST.get('hotel')
        if form.is_valid():
            for file in request.FILES.getlist('images'):
                instance = HotelMultipleImage(
                    hotel=Hotel.objects.get(id=hotel_id),
                    images=file
                )
                instance.save()
            form.instance.hotel = hotel_id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# Create your views here.
def my_hotel(request):
    hotels = Hotel.objects.filter(user=request.user)
    hotels_count = hotels.count()
    context = {
        'hotels': hotels,
        'hotels_count': hotels_count
    }

    return render(request, "dashboard/my-hotels.html", context)


def add_hotel(request):
    form = HotelForm(request.POST, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.user = request.user
            hotel.save()
            messages.success(request, 'تم إضافة الفندق بنجاح!')
            return redirect("my-hotel")
        else:
            messages.error(request, 'خطا! لم تتم إضافة الفندق')
            return HttpResponseRedirect(reverse('my-hotel'))
    return render(request, "dashboard/add-hotel.html", {"form": form})

############  Employee area ########
# REDIRECTION_EMPLOYEE = redirect(reverse('employee-list', kwargs={'slug': hotel.slug}))


def employee_list(request, slug):
    """List + Add"""
    hotel = Hotel.objects.get(slug=slug)
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.hotel = hotel
            instance.save()

            messages.success(request, 'تم اضافة موظف جديد بنجاح')
            return redirect(reverse('employee-list', kwargs={'slug': hotel.slug}))

        messages.error(request, message='خطأ في اضافة الموظف',
                       extra_tags='danger')
        return redirect(reverse('employee-list', kwargs={'slug': hotel.slug}))

    queryset = hotel.employee_set.all()
    employee_forms = []

    # Paginations
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for employee in page_obj:
        form = EmployeeForm(instance=employee)
        employee_forms.append((employee, form))

    form = EmployeeForm()
    messages_list = messages.get_messages(request)

    context = {
        'hotel': hotel,
        'employee_forms': employee_forms,
        'form': form,
        'messages': messages_list,
        'employees':page_obj
    }

    return render(request, 'dashboard/employee/employee_list.html', context)


def employee_update(request, slug, employeeId):
    hotel = Hotel.objects.get(slug=slug)
    instance = Employee.objects.get(id=employeeId)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'تم التعديل بنجاح')
            return redirect(reverse('employee-list', kwargs={'slug': hotel.slug}))
        # TODO
        messages.error(request, message='خطأ في اضافة الموظف',
                       extra_tags='danger')
        return redirect(reverse('employee-list', kwargs={'slug': hotel.slug}))

########### End employee ########

############  Invoice area ########


def invoice_list(request, slug):

    hotel = Hotel.objects.get(slug=slug)
    queryset = hotel.invoice_set.all()

    # Paginations
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    context = {
        'hotel': hotel,
        'invoices':page_obj,
    }
    return render(request, 'dashboard/invoice/invoice_list.html', context)


def invoice_details(request, slug, invoiceId):

    invoice = Invoice.objects.get(id=invoiceId)

    hotel = Hotel.objects.get(slug=slug)
    context = {
        'hotel': hotel,
        'invoice': invoice
    }
    return render(request, 'dashboard/invoice/invoice_details.html', context)


def invoice_print(request, slug, invoiceId):

    hotel = Hotel.objects.get(slug=slug)
    invoice = Invoice.objects.get(id=invoiceId)
    context = {
        'hotel': hotel,
        'invoice': invoice
    }

    return render(request, 'dashboard/invoice/invoice_print.html', context)

############  End Invoice area ########

############  Expenses area ########


def expense_list(request, slug):
    hotel = Hotel.objects.get(slug=slug)
    queryset = hotel.expense_set.all()
    
    # Paginations
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'hotel': hotel,
        'expenses':page_obj

    }
    return render(request, 'dashboard/expense/expense_list.html', context)


def expense_details(request, slug, expenseId):

    # expense.objects.get(id=expenseId)

    hotel = Hotel.objects.get(slug=slug)
    context = {
        'hotel': hotel
    }
    return render(request, 'dashboard/expense/expense_details.html', context)


def expense_print(request, expenseId):

    # expense = expense.objects.get(id=expenseID)
    context = {
        # 'expense':{'id':1}
    }
    return render(request, 'dashboard/expense/expense_print.html', context)

############  End Expense area ########

############  Report Stock area ########


def report_stock(request, slug):
    # List + Add stock
    hotel = Hotel.objects.get(slug=slug)
    
    if request.method == 'POST':
        form = StockForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.hotel = hotel
            instance.save()
            messages.success(request, 'تم إضافة بنجاح')
            return redirect(reverse('report-stocks', kwargs={'slug': hotel.slug}))
        
        # TODO handling the error case 
        messages.error(request, message='خطأ في إضافة المخزون',
                       extra_tags='danger')
        return redirect(reverse('report-stocks', kwargs={'slug': hotel.slug}))

        
    # Paginations
    queryset = hotel.stock_set.all().order_by('-created')
    
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    stock_forms = []
    for stock in page_obj:
        form = StockForm(instance=stock)
        stock_forms.append((stock, form))

    form = StockForm()


    context = {
        'hotel': hotel,
        'stock_forms': stock_forms,
        'form': form, 
        'stocks': page_obj
    }
    return render(request, 'dashboard/report/report_stocks.html', context)

def report_stock_update(request, slug, stockId):
    hotel = Hotel.objects.get(slug=slug)
    instance = Stock.objects.get(id=stockId)

    if request.method == 'POST':
        form = StockForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'تم التعديل بنجاح')
            return redirect(reverse('report-stocks', kwargs={'slug': hotel.slug}))
        # TODO
        messages.error(request, message='خطأ في تعديل المخزون',
                       extra_tags='danger')
        return redirect(reverse('report-stocks', kwargs={'slug': hotel.slug}))

############  End Report Stock area ########


############  Report Expense area ########
def report_expense(request, slug):
    # list + add
    hotel = Hotel.objects.get(slug=slug)
    
    if request.method == 'POST':

        form = ExpenseForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.hotel = hotel
            instance.save()
            messages.success(request, 'تم إضافة بنجاح')
            return redirect(reverse('report-expenses', kwargs={'slug': hotel.slug}))
        
        # TODO handling the error message 
        messages.error(request, message='خطأ في إضافة المنصرف',
                       extra_tags='danger')
        return redirect(reverse('report-expenses', kwargs={'slug': hotel.slug}))

    queryset = hotel.expense_set.all().order_by('-created')
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    expense_forms = []

    for expense in page_obj:
        form = ExpenseForm(instance=expense)
        expense_forms.append((expense, form))

    form = ExpenseForm()
    context = {
        'hotel': hotel,
        'expense_forms': expense_forms,
        'form': form,
        'expenses':page_obj
    }
    return render(request, 'dashboard/report/report_expenses.html', context)

def report_expense_update(request, slug, expenseId):
    hotel = Hotel.objects.get(slug=slug)
    instance = Expense.objects.get(id=expenseId)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'تم التعديل بنجاح')
            return redirect(reverse('report-expenses', kwargs={'slug': hotel.slug}))
        # TODO
        print(form.errors)
        messages.error(request, message='خطأ في تعديل المنصرف',
                       extra_tags='danger')
        return redirect(reverse('report-expenses', kwargs={'slug': hotel.slug}))

############  End Expense area ########


############  Statistic Data ########

def get_statistics_data(request, slug):
    hotel = Hotel.objects.get(slug=slug)

    # Requests 
    total_request = hotel.request_set.all().count()
    this_month_request = 300
    this_week_request = 97

    # Expenses  hotel.expenses_set.all().count
    total_expenses = hotel.total_expenses_amount
    this_month_expenses = 3000
    this_week_expenses = 1250
    
    # Incomes  hotel.expenses_set.all().count
    total_income_amount = hotel.total_income_amount
    this_month_incomes = 3000
    this_week_incomes = 1250
    
    # Rooms 
    total_rooms = hotel.room_set.all().count()
    total_booked_room_this_month = 10
    total_booked_room_this_week = 10

    # Seasons الباقات
    total_booking_count_in_season = 0

    for item in Season.objects.all():
        total_booking_count_in_season += item.total_booking

    seasons = []
    for item in Season.objects.all():
        progress = (item.total_booking / total_booking_count_in_season) * 100
        seasons.append({'id':item.id, 'name': item.season, 'progress': progress})

    # hotel Steps Status
    hotel_status = {
            'imageAndLocationHasAdded': False,
            'roomsHasAdded':False,
            'isActivated':False
        }

    if hotel.hotelmultipleimage_set.count() and hotel.location:
        hotel_status.update({'imageAndLocationHasAdded': True})

    if hotel.total_room > 0:
        hotel_status.update({'roomsHasAdded': True})

    if hotel.is_active:
        hotel_status.update({'isActivated':True})

    # Booked Room
    
    booked_rooms = []
    # for room in hotel.booked_rooms:
    #     room_type = room.roomType.roomType
    #     booked_time = room.booking_set.count()
    #     booked_rooms.append({'room_type':room_type, 'booked_time':booked_time})

    # print(booked_rooms)

    booked_rooms_test = [
        {'room_type':'single', 'booked_time': 20},
        {'room_type':'double', 'booked_time':45},
        {'room_type':'triple', 'booked_time':12},
        {'room_type':'quadrble', 'booked_time':8},
    ]

    data = {
        'requests':{
        'total_request': total_request,
        'this_month_request': this_month_request,
        'this_week_request': this_week_request,
        },
        
        'expenses':{
            'total_expenses':total_expenses,
            'this_month_expenses':this_month_expenses,
            'this_week_expenses':this_week_expenses,
        },

        'rooms':{
            'total_rooms':total_rooms,
            'total_booked_room_this_month':total_booked_room_this_month,
            'total_booked_room_this_week':total_booked_room_this_week,
        },
        
        'seasons':seasons,
        
        'hotel_status':hotel_status,
        
        'incomes':{
            'total_income_amount':total_income_amount
        },

        'booked_rooms':booked_rooms_test
        # 'chart_data': {
        #     'labels': ['This Month', 'This Week'],
        #     'data': [this_month_request, this_week_request],
        # },
    }

    return JsonResponse(data)


############  End Statistic Data ########


class HotelDashboard(DetailView):
    # specify the model to use
    model = Hotel
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the 'seasons' queryset to the context
        context['seasons'] = Season.objects.all()

        return context

def index(request):
    return render(request, 'dashboard/home.html')


class HotelInformation(SuccessMessageMixin, generic.UpdateView):
    # specify the model to use
    model = Hotel
    form_class = HotelForm
    template_name = 'dashboard/hotel_information/general.html'
    success_message = "تم تحديث بيانات الفندق بنجاح!"

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        return reverse('hotel_information', kwargs={'slug': slug})


def change_hotel_status(request, hotelId):
    referer_url = request.META.get('HTTP_REFERER', None)
    hotel = Hotel.objects.get(id=hotelId)
    hotel.is_active = not hotel.is_active
    hotel.save()
    
    return redirect(referer_url)
# def show_location(request, self):
#     if 'slug' in self.kwargs:
#         slug = self.kwargs['slug']
#     else:
#         slug = 'demo'
#
#     context = {'slug': slug}
#     return render(request, 'dashboard/hotel_information/location.html', context)


class AddHotelLocation(SuccessMessageMixin, generic.CreateView):
    model = HotelLocation
    form_class = HotelLocationForm
    template_name = 'dashboard/hotel_information/location.html'
    success_message = "تم إضافة الموقع الجغرافي بنجاح!"
    success_url = 'hotel_location'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        try:
            context['locations'] = HotelLocation.objects.get(
                hotel__slug=self.kwargs['slug'])
        except HotelLocation.DoesNotExist:
            context['locations'] = None
        return context

    def form_valid(self, form):
        hotel_id = form.instance.hotel.id
        q = Hotel.objects.get(pk=hotel_id)
        print(q)
        city = q.city
        if city == 'Makkah':
            hrm = (21.4230884, 39.8305041)

        elif city == 'Madinah':
            hrm = (24.4672018, 39.6156392)

        latitude = form.instance.latitude
        longitude = form.instance.longitude
        hotel_dist = (latitude, longitude)
        d = geopy_distance(hrm, hotel_dist)
        distance = d.km
        form.instance.hrm = distance
        return super().form_valid(form)

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = ''
        return reverse('hotel_current_location', kwargs={'slug': slug})


class CurrentLocation(generic.CreateView):
    model = HotelLocation
    form_class = HotelLocationForm
    template_name = 'dashboard/hotel_information/current_location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        try:
            context['locations'] = HotelLocation.objects.get(
                hotel__slug=self.kwargs['slug'])
            context['late'] = context['locations'].latitude
            context['lange'] = context['locations'].longitude
        except HotelLocation.DoesNotExist:
            context['locations'] = None
            context['late'] = None
            context['lange'] = None
        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = 'demo'
        return reverse('hotel_current_location', kwargs={'slug': slug, 'pk': pk})


class UpdateHotelLocation(SuccessMessageMixin, generic.UpdateView):
    model = HotelLocation
    form_class = HotelLocationForm
    template_name = 'dashboard/hotel_information/update_current_location.html'
    success_message = "تم تحديث الموقع الجغرافي بنجاح!"
    success_url = 'hotel_current_location'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        context['locations'] = HotelLocation.objects.get(
            hotel__slug=self.kwargs['slug'])
        context['late'] = context['locations'].latitude
        context['lange'] = context['locations'].longitude
        context['pk'] = context['locations'].pk

        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = 'demo'
        return reverse('hotel_current_location', kwargs={'slug': slug})


def hotel_upload_images(request, slug):
    if request.method == 'POST':
        my_file = request.FILES.get('file')
        hotel = request.POST['hotel']
        h = get_object_or_404(Hotel, slug=slug)
        slug = h.slug
        HotelMultipleImage.objects.create(images=my_file, hotel_id=hotel)
        return HttpResponse('')
    return JsonResponse({'post': 'false'})


class HotelImage(generic.CreateView):
    # specify the model to use
    form_class = FileFieldForm
    template_name = 'dashboard/hotel_information/image.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        try:
            context['images'] = HotelMultipleImage.objects.filter(
                hotel__slug=self.kwargs['slug'])
        except HotelMultipleImage.DoesNotExist:
            context['images'] = None
        return context

    def form_valid(self, form):
        hotel_id = Hotel.objects.get(slug=self.kwargs['slug'])
        q = hotel_id
        my_file = self.request.FILES.get('images')
        if my_file:
            img = HotelMultipleImage(images=my_file, hotel=q)
            img.save()
        form.instance.hotel = q
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        return reverse('hotel_gallery', kwargs={'slug': slug})


def hotel_gallery(request, slug):
    hotels = Hotel.objects.filter(user=request.user)
    hotels_count = hotels.count()
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    images = HotelMultipleImage.objects.filter(hotel__slug=slug)
    hotel = Hotel.objects.get(slug=slug)

    context = {
        'hotels': hotels,
        'hotel': hotel,
        'hotels_count': hotels_count,
        'slug': slug,
        'images': images
    }

    return render(request, "dashboard/hotel_information/gallery.html", context)


def gallery_upload(request, slug):
    if request.method == "POST":
        h = get_object_or_404(Hotel, slug=slug)
        slug = h.slug
        gallery = HotelMultipleImage()
        gallery.images = request.FILES['file_name']
        gallery.hotel_id = h.id
        gallery.save()
        # Can update response as per requirement.
        # Can Add `Status`: Success/Failed to make it more clear.
        return JsonResponse({"Message": "File Uploaded Successfully"})
    return JsonResponse({"Message": ""})

# requests


def requests(request, slug):
    # url -> dashboard/my_hotel/<slug:slug>/requests
    # namespace -> request-list->
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)
    rooms = Room.objects.filter(roomType__hotel__slug=slug)
    messages_list = messages.get_messages(request)
    context = {
        'hotel': hotel,
        'slug': slug,
        'rooms': rooms,
        'messages': messages_list
    }
    return render(request, 'dashboard/requests/requests.html', context)


def request_details(request, slug, requestId):
    instance = Request.objects.get(id=requestId)

    if request.method == 'POST':
        form = RequestForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            messages.success(request, 'تم معالجة الطلب بنجاح')
            return redirect(reverse('request-list', kwargs={'slug': slug}))
    # GET
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)

    form = RequestForm(instance=instance)
    context = {
        'hotel': hotel,
        'slug': slug,
        'request': instance,
        'form': form
    }
    return render(request, 'dashboard/requests/request_details.html', context)


@login_required
def bookings(request, slug):
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)
    rooms = Room.objects.filter(roomType__hotel__slug=slug)
    messages_list = messages.get_messages(request)
    context = {
        'hotel': hotel,
        'slug': slug,
        'rooms': rooms,
        'messages': messages_list
    }
    return render(request, 'dashboard/booking/bookings.html', context)


def booking_add(request, slug):
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)
    rooms = Room.objects.filter(roomType__hotel__slug=slug)
    context = {
        'hotel': hotel,
        'slug': slug,
        'rooms': rooms
    }
    return render(request, 'dashboard/booking/booking-add.html', context)


def booking_edit(request, slug, bookingId):

    instance = Booking.objects.get(id=bookingId)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            messages.success(request, 'تم معالجة الطلب بنجاح')
            return redirect(reverse('booking-list', kwargs={'slug': slug}))
    # GET
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)

    form = BookingForm(instance=instance)
    context = {
        'hotel': hotel,
        'slug': slug,
        'booking': instance,
        'form': form
    }
    return render(request, 'dashboard/booking/booking-edit.html', context)


class RoomTypeView(generic.ListView):
    model = RoomType
    form_class = RoomTypeForm
    template_name = 'dashboard/rooms/room-type.html'
    context_object_name = 'types'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        try:
            context['types'] = RoomType.objects.filter(
                hotel__slug=self.kwargs['slug'])
        except RoomType.DoesNotExist:
            context['types'] = None
        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        return reverse('room-type', kwargs={'slug': slug})


class RoomTypeDetailView(generic.UpdateView):
    model = RoomType
    form_class = RoomTypeForm
    template_name = 'dashboard/rooms/add_room_type.html'
    context_object_name = 'types'
    success_url = 'room-type'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        try:
            context['types'] = RoomType.objects.filter(
                hotel__slug=self.kwargs['slug'])
        except RoomType.DoesNotExist:
            context['types'] = None
        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = ''
        return reverse('room-type', kwargs={'slug': slug})


class CreateRoomTypeView(SuccessMessageMixin, generic.CreateView):
    model = RoomType
    form_class = RoomTypeForm
    template_name = 'dashboard/rooms/add_room_type.html'
    success_message = "تم إضافة نوع الغرفة بنجاح!"
    success_url = 'room-type'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        try:
            context['types'] = RoomType.objects.filter(
                hotel__slug=self.kwargs['slug'])
        except RoomType.DoesNotExist:
            context['types'] = None
        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        return reverse('room-type', kwargs={'slug': slug})

    def form_valid(self, form, **kwargs):
        hotel = Hotel.objects.get(slug=self.kwargs['slug'])
        form.instance.hotel = hotel
        return super().form_valid(form)


class RoomListView(generic.ListView):
    model = Room
    template_name = 'dashboard/rooms/room-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        try:
            context['rooms'] = Room.objects.filter(
                hotel__slug=self.kwargs['slug'])
        except Room.DoesNotExist:
            context['rooms'] = None

        try:
            context['roomType'] = RoomType.objects.filter(
                hotel__slug=self.kwargs['slug'])
        except RoomType.DoesNotExist:
            context['roomType'] = None
        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        return reverse('room-list', kwargs={'slug': slug})


def room_list(request, slug):
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)
    rooms = Room.objects.filter(roomType__hotel__slug=slug)
    roomType = RoomType.objects.filter(hotel__slug=slug)

    context = {
        'hotel': hotel,
        'slug': slug,
        'rooms': rooms,
        'roomType': roomType,
    }
    return render(request, 'dashboard/rooms/room-list.html', context)


def room_grid(request, slug):
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)
    rooms = Room.objects.filter(roomType__hotel__slug=slug)
    roomType = RoomType.objects.filter(hotel__slug=slug)
    context = {
        'hotel': hotel,
        'slug': slug,
        'rooms': rooms,
        'roomType': roomType,
    }
    return render(request, 'dashboard/rooms/room-grid.html', context)


class CreateRoomView(SuccessMessageMixin, generic.CreateView):
    model = Room
    form_class = AddRoomForm
    template_name = 'dashboard/rooms/add_room.html'
    success_message = "تم إضافة الغرفة بنجاح!"
    success_url = 'room_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        context['Types'] = RoomType.objects.filter(
            hotel__slug=self.kwargs['slug'])
        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        return reverse('room-list', kwargs={'slug': slug})

    def form_valid(self, form, **kwargs):
        type = self.request.POST.get('roomType')
        types = RoomType.objects.get(id=type)
        form.instance.roomType = types
        form.instance.capacity = types.capacity
        form.instance.Electric = types.Electric
        form.instance.Services = types.Services
        form.instance.Facilities = types.Facilities
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     roomT = request.POST.get('roomType')
    #     type = RoomType.objects.get(roomType=roomT)
    #     print(type.id)
    #     if form.is_valid():
    #         form.instance.roomType = type.id,
    #
    #         instance = Room(
    #             roomNo=form.instance.roomNo,
    #             floor=form.instance.floor,
    #             capacity=type.capacity,
    #             Electric = type.Electric,
    #             Facilities = type.Facilities,
    #             Services = type.Services,
    #         )
    #         instance.save()
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)


class RoomDetailView(generic.UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'dashboard/rooms/add_room.html'
    context_object_name = 'rooms'
    success_url = 'room-list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        context['Types'] = RoomType.objects.filter(
            hotel__slug=self.kwargs['slug'])
        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = ''
        return reverse('room-list', kwargs={'slug': slug})


def season_price_list(request, slug):
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)
    rooms = RoomType.objects.filter(hotel__slug=slug)
    roomType = RoomType.objects.filter(hotel__slug=slug)

    seasons = SeasonPrice.objects.filter(roomType__hotel__slug=slug)
    context = {
        'hotel': hotel,
        'slug': slug,
        'rooms': rooms,
        'roomType': roomType,
        'seasons': seasons
    }
    return render(request, 'dashboard/price/price_list.html', context)


class CreateSeasonPriceView(SuccessMessageMixin, generic.CreateView):
    model = SeasonPrice
    form_class = SeasonPriceForm
    template_name = 'dashboard/price/add_price.html'
    success_message = "تم إضافة السعر بنجاح!"
    success_url = 'season-price-list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        context['Types'] = RoomType.objects.filter(
            hotel__slug=self.kwargs['slug'])
        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        return reverse('season-price-list', kwargs={'slug': slug})

    def form_valid(self, form, **kwargs):
        type = self.request.POST.get('roomType')
        types = RoomType.objects.get(id=type)
        form.instance.roomType = types
        return super().form_valid(form)


class SeasonPriceDetailView(generic.UpdateView):
    model = SeasonPrice
    form_class = SeasonPriceForm
    template_name = 'dashboard/price/add_price.html'
    context_object_name = 'seasons'
    success_url = 'season-price-list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        context['Types'] = RoomType.objects.filter(
            hotel__slug=self.kwargs['slug'])
        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = ''
        return reverse('season-price-list', kwargs={'slug': slug})


def customer(request, slug):
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)
    rooms = Room.objects.filter(roomType__hotel__slug=slug)
    context = {
        'hotel': hotel,
        'slug': slug,
        'rooms': rooms
    }
    return render(request, 'dashboard/customer/customer-list.html', context)


def payment_methods(request, slug):
    hotel = Hotel.objects.get(slug=slug)

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.hotel = hotel
            myform.save()
            messages.success(request, 'تم اضافة وسيلة الدفع بنجاح')
            return redirect(reverse('payment-methods', kwargs={'slug': slug}))
        print(form.errors.as_text)
        messages.error(request, form.errors)
        return redirect(reverse('payment-methods', kwargs={'slug': slug}))

    payment_methods = hotel.payment_methods.all()
    payment_methods_forms = []

    for payment_method in payment_methods:
        form = UpdatePaymentMethodForm(instance=payment_method)
        payment_methods_forms.append((payment_method, form))
    messages_list = messages.get_messages(request)
    rooms = Room.objects.filter(roomType__hotel__slug=slug)
    form = PaymentMethodForm()
    context = {
        'hotel': hotel,
        'slug': slug,
        'rooms': rooms,
        'payment_methods_forms': payment_methods_forms,
        'messages': messages_list,
        'form': form
    }
    return render(request, 'dashboard/payment/payment-methods.html', context)


def payment_method_edit(request, slug, paymentMethodId):
    instance = PaymentMethod.objects.get(id=paymentMethodId)

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'تم معالجة الطلب بنجاح')
            return redirect(reverse('payment-methods', kwargs={'slug': slug}))

        messages.error(request, form.errors)
        return redirect(reverse('payment-methods', kwargs={'slug': slug}))


def rooms_for_annual_rent(request, slug):
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)
    annual_list = AnnualRent.objects.filter(hotel__slug=slug)

    context = {
        'hotel': hotel,
        'slug': slug,
        'annual_list': annual_list

    }
    return render(request, 'dashboard/annual_rent/owner/annual_rent_list.html', context)


class AnnualRentAddView(SuccessMessageMixin, generic.CreateView):
    model = AnnualRent
    form_class = AnnulRoomRentForm
    template_name = 'dashboard/annual_rent/owner/add.html'
    context_object_name = 'annual_rent'
    success_url = 'annual_rent'
    success_message = "تم إضافة القائمة بنجاح!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['slug'] = slug
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        context['form'] = AnnulRoomRentForm(hotel_slug=slug)
        return context

    def form_valid(self, form, **kwargs):
        hotel = Hotel.objects.get(slug=self.kwargs['slug'])
        form.instance.hotel = hotel
        return super().form_valid(form)

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = ''
        return reverse('annual_rent', kwargs={'slug': slug})


class AnnualRentView(SuccessMessageMixin, generic.UpdateView):
    model = AnnualRent
    form_class = AnnulRoomRentForm
    template_name = 'dashboard/annual_rent/owner/update.html'
    success_url = 'annual_rent'
    success_message = 'تم تحديث المعلومات بنجاح!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        pk = self.kwargs['pk']
        context['slug'] = slug
        context['pk'] = pk
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        return context

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = 'demo'
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = ''
        return reverse('annual_rent', kwargs={'slug': slug})
