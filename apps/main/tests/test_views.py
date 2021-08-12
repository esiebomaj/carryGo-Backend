import datetime

from accounts.models import CustomUser
from django.shortcuts import reverse
from main.models import Package, Wallet
from rest_framework import status
from rest_framework.test import APITestCase


class PackageTestCase(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="john", email="john@gmail.com", password='s3r3n1ty',)
        self.user = CustomUser.objects.create_user(
            username="john1", email="john1@gmail.com", password='s3r3n1ty',)
        self.client.login(username='john1@gmail.com', password='s3r3n1ty')

    def test_package_create(self):
        """Test that a package can be created successfully"""
        url = reverse("core:packages-list")
        packageData = {
            'name': 'Hp Pavillion Laptop',
            'price': 10000,
            'origin': 'Lagos',
            'destination': 'Abuja',
            'owner': self.user.id,
            'carrier': self.user1.id
        }
        response = self.client.post(url, packageData, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Package.objects.all()), 1)
        # test that security pin was properlly generated
        self.assertEqual(len(Package.objects.first().security_code), 5)


class WalletTestCase(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="john", email="john@gmail.com", password='s3r3n1ty',)
        self.user = CustomUser.objects.create_user(
            username="john1", email="john1@gmail.com", password='s3r3n1ty',)
        self.client.login(username='john1@gmail.com', password='s3r3n1ty')
        self.user.wallet.deposit(4000)

    def test_deposit(self):
        """Test that a user can make deposit"""
        url = reverse("core:deposit", kwargs={"pk": 2, "amount": "2000"})
        response = self.client.post(url, format='json')
        wallet = Wallet.objects.get(pk=2)

        self.assertEqual(response.data["message"], 'deposit successfull')
        self.assertEqual(wallet.current_balance, 6000.0)

    def test_withdraw_insufficient_balance(self):
        """Test that a user can't withdraw with an insufficient balance"""
        url = reverse("core:withdraw", kwargs={"pk": 2, "amount": "8000"})
        response = self.client.post(url, format='json')
        wallet = Wallet.objects.get(pk=2)

        self.assertEqual(response.data["message"], 'insufficient balance')
        self.assertEqual(wallet.current_balance, 4000.0)

    def test_withdraw(self):
        """Test that a user can withdraw with a sufficient balance"""
        url = reverse("core:withdraw", kwargs={"pk": 2, "amount": "2000"})
        response = self.client.post(url, format='json')
        wallet = Wallet.objects.get(pk=2)

        self.assertEqual(response.data["message"], 'withdraw successfull')
        self.assertEqual(wallet.current_balance, 2000.0)

    def test_transfer(self):
        """Test that transfer can be made from one user to another"""
        url = reverse("core:transfer", kwargs={"amount": "2000"})
        data = {"owner": self.user.id, "carrier": self.user1.id}
        response = self.client.post(url, data, format='json')

        wallet = Wallet.objects.get(pk=2)

        self.assertEqual(response.data["message"], 'transer successfull')
        self.assertEqual(wallet.current_balance, 2000.0)
