from django.contrib import admin
from django.db.models import Count
# Register your models here.
from .models import *


class HotelAdmin(admin.ModelAdmin):
    list_display = ['id','hotel_name', 'total_room', 'total_capacity', 'accomadate_space']

    # inlines = ['RoomInline']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['roomNo', 'status','capacity', 'hotel']
    list_editable = ['status']

class RoomInline(admin.TabularInline):
    # autocomplete_fields = ['roomNo']
    # readonly_fields = ['unit_price']
    min_num = 1
    max_num = 10
    model = Room
    extra = 0

class BookingAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'status', 'total_with_vat', 'customer']
    list_editable = ['status']
    readonly_fields = ['vat', 'total_with_vat', 'created']
    filter_horizontal = ['room']

    

class AnnualRentAdmin(admin.ModelAdmin):
    filter_horizontal = ['rooms']

@admin.register(HotelLocation)
class HotelLocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'hrm', 'latitude','longitude', 'hotel']

@admin.register(PaymentMethod)
class HotelLocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'bank_name', 'currency', 'status','type', 'hotel']


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    list_editable = ['status']

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Booking, BookingAdmin)

admin.site.register(HotelMultipleImage)
admin.site.register(RoomType)
admin.site.register(Room, RoomAdmin)
admin.site.register(AnnualRent, AnnualRentAdmin)
admin.site.register(Season)
admin.site.register(SeasonPrice)
