app_name =  "driver"
from django.conf.urls import include,url
from django.urls import path
from . import views

urlpatterns = [
    path("", views.SignInDriverIDlView, name="login_driver_id"),
    #url("country/", views.StudentCountry, name="country_info"),
    path("password/<str:carNumber>/", views.SignInPasswordlView, name="login_password"),
    #url("password/admin/<slug:username>/", views.AdminSignInPasswordlView, name="admin_login_password"),
    path("logout/", views.Logout, name="logout"),
    path("start/payment/", views.DriverLoginView, name="payment"),
    url(r'^confirm/$', views.PaymentConfirmedView, name='confirm_paymennt')
]
