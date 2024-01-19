from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from .serializers import UserRegisterationSerializer


class UserSignupViewSet(GenericViewSet, CreateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterationSerializer
