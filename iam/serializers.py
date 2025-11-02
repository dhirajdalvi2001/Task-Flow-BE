from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"password":"Invalid username or password"})

        if not user.check_password(attrs['password']):
            raise serializers.ValidationError({"password":"Invalid username or password"})
        if not user.is_active:
            raise serializers.ValidationError({"password":"User is not active"})
        
       
        return {
            "access": self.get_access_token(user),
            "refresh": self.get_refresh_token(user),
            "user": self.get_user(user),
        }

    def get_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def get_refresh_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)
    
    def get_user(self, user):
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            "first_name": getattr(user, "first_name", ""),
            "last_name": getattr(user, "last_name", ""),
            "phone_number": getattr(user, "phone_number", None),
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        }
        
    # ensure serializer.data returns the token dict (the dict returned from validate)
    def to_representation(self, instance):
        # instance will be the dict returned by validate()
        return instance


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            refresh = RefreshToken(attrs['refresh'])
            return {
                'access': str(refresh.access_token),
            }
        except Exception as e:
            raise serializers.ValidationError({"refresh":"Invalid refresh token"})

    def to_representation(self, instance):
        return instance


class SignUpSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=True)
    is_active = serializers.BooleanField(required=False, default=True)
    is_staff = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'is_superuser', 'password']
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email":"Email already exists"})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username":"Username already exists"})
        return attrs

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError({"phone_number":"Phone number must be a number"})
        if len(value) != 10:
            raise serializers.ValidationError({"phone_number":"Phone number must be 10 digits"})
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def get_user(self, user):
        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        }
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'is_superuser']

