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



class Driver(models.Model):
    driverid = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, default="male")
    address = models.CharField(max_length=400, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    licensePlate = models.CharField(max_length=50)
    vehicleType = models.CharField(max_length=50, blank=True)
    date_created  = models.DateTimeField(default = timezone.now)    

    def __str__(self):
        return str(self.driverid.first_name) + str(" ") + str(self.driverid.last_name)

    class Meta:
        db_table = "driver"

class licensePlate(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    licensePlate = models.CharField(max_length=50, blank=False)
    crime_case_count = models.IntegerField(default=0, blank=True)
    
    

    def __str__(self):
        return str(self.driver)

    class Meta:
        db_table = "licensePlate"


class Incidence(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    traffic_light_no = models.CharField(max_length=50, blank=True)
    licensePlate = models.CharField(max_length=50, blank=False)
    color = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    offence = models.CharField(max_length=50, blank=True)
    offence_payment = models.BooleanField(default=False)
    date_created = models.DateTimeField(default = timezone.now)
    accuracy_score = models.CharField(max_length=10, blank=True)
    

    def __str__(self):
        return str(self.licensePlate) 

     