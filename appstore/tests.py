from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import UserWallet
from .models import (
    Application,
    PurchasedApplication
)

User = get_user_model()


class TestApplicationAPIs(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(username="user", is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.application = Application.objects.create(
            owner=self.user, title='formaloo', description='formaloo application',
            icon='https://www.formaloo.com/en/', link='https://www.formaloo.com/en/',
            price=100.00
        )
    
    def test_list_application_created_by_specific_user(self):
        url = reverse('applications-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Application.objects.count())

    def test_create_new_application_success_case(self):
        url = reverse('applications-list')
        data = {
            'title': 'Formaloo',
            'description': 'Formaloo application',
            'icon': 'https://www.formaloo.com/en/',
            'link': 'https://www.formaloo.com/en/',
            'price': 100.00
        }
        application_count_before = Application.objects.count()
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(application_count_before + 1, Application.objects.count())

    def test_create_new_application_failure_case(self):
        url = reverse('applications-list')

        application_count_before = Application.objects.count()
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(application_count_before, Application.objects.count())

    def test_update_existing_application_success_case(self):
        url = reverse('applications-detail', kwargs={'pk': self.application.id})

        data = {
            'price': 2000.00
        }

        response = self.client.patch(url, data=data)
        self.application.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.application.price, data['price'])

    def test_update_application_does_not_exist_failure_case(self):
        url = reverse('applications-detail', kwargs={'pk': self.application.id + 10000})
        data = {
            'price': 2000.00
        }
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_existing_application_success_case(self):
        url = reverse('applications-detail', kwargs={'pk': self.application.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_application_does_not_exist_failure_case(self):
        url = reverse('applications-detail', kwargs={'pk': self.application.id + 1000})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestPurchasedApplicationAPIs(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.owner = User.objects.create(username='owner')
        self.user = User.objects.create(username="user")
        UserWallet.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.application = Application.objects.create(
            owner=self.owner, title='formaloo', description='formaloo application',
            icon='https://www.formaloo.com/en/', link='https://www.formaloo.com/en/',
            price=100.00
        )
        self.application_2 = Application.objects.create(
            owner=self.owner, title='formaloo', description='formaloo application',
            icon='https://www.formaloo.com/en/', link='https://www.formaloo.com/en/',
            price=1000.00
        )

        self.purchased_application = PurchasedApplication.objects.create(
            user=self.user, app=self.application
        )

    def test_purchase_application_success_case(self):
        url = reverse('purchase')

        data = {
            "app_id": self.application.id
        }

        response = self.client.post(url, data=data)
        self.user.userwallet.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], 'Purchased')
        self.assertEqual(self.user.userwallet.credit, 0)

    def test_purchase_application_insufficenit_balance_case(self):
        url = reverse('purchase')

        data = {
            "app_id": self.application_2.id
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['msg'], 'Insufficient balance')

    def test_list_purchased_application(self):
        url = reverse('purchased-applications-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), PurchasedApplication.objects.filter(user=self.user).count())

    def test_list_unpurchased_application(self):
        url = reverse('unpurchased-applications-list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Application.objects.exclude(owner=self.user).count())
