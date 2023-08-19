from django.contrib import admin
from . import models
from .forms import CustomerAdminCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name']



    