from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import AppUser


class UserRegisterSerilaizer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = AppUser
        fields = [
            'first_name', 'last_name', 'email', 
            'password', 'confirm_password',
        ]

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError(
                'First name must contain only alphabets.')
        if len(value) > 15:
            raise serializers.ValidationError(
                "First name must be at most 15 characters.")
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError(
                "Last name must contain only alphabets.")
        if len(value) > 15:
            raise serializers.ValidationError(
                "Last name must be at most 15 characters.")
        return value

    def validate_email(self, value):
        user = AppUser.objects.get(
            email=value)
        if user:
            raise serializers.ValidationError("Email Already Exists")
        return value

    def validate_confirm_password(self, value):
        password = self.initial_data.get('password')
        if password and value != password:
            raise serializers.ValidationError("Password not match")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
       
        user = AppUser(**validated_data)

        user.set_password(password)
        user.is_email_verify = False 
        user.save()
        data = {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_email_verified": user.is_email_verify,
        }
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = AppUser.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({'email': 'Email not exists'})
        if not user.check_password(password):
            raise serializers.ValidationError({
                'user_id': str(user.id),
                'is_email_verify': user.is_email_verify,
                'password': ['Please Enter the Correct Password.']
            })

    

        if not user.check_password(password):
            raise serializers.ValidationError(
                {'password': 'Password is Wrong'})

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.is_active = True
        user.is_email_verify = True
        refresh = RefreshToken.for_user(user)
        user.save()
        return {
            "user_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_email_verify": user.is_email_verify,
            "is_active": user.is_active,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
