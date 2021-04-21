from django.shortcuts import render,HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from trafficlight.ocr.models import  UserProfile,Driver,licensePlate,Incidence
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator

@login_required
def PaymentView(request):
    return render(request,"my_payment_template.html")



@login_required
def LoginView(request):
    return render(request, 'home.html')

def TryView(request):
    return render(request, 'daniel_try.html')

#List all incidence sorted based on date added
@login_required
def IncidenceList(request):
    incidence = Incidence.objects.all()
    paginate_by = 10
    return render(request, 'home.html', {"incidence":incidence})

#List all drivers 
@login_required
def DriverList(request):
    drivers = Driver.objects.all()
    return render(request, 'vehicle_owners.html', {"drivers":drivers})

#View and edit driver profile information
@login_required
def EditDriverProfile(request,driverID):
    driver = Driver.objects.filter(id=driverID)[0]
    drivers = Driver.objects.all()
    if request.method == "POST": 
        try:
            driver.title = request.POST.get('title')
            driver.first_name = request.POST.get('first_name')
            driver.last_name = request.POST.get('last_name')
            driver.gender = request.POST.get('gender')
            driver.email = request.POST.get('email')
            driver.mobile = request.POST.get('mobile')
            driver.address = request.POST.get('address')
            driver.vehicleType = request.POST.get('vtype')
            driver.licensePlate = request.POST.get('licensePlate')
            driver.save()
            print(request.POST.get('gender'))
            return render(request, 'vehicle_owners.html', {"drivers":drivers})
        except Exception :
            raise Exception

            return render(request,"Something went wrong")
        
    else:
        return render(request, 'edit_profile.html',{"driver_info":driver})

#Update Driver's profile

def UpdateDriverProfile(request,driverID):
    driver = Driver.objects.filter(id=driverID)[0]
    drivers = Driver.objects.all()
    if request.method == "POST": 
        try:
            driver.first_name = request.POST.get('first_name')
            driver.last_name = request.POST.get('last_name')
            driver.gender = request.POST.get('gender')
            driver.email = request.POST.get('email')
            driver.mobile = request.POST.get('mobile')
            driver.address = request.POST.get('address')
            driver.vehicleType = request.POST.get('vtype')
            driver.licensePlate = request.POST.get('licensePlate')
            driver.save()
            
            return render(request, 'vehicle_owners.html', {"drivers":drivers})
        except Exception :
            raise Exception

            return render(request,"Something went wrong")
       


@login_required
def AddDriverCreate(request):
    if request.method == "POST": 

        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            address = request.POST.get('address')
            vehicleType = request.POST.get('vtype')
            licensep = request.POST.get('licensePlate')

            _, created = User.objects.update_or_create(
                username = str(licensep),
                first_name = first_name,
                last_name = last_name,
                email = email,
                
            )

            
            _, created = Driver.objects.update_or_create(
                driverid = _, 
                mobile = mobile,
                address = address,
                vehicleType = vehicleType,
                licensePlate = licensep,
                gender = gender
            )
            print(_)
            _, created = licensePlate.objects.update_or_create(
                driver = _, 
                licensePlate = licensep,
                crime_case_count = 0
            )


            return HttpResponseRedirect(reverse('ocrAdmin:drivers_list'))
        except Exception :
            raise Exception

            return render(request,"Something went wrong")

    else:
        return render(request,"create_profile.html")