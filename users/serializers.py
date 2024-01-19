from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from .models import UserWallet
User = get_user_model()


class UserRegisterationSerializer(serializers.ModelSerializer):
    """
        This serializer responsible for signup a new user to our system
    """
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    @atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        # create wallet for the registered user
        UserWallet.objects.create(user=user)

        return user

    class Meta:
        model = User
        fields = ("username", "password")
