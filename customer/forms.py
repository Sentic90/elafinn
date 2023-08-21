
from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from dashboard.models import Booking
from .models import Customer
User = get_user_model()

class CustomerAdminCreationForm(forms.ModelForm):


    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm your Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_password2(self):
        # Cheacks that the password entries matches
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("password did't match")
        return password2

    def save(self, commit=True):
        # save the provided password in hash format
        user = super(CustomerAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_customer = True
        if commit:
            user.save()
        return user


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'gender', 'phone', 'email', 'address']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({ 'class':'form-control', 'placeholder':'الاسم الاول'})
        self.fields['last_name'].widget.attrs.update({ 'class':'form-control','placeholder':'اسم العائلة'})
        self.fields['gender'].widget.attrs.update({ 'class':'form-select form-control', 'placeholder':'رقم الهاتف'})
        self.fields['phone'].widget.attrs.update({ 'class':'form-control', 'placeholder':'رقم الهاتف'})
        self.fields['email'].widget.attrs.update({ 'class':'form-control'})
        self.fields['address'].widget.attrs.update({ 'class':'form-control', 'placeholder':'العنوان'})


class BookingCustomerForm(forms.ModelForm):

    payment_receipt = forms.FileField(label='إيصال الدفع',widget=forms.widgets.FileInput(attrs={
        'class':'form-file-input'
    }))
    document = forms.FileField(label='الوثائق الثبوتية',widget=forms.widgets.FileInput(attrs={
        'class':'form-file-input'
    }))
    class Meta:
        model = Booking
        fields = ['document', 'payment_receipt']