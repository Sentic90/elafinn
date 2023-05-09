from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Hotel(models.Model):
    city = models.CharField(_("City"), max_length=100)
    name = models.CharField(_("Name"), max_length=100)
    nationality_choices = (
        ("US", "US"),
        ("UK", "UK"),
        ("FR", "FR"),
    )
    nationality = models.CharField(_("Nationality"), max_length=2, choices=nationality_choices)

    # add more fields as required

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hotel_detail', args=[str(self.id)])


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(_("Room Number"), max_length=10)
    room_capacity = models.IntegerField(_("Room Capacity"))
    is_available = models.BooleanField(default=True)

    # add more fields as required

    def __str__(self):
        return f"{self.hotel.name} - {self.room_number}"


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    guest_name = models.CharField(_("Guest Name"), max_length=100)
    guest_email = models.EmailField(_("Guest Email"), max_length=254)
    guest_nationality = models.CharField(_("Guest Nationality"), max_length=2, choices=Hotel.nationality_choices)
    check_in_date = models.DateField(_("Check-in Date"))
    check_out_date = models.DateField(_("Check-out Date"))

    def __str__(self):
        return f"{self.guest_name} - {self.room}"
