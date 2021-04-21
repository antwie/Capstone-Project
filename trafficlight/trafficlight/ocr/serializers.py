from django.contrib.auth.models import User 
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import UserProfile,Driver,licensePlate,Incidence
from django.contrib.auth import authenticate

####################################################


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name')


####################################################


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user',)


####################################################


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username','email', 'first_name', 'last_name', 'profile')

####################################################



class UserBasicInfoSerializer(serializers.ModelSerializer):
    username = serializers.EmailField()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['email'] = validated_data['username']
        try:
            # creates the user object
            user = User(**validated_data)
            # Hash the user's password.
            user.set_password(validated_data['password'])
            user.save()
            # hides the user password
            user.password = ''
            # Creates an empty user profile for user with default x'tics
            user_profile = UserProfile.objects.create(user=user)
            # saves the profile
            user_profile.save()
            return user
        except IntegrityError:
            raise ValidationError('This email has already been used')



#########################################################################

class UserLoginSerializer(serializers.ModelSerializer):
    # username = serializers.EmailField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}, 'username': {'write_only': True, 'required':False}}


    def update(self, validated_data):
        print("something")
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        
        # user exists and is activated
        if  (user is not None) and user.is_active:
            return user
        raise ValidationError('Wrong login credentials')


#########################################################################

class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=50)


    class Meta:
        model = User
        fields = ['password', 'new_password']

    def update(self, instance, validated_data):
        # gets the old and new password into variables
        password = validated_data.pop('password', None)
        new_password = validated_data.pop('new_password', None)

        # checks if the password given is correct
        is_password_correct = instance.check_password(password)
        if not is_password_correct:
            raise ValidationError("Current password is incorrect")

        # checks if the new password given is not empty and changes it
        if new_password is not None:
            instance.set_password(new_password)

        # saves to update
        instance.save()
        # returns the user object
        return instance


#########################################################################

class DriverUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['title','first_name','last_name','gender','address','mobile','email']


#########################################################################
#Post Incidence information about driver

class PostCrimeDatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidence
        
        fields = ['driver','traffic_light_no','licensePlate','color','model','offence','offence_payment','accuracy_score']
        read_only_fields = ('driver',)

    def create(self, validated_data):
        try:
            driver = Driver.objects.filter(licensePlate= validated_data['licensePlate']).first()
            
            created = Incidence.objects.create(
                driver = driver,
                traffic_light_no = validated_data['traffic_light_no'],
                licensePlate = validated_data['licensePlate'],
                color = validated_data['color'],
                model =  validated_data['model'],
                offence =  validated_data['offence'],
                offence_payment = validated_data['offence_payment'],
                accuracy_score = validated_data['accuracy_score'],
            )
            
            crime_count = licensePlate.objects.filter(driver =driver)[0]
            print(crime_count.crime_case_count)
            crime_count.crime_case_count = crime_count.crime_case_count + 1
            crime_count.save()

            return created
        except IntegrityError:
            #raise Exception
            raise ValidationError('Driver not found in our database')
            


class GetCrimeDatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidence
        
        fields = ['driver','traffic_light_no','licensePlate','vehicleType','color','model','offence','accuracy_score','offence_payment']



class DriverListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        
        fields = ['driverid','first_name','last_name','gender','mobile','email','licensePlate','vehicleType','date_created']