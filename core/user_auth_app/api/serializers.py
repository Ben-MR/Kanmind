from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']

class RegistrationsSerializer (serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only = True)
    fullname = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only' : True
            }
        }
    
    def save(self):
        pw = self.validated_data ['password']
        repeated_pw = self.validated_data ['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'password dont match'})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['email'])
        account.first_name = self.validated_data['fullname']
        account.set_password(pw)
        account.save()
        return account
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
