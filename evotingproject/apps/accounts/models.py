# from django.conf import settings


from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None # Here
    email = models.EmailField('email address', unique=True) # Here
    User_Img = models.ImageField(upload_to='images/')
    course = models.CharField(max_length=100)
    voted = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email' # Here
    REQUIRED_FIELDS = []

    objects = CustomUserManager() # Here

    class Meta:
        verbose_name = "custom user"
        verbose_name_plural = "custom users"

class UserProfile(models.Model):
     
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    User_Img = models.ImageField(upload_to='images/',null=True)
    name = models.CharField(max_length=200)
    stud_id = models.CharField(max_length=200)
    course_year_and_section = models.CharField(max_length=200)