from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
  email = models.EmailField(unique=True)
  is_customer = models.BooleanField(default=True)


class Notification(models.Model):
  recipient = models.ForeignKey(User, on_delete=models.CASCADE, )
  message = models.CharField(max_length=1024)
  read = models.BooleanField(default=False)
  time = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return self.message