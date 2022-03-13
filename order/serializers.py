from django.db.models import fields
from rest_framework import serializers
from .models import Post, OrderProcessModel

from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import OrderProcessModel

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title', 'description'
            )

class OrderProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProcessModel
        fields = (
        'email', 'name', 'order_id', 'order_date', 'product_url', 'product_title'
        )
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = { 'password': {'write_only':True} }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(seld, data):
            user = authenticate(**data)

            if user and user.is_active:
                    return user
            raise serializers.ValidationError("Incorrect Credentials")


class OrderProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProcessModel
        fields = '__all__'