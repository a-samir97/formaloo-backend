from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ApplicationSerializer,
    UnpurchasedApplicationSerializer,
    PurchasedApplicationSerializer
)
from .models import Application, PurchasedApplication
from users.models import UserWallet


class ApplicationViewSet(ModelViewSet):
    def get_queryset(self):
        queryset = Application.objects.filter(owner=self.request.user)
        return queryset

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UnpurchasedApplicationViewSet(GenericViewSet, ListModelMixin):
    def get_queryset(self):
        queryset = Application.objects.exclude(owner=self.request.user)
        return queryset
    serializer_class = UnpurchasedApplicationSerializer
    permission_classes = [IsAuthenticated]


class PurchasedApplicationViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    def get_queryset(self):
        queryset = PurchasedApplication.objects.filter(user=self.request.user)
        return queryset

    serializer_class = PurchasedApplicationSerializer
    permission_classes = [IsAuthenticated]


class PurchaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        app_id = request.data.get('app_id')
        app = get_object_or_404(Application, id=app_id)
        if request.user.userwallet.credit >= app.price:
            # to avoid race condition
            user_wallet = UserWallet.objects.select_for_update().filter(user=request.user).first()
            user_wallet.credit -= app.price
            user_wallet.save()
            message = {"msg": "Purchased"}
            return Response(data=message, status=status.HTTP_200_OK)
        message = {"msg": "Insufficient balance"}
        return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
