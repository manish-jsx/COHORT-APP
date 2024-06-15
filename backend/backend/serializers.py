from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from dj_rest_auth.serializers import LoginSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

class CustomRegisterSerializer(serializers.ModelSerializer):  
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:  
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 since it's not needed in the User model
        validated_data['password'] = make_password(validated_data.get('password'))
        user = User.objects.create(**validated_data)
        return user

    def save(self, request):
        user = super().save(request)
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def authenticate(self, **kwargs):
        return authenticate(self.context["request"], **kwargs)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = self.authenticate(username=username, password=password)

        if not user:
            raise ValidationError(
                "Invalid login credentials.",
                code="invalid_credentials",
            )

        attrs["user"] = user
        return attrs

class EmailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']  # Include only the fields you need for emails
