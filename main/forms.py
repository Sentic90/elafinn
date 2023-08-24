from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.widgets import DateInput
from .models import Reservation
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from dashboard.models import Booking, Hotel, Season, Request
from django.forms.widgets import SelectDateWidget
from customer.models import Customer
# Create your forms here.

User = get_user_model()

class RequestForm(forms.ModelForm):
    package = forms.ModelChoiceField(queryset=Season.objects.all(), widget=forms.widgets.Select(
        attrs={'class':'form-select form-select2'}
    ))
    

    class Meta:
        model = Request
        fields = ['room', 'guests', 'package', 'start_date', 'end_date']


    def save(self, request, slug, commit=True):
        # Get the customer from request.user
        customer = Customer.objects.get(user=request.user)

        # get Hotel from slug
        hotel = Hotel.objects.get(slug=slug)
        # Get the room from request.POST
        rooms_data = self.cleaned_data.get('room')  # Assuming 'room' is the name of the room field in the form

        fetched_rooms = hotel.room_set.filter(id__in=rooms_data).values('id','price')
        rooms = [room['id'] for room in fetched_rooms]
        totalPrice = 0
        for room in fetched_rooms:
            totalPrice += room['price']
        vat = hotel.vat
        total_with_vat = totalPrice * ((vat / 100) + 1)
        

        # Create a new instance of the associated model using form data
        request = super().save(commit=False)

        # Assign the fields
        request.total_price_with_vat = total_with_vat
        request.vat = vat
        request.hotel = hotel
        request.customer = customer
        
        # Save the booking instance to the database if commit is True
        if commit:
            request.save()

        request.room.set(rooms)
        
        hotel.room_set.filter(id__in=rooms).update(status=4) #booked
        # send confirmation emails,

        return request


class BookingForm(forms.ModelForm):
    package = forms.ModelChoiceField(queryset=Season.objects.all(), widget=forms.widgets.Select(
        attrs={'class':'form-select form-select2'}
    ))
    payment_receipt = forms.FileField(label='إيصال الدفع' ,required=False,widget=forms.widgets.FileInput(attrs={
        'class':'form-file-input'
    }))
    document = forms.FileField(label='الوثائق الثبوتية',widget=forms.widgets.FileInput(attrs={
        'class':'form-file-input'
    }))

    class Meta:
        model = Booking
        fields = ['room', 'guests', 'package', 'start_date', 'end_date', 'document','payment_receipt']


    def save(self, request, slug, commit=True):
        # Get the customer from request.user
        customer = Customer.objects.get(user=request.user)

        # get Hotel from slug
        hotel = Hotel.objects.get(slug=slug)
        # Get the room from request.POST
        rooms_data = self.cleaned_data.get('room')  # Assuming 'room' is the name of the room field in the form

        fetched_rooms = hotel.room_set.filter(id__in=rooms_data).values('id')
        rooms = [room['id'] for room in fetched_rooms]
        print(rooms)

        # Create a new instance of the associated model using form data
        booking = super().save(commit=False)

        # Assign the fields
        booking.hotel = hotel
        booking.customer = customer
        
        # Save the booking instance to the database if commit is True
        if commit:
            booking.save()

        booking.room.set(rooms)
        
        hotel.room_set.filter(id__in=rooms).update(status=4) #booked
        # send confirmation emails,

        return booking



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