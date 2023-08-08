from django.contrib import admin
from django.db.models import Count
# Register your models here.
from .models import *


class HotelAdmin(admin.ModelAdmin):
    list_display = ['hotel_name', 'total_room', 'total_capacity', 'accomadate_space']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['roomNo', 'status','capacity', 'hotel']





class RoomInline(admin.TabularInline):
    # autocomplete_fields = ['roomNo']
    # readonly_fields = ['unit_price']
    min_num = 1
    max_num = 10
    model = Room
    extra = 0

class BookingAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'status', 'total_with_vat', 'full_name', 'email']

    readonly_fields = ['vat', 'total_with_vat', 'created']
    filter_horizontal = ['room']

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(HotelLocation)
admin.site.register(HotelMultipleImage)
admin.site.register(RoomType)
admin.site.register(Room, RoomAdmin)
admin.site.register(AnnualRent)
admin.site.register(Season)
admin.site.register(SeasonPrice)
