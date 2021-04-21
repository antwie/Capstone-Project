from django.contrib.auth.models import User 
from rest_framework import generics
from rest_framework.response import Response
from .models import UserProfile,Driver,licensePlate,Incidence
from .serializers import UserSerializer, UserBasicInfoSerializer, UserLoginSerializer, UserProfileSerializer \
    , UserUpdateSerializer, ChangePasswordSerializer, DriverUpdateSerializer, PostCrimeDatSerializer, GetCrimeDatSerializer \
        ,DriverListSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.decorators import api_view
#from ApplicationPortal.AdminPortal.serializers import MakeStaffSerializer
from rest_framework.authtoken.models import Token


class CrimeDataCreateAPIView(generics.CreateAPIView):
    '''
    POST car number plate details from raspberry pi
    '''
    queryset = Incidence.objects.all()
    serializer_class = PostCrimeDatSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)    




class DriverList(generics.ListAPIView):
    '''
    Display all drivers in the system
    '''
    queryset = Driver.objects.all()
    serializer_class =  DriverListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )


class IncidenceList(generics.ListAPIView):
    '''
    Display all Indicence in the database
    '''
    queryset = Incidence.objects.all()
    serializer_class = GetCrimeDatSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    


class SingleDriverInfoAPIView(generics.ListAPIView):
    '''
    Display details about a driver given their car number plate
    '''
    queryset = Driver.objects.all()
    serializer_class = DriverUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    #lookup_url_kwarg = "phone"

    def get_queryset(self):
        """
        This view should return a.
        """
        # does a get based on the user id
        uid = self.kwargs['phone']
        print(uid)
        
        
        return self.queryset.filter(mobile=uid)
        


@api_view(['POST'])
def logout_user(request):
    if request.method == 'POST':
        request.auth.delete()
        return Response({"success":True})


@api_view(['POST'])
def logged_in(request):
    if request.method == 'POST':

        return Response(request.user.is_authenticated)



class UserList(generics.ListAPIView):

    '''
    displaying list a users- Admin only
    '''
    queryset = User.objects.all()
    #serializer_class = MakeStaffSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser, )



class UserCreate(generics.CreateAPIView):
    '''
    creating a new user
    '''
    queryset = User.objects.all()
    serializer_class = UserBasicInfoSerializer
    permission_classes = (AllowAny, )
    authentication_classes = (BasicAuthentication, )


    def create(self, request, *args, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        self.get_queryset()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'id':user.id, 'first_name':user.first_name, 'token':token.key})


    def perform_create(self, serializer):
        return serializer.save()


class UserLoginCreate(generics.CreateAPIView):
    '''
    for user login
    '''
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )
    authentication_classes = (BasicAuthentication, )


    def create(self, request, *args, **kwargs):
        self.get_queryset()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        if user is None:
            return Response(serializer.data)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'id':user.id, 'first_name':user.first_name, 'token':token.key})

    def perform_create(self, serializer):
        return serializer.save()


class UserAuthProfileList(generics.ListAPIView):
    '''
    user to retrieve their user status and profile
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return User.objects.filter(id=self.request.user.id)



class UserUpdateUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return User.objects.filter(id=self.request.user.id)

class UserProfilesUpdate(generics.UpdateAPIView):
    '''
    Retrieve and update user profile.
    '''
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return UserProfile.objects.filter(user=self.request.user.id)


class ChangePasswordUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"password_changed":True})