from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.views import generic
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.contrib import messages, auth
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


class HotelDashboard(DetailView):
    # specify the model to use
    model = Hotel
    template_name = 'dashboard/home.html'


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



def change_hotel_status(self, hotelId):
    hotel = Hotel.objects.get(id=hotelId)
    hotel.is_active = not hotel.is_active
    hotel.save()
    return redirect("my-hotel")
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


def bookings(request, slug):
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)
    rooms = Room.objects.filter(roomType__hotel__slug=slug)
    context = {
        'hotel': hotel,
        'slug': slug,
        'rooms': rooms, 
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


def booking_edit(request, slug):
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
    return render(request, 'dashboard/booking/booking-edit.html', context)


# @login_required TODO
def orders(request, slug):
    hotels = Hotel.objects.filter(user=request.user)
    h = get_object_or_404(Hotel, slug=slug)
    slug = h.slug
    hotel = Hotel.objects.get(slug=slug)
    orders = Order.objects.filter(hotel=h)
    context = {
        'hotel':hotel,
        'orders': orders,
        'slug': slug
    }
    return render(request, 'dashboard/orders/orders.html', context)





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
    return render(request, 'dashboard/payment/payment-methods.html', context)


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
