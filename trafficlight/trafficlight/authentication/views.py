from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.html import format_html
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.
from trafficlight.email_credentials import EMAIL_HOST_USER
import uuid
from trafficlight.ocr.models import Driver,Incidence



@login_required
def DriverLoginView(request):
    """Sign Up view"""
    driver_id = Driver.objects.filter(driverid = request.user)[0]
    print(driver_id.mobile)
    return render(request,"my_payment_template.html",{"driver_id":driver_id})
  

def PaymentConfirmedView(request):
    payment_status = request.GET['status']
    transaction_id = request.GET['transaction_id']
    print(payment_status)
    if payment_status =='successful':
        driver =  Driver.objects.filter(driverid = request.user)[0]
        update_incidence = Incidence.objects.filter(driver = driver)[0]
        update_incidence.offence_payment = True
        update_incidence.save()
        logout(request)
        return HttpResponse("Thank you")
    return HttpResponse("Failed")

def SignInDriverIDlView(request):
    invalid_id = False
    if request.method == "POST":
        driver_id = request.POST.get('carNumber')
        try:
             
            user = User.objects.get_by_natural_key(username=driver_id)
            
            if (user is not None) and user.is_active:
                
                if not user.is_staff:
                    
                    user_password = uuid.uuid4().hex.upper()[0:6]
                    user.set_password(user_password)
                     
                    user.save()
                    
                    SendEmailSigninTemplate(user.first_name, user.email, user_password)
                     
                    return HttpResponseRedirect(reverse('driver:login_password',kwargs={"carNumber":user.username}))
                else:
                    return HttpResponseRedirect(reverse('admin_login_password',kwargs={"username":user.username}))
        except Exception:
            print("Not sent")
            raise Exception
            invalid_id = True
    return render(request, 'authentication/login.html', {"invalidID": invalid_id})


def SignInPasswordlView(request, carNumber):
    wrong_password_msg = False
    if request.method == "POST":

        password = request.POST.get('password')
        user = User.objects.get_by_natural_key(username=carNumber)
        
        if user is None:
            return HttpResponseRedirect(reverse('driver:login_password'))

        user = authenticate(username=user.username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            #return render(request,"my_payment_template.html",{"driver_id":driver_id})
            return HttpResponseRedirect(reverse('driver:payment'))
        wrong_password_msg = True
    return render(request, 'authentication/password.html', {"carNumber":carNumber, "wrongPassword": wrong_password_msg})


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('driver:login_driver_id'))


def SendEmailSigninTemplate(username, email, password):
    subject = "Red Light Crossing Fine"
    message = "Dear {username}\nYour login password is {password}".format(username=username, password=password)
    print("About to send mail")
    send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=[email])
