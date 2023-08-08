from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


User = get_user_model()
class Customer(models.Model):
    full_name= models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # booking_set

# can_be_customer = Permission.objects.create(
#     codename='can_be_customer',
#     name='Can be Customer'
# )