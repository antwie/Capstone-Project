from django.db import models
from django.contrib.auth.models import User
import datetime  
from django.utils import timezone
from django.conf import settings
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=5, default="Mr.")
    gender = models.CharField(max_length=20, default="male")
    dob = models.DateField(default=timezone.now)
    address = models.CharField(max_length=400, blank=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    #photo = models.ImageField(upload_to='uploads/', blank=True)


class licensePlate(models.Model):
    car_number = models.CharField(max_length=50)
    crime_case_count = models.IntegerField()
    crime_alert = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return str(self.car_number)

    class Meta:
        db_table = "licensePlate"

class Driver(models.Model):
    title = models.CharField(max_length=5, default="Mr.")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=20, default="male")
    address = models.CharField(max_length=400, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=50, blank=True)
    licensePlate = models.ForeignKey(licensePlate, on_delete=models.CASCADE)
    date_created  = models.DateField(default = timezone.now)
    

    def __str__(self):
        return str(self.first_name) + str(" ") + str(self.last_name)

    class Meta:
        db_table = "driver"



class Incedence(models.Model):
    traffic_light_no = models.CharField(max_length=50, blank=True)
    licensePlate = models.CharField(max_length=50, blank=False)
    vehicleType = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    offence = models.CharField(max_length=50, blank=True)
    date_created = models.DateField(default = timezone.now)
    accuracy_score = models.CharField(max_length=10, blank=True)
    

    def __str__(self):
        return str(self.offence) 

     