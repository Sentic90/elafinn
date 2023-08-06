from django.contrib import admin

# Register your models here.
from .models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ['roomNo', 'status', 'owner']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'status', 'total_with_vat']

    readonly_fields = ['vat', 'total_with_vat', 'created']


admin.site.register(Hotel)
admin.site.register(Order, OrderAdmin)
admin.site.register(HotelLocation)
admin.site.register(HotelMultipleImage)
admin.site.register(RoomType)
admin.site.register(Room, RoomAdmin)
admin.site.register(AnnualRent)
admin.site.register(Season)
admin.site.register(SeasonPrice)
