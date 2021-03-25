app_name =  "ocr"

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from trafficlight.ocr import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'Drivers', views.SingleDriverInfoAPIView, basename="Drivers")
 

urlpatterns = [
    # view all accounts. Admin only
    path('account/all-users', views.UserList.as_view()),
    # register
    path('account/register/', views.UserCreate.as_view()),
    # login
    path('account/login/', views.UserLoginCreate.as_view()),
    # logged in?
    path('account/logged-in/', views.logged_in),
    # logout
    path('account/logout/', views.logout_user),
    # retrieve auth.user and profile of user
    path('account/', views.UserAuthProfileList.as_view()),
    # update user profile
    path('account/profile/details/<int:pk>/', views.UserProfilesUpdate.as_view()),
    # update auth.user properties without password
    path('account/profile/<int:pk>/', views.UserUpdateUpdate.as_view()),
    # change password of an authenticated user
    path('account/change-password/<int:pk>/', views.ChangePasswordUpdate.as_view()),
    #view all drivers in database
    path('drivers/', views.DriverList.as_view()),
    path('SingleDriverInfo/<str:phone>/',views.SingleDriverInfoAPIView.as_view(), name ="driverdetail"),
    path('crime/',views.CrimeDataCreateAPIView.as_view(), name ="crime"),

]
urlpatterns = format_suffix_patterns(urlpatterns)
