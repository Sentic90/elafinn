from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Hotel)
admin.site.register(HotelLocation)
admin.site.register(HotelMultipleImage)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(AnnualRent)
admin.site.register(Season)
admin.site.register(SeasonPrice)
