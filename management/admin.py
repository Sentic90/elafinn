from django.contrib import admin

from . import models


class InvoiceItemInlines(admin.TabularInline):
    # autocomplete_fields = ['product']
    # readonly_fields = ['unit_price']
    min_num = 1
    max_num = 10
    model = models.InvoiceItem
    extra = 0

@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice_number', 'hotel', 'customer', 'status']


    inlines = [InvoiceItemInlines]


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'stock_number', 'hotel', 'status']
    list_editable = ['status']
    readonly_fields = ['total_price', 'stock_number']


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'hotel', 'total_employee']
    

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'hotel', 'department', 'is_verified', 'designation']

@admin.register(models.Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier_name', 'hotel', 'amount']

