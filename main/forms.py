from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.widgets import DateInput
from .models import Reservation
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from dashboard.models import Hotel
from django.forms.widgets import SelectDateWidget
from customer.models import Customer
# Create your forms here.

User = get_user_model()
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RoomSearchForm(forms.Form):
    city = forms.CharField(label='City', max_length=100)
    num_rooms = forms.IntegerField(label='Number of Rooms')
    num_guests = forms.IntegerField(label='Number of Guests')
    from_date = forms.DateField(label='Check-in Date', widget=DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(label='Check-out Date', widget=DateInput(attrs={'type': 'date'}))
    guest_nationality = forms.ChoiceField(label='Guest Nationality', choices=(('', '---'),) + Reservation._meta.get_field('guest_nationality').choices)


class SearchForm(forms.ModelForm):
    # city = forms.CharField(label='City', max_length=100)
    num_rooms = forms.IntegerField(label='Number of rooms', min_value=1, max_value=10)
    num_guests = forms.IntegerField(label='Number of guests', min_value=1, max_value=20)
    from_date = forms.DateField(label='Check-in date', widget=SelectDateWidget())
    to_date = forms.DateField(label='Check-out date', widget=SelectDateWidget())
    # nationality = CountryField().formfield(blank_label="(select country)", widgets=forms.widgets.Select(attrs={'class':'form-select form-control'}))
    guest_nationality = forms.ChoiceField(label='Guest nationality', choices=(('', '---'),) + Reservation._meta.get_field('guest_nationality').choices)
    
    class Meta:
        model = Hotel
        fields = ['nationality', 'city']
        widgets = {
            'nationality': forms.widgets.Select(attrs={'class':'form-select form-control'}),
            # 'city': forms.widgets.Select(attrs={'class':'form select form-control'})
            }