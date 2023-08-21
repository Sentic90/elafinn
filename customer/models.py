from django.contrib.auth import get_user_model
from django.db import models



User = get_user_model()

GENDER = (
    ('male', 'ذكر'),
    ('female', 'انثى')
)
class Customer(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='الاسم الاول')
    last_name = models.CharField(max_length=255, verbose_name='اسم العائلة ')
    email = models.EmailField(max_length=255, verbose_name='البريد الالكتروني')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='رقم الهاتف')
    gender = models.CharField(choices=GENDER, max_length=10, verbose_name='الجنس')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='العنوان')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # booking_set

    def __str__(self) -> str:
        return self.first_name + self.last_name
