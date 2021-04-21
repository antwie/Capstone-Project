from django.contrib import admin
from .models import *
from rest_framework.authtoken.admin import TokenAdmin
# project imports




# Register your models here.
admin.site.register([UserProfile,Driver,Incidence,licensePlate])


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False



TokenAdmin.raw_id_fields = ['user']