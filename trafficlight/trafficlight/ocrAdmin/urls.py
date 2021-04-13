app_name =  "ocrAdmin"
from django.conf.urls import include,url
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    #authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html',redirect_field_name="home.html"),name='user_login2'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html',redirect_field_name="home.html"),name='user_login1'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("", IncidenceList, name="incidence"),
    path("incidence/", IncidenceList, name="incidence"),
    path("drivers/", DriverList, name="drivers_list"),
    path("drivers/edit/<int:driverID>/", EditDriverProfile, name="edit_info"),
    path("drivers/update/<int:driverID>/", UpdateDriverProfile , name="update_info"),
    # path("student/", views.SignInStudentIDlView, name="login_student_id"),
    # path("country/", views.StudentCountry, name="country_info"),
    # path("password/<int:studentID>/", views.SignInPasswordlView, name="login_password"),
    # path("password/admin/<slug:username>/", views.AdminSignInPasswordlView, name="admin_login_password"),
    # path("logout/", views.Logout, name="logout"),
]
