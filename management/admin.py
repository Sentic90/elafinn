from django.contrib import admin

from .models import Invoice, InvoiceItem



class InvoiceItemInlines(admin.TabularInline):
    # autocomplete_fields = ['product']
    # readonly_fields = ['unit_price']
    min_num = 1
    max_num = 10
    model = InvoiceItem
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice_number', 'hotel', 'customer', 'status']


    inlines = [InvoiceItemInlines]

