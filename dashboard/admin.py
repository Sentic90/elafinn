from django.contrib import admin
from django.db.models import Count
# Register your models here.
from .models import *


class HotelAdmin(admin.ModelAdmin):
    list_display = ['hotel_name', 'total_room', 'total_capacity', 'accomadate_space']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['roomNo', 'status','capacity', 'hotel']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'status', 'total_with_vat']

    readonly_fields = ['vat', 'total_with_vat', 'created']


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(HotelLocation)
admin.site.register(HotelMultipleImage)
admin.site.register(RoomType)
admin.site.register(Room, RoomAdmin)
admin.site.register(AnnualRent)
admin.site.register(Season)
admin.site.register(SeasonPrice)
