import logging

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

LOGGER = logging.getLogger(__name__)

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")

        if not first_name:
            LOGGER.warning("First name was not specified")
            raise serializers.ValidationError("First name was not specified")
        
        if not last_name:
            LOGGER.warning("Last name was not specified")
            raise serializers.ValidationError("Last name was not specified")
        
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)

        try:
            validate_password(password=password, user=user)
        except ValidationError as error:
            LOGGER.warning("Password didn't pass validation")
            raise serializers.ValidationError(error.messages)
        
        user.set_password(password)
        user.save()

        return user
    
    def to_representation(self, instance):
        user = super().to_representation(instance)
        refresh = RefreshToken.for_user(instance)
        access = refresh.access_token

        return {
            "user": user,
            "refresh": str(refresh),
            "access": str(access),
        }
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = authenticate(email=email, password=password)
        except User.DoesNotExist:
            user = None

        if not user:
            LOGGER.warning("Invalid credentials")
            raise serializers.ValidationError("Invalid credentials")
        
        attrs["user"] = user

        return attrs
    
    def user_tokens(self):
        user = self.validated_data.get("user")
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            "refresh_token": str(refresh),
            "access_token": str(access)
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]