from django.contrib.auth import get_user_model
from django.db import models



User = get_user_model()
class Customer(models.Model):
    full_name= models.CharField(max_length=255)
    # email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # booking_set

