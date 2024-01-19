from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("apps", views.ApplicationViewSet, basename='applications')
router.register(
    "unpurchased/apps", views.UnpurchasedApplicationViewSet, basename='unpurchased-applications')
router.register(
    "purchased/apps", views.PurchasedApplicationViewSet, basename="purchased-applications")

urlpatterns = [
    path("purchase/", views.PurchaseAPIView.as_view(), name='purchase')
]

urlpatterns += router.urls
