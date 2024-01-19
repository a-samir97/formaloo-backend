from rest_framework import serializers
from .models import Application, PurchasedApplication


class ApplicationSerializer(serializers.ModelSerializer):
    """
        This serializer responsible for CRUD functionality for
        Application model
    """
    class Meta:
        model = Application
        exclude = ("is_verified", "owner")


class UnpurchasedApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        exclude = ("is_verified", "key", "link")


class PurchasedApplicationSerializer(serializers.ModelSerializer):
    app = ApplicationSerializer()

    class Meta:
        model = PurchasedApplication
        exclude = ('user',)
