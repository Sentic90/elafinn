from django import forms
from .models import *
from django_countries.widgets import CountrySelectWidget
from django.shortcuts import get_object_or_404


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'
        exclude = ['user', 'created', 'updated', 'is_priority', 'is_active', 'slug']
        widgets = {"country": CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["hotel_name"].widget.attrs.update({"class": "form-control"})
        self.fields["city"].widget.attrs.update({"class": "form-control"})
        self.fields["address"].widget.attrs.update({"class": "form-control"})
        self.fields["tel"].widget.attrs.update({"class": "form-control"})
        self.fields["mobile"].widget.attrs.update({"class": "form-control"})
        self.fields["category"].widget.attrs.update({"class": "form-control"})
        self.fields["Cancellation_policy"].widget.attrs.update({"class": "form-control"})
        self.fields["Cancellation_hours"].widget.attrs.update({"class": "form-control"})
        self.fields["Check_in"].widget.attrs.update({"class": "form-control time-picker w-30"})
        self.fields["Check_out"].widget.attrs.update({"class": "form-control time-picker w-30"})
        self.fields["nationality"].widget.attrs.update({"class": "form-select js-select2 select2-hidden-accessible"})
        self.fields["about_hotel"].widget.attrs.update({"class": "form-control"})
        self.fields["location"].widget.attrs.update({"class": "form-control"})
        self.fields["location"].widget.attrs['disabled'] = 'disabled'
        self.fields["logo"].widget.attrs.update({"class": "form-control"})
        self.fields["logo"].widget.attrs['required'] = 'required'


class HotelLocationForm(forms.ModelForm):
    class Meta:
        model = HotelLocation
        fields = '__all__'
        exclude = ['user', 'created', 'updated']


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = '__all__'
        exclude = ['hotel', 'created', 'updated']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["roomType"].widget.attrs.update({"class": "form-control w-50"})
        self.fields["capacity"].widget.attrs.update({"class": "form-control w-50"})


class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['roomNo', 'floor', 'status', 'is_view']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kwargs = kwargs
        self.fields["roomNo"].widget.attrs.update({"class": "form-control w-50"})
        self.fields["floor"].widget.attrs.update({"class": "form-control w-50"})
        self.fields["status"].widget.attrs.update({"class": "form-control w-50"})
        self.fields["is_view"].widget.attrs.update({"class": "form-control w-50"})


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['roomType', 'is_mine', 'owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kwargs = kwargs
        self.fields["roomNo"].widget.attrs.update({"class": "form-control w-50"})
        self.fields["floor"].widget.attrs.update({"class": "form-control w-50"})
        self.fields["capacity"].widget.attrs.update({"class": "form-control w-50"})
        self.fields["status"].widget.attrs.update({"class": "form-control w-50"})
        self.fields["is_view"].widget.attrs.update({"class": "form-control w-50"})


class SeasonPriceForm(forms.ModelForm):

    class Meta:
        model = SeasonPrice
        fields = '__all__'
        exclude = ['roomType']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kwargs = kwargs
        self.fields["season"].widget.attrs.update({"class": "form-control w-50"})
        self.fields["price"].widget.attrs.update({"class": "form-control w-50"})


class FileFieldForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = HotelMultipleImage
        fields = ['images']
        exclude = ['hotel']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["images"].widget.attrs.update({"class": "form-control"})


class AnnulRoomRentForm(forms.ModelForm):
    class Meta:
        model = AnnualRent
        fields = '__all__'
        exclude = ['hotel', 'status']

    def __init__(self, hotel_slug=None, *args, **kwargs):
        super(AnnulRoomRentForm, self).__init__(*args, **kwargs)
        self.fields["season"].widget.attrs.update({"class": "form-control"})
        self.fields["rooms"].widget.attrs.update(
            {"class": "form-select js-select2 select2-hidden-accessible", "multiple": "multiple"}
        )
        self.fields["price"].widget.attrs.update({"class": "form-control"})

        if hotel_slug:
            self.fields['rooms'].queryset = Room.objects.filter(roomType__hotel__slug=hotel_slug)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status', 'room']
        widgets = {'room': forms.widgets.SelectMultiple()}
        # exclude = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class':'form-select js-select2'})
        self.fields['room'].widget.attrs.update({'class': 'form-control'})


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['status', 'room']
        widgets = {'room': forms.widgets.SelectMultiple()}
        # exclude = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class':'form-select js-select2'})
        self.fields['room'].widget.attrs.update({'class': 'form-control'})

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['bank_name', 'status', 'ipan', 'currency', 'swifit_code', 'type']
        widgets = {
            'status': forms.widgets.Select(),
            'type': forms.widgets.Select()

            }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_name'].widget.attrs.update({'class':'form-control', 'id':'payment-name-edit', "placeholder":"اسم البنك"})
        self.fields['status'].widget.attrs.update({'class':'form-select js-select2'})
        self.fields['currency'].widget.attrs.update({'class':'form-select js-select2'})
        self.fields['ipan'].widget.attrs.update({'class':'form-control', 'id':'email-edit'})
        self.fields['swifit_code'].widget.attrs.update({'class':'form-control', 'id':'march-id-edit', "placeholder":"سويفت كود"})
        self.fields['type'].widget.attrs.update({'class':'form-select js-select2', 'id':'paymentMethod'})


class UpdatePaymentMethodForm(PaymentMethodForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class':'form-select js-select2', 'id':'paymentMethodEdit'})
# from django import forms
# from django.utils.translation import gettext_lazy as _
#
#
# class RoomSearchForm(forms.Form):
#     city = forms.CharField(max_length=100, required=False)
#     num_rooms = forms.IntegerField(min_value=1, max_value=10, initial=1)
#     num_guests = forms.IntegerField(min_value=1, max_value=10, initial=1)
#     start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     nationality = forms.CharField(max_length=100, required=False, label=_('Nationality'))