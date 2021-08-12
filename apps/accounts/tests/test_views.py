from rest_framework import status
from rest_framework.test import APITestCase
from django.shortcuts import reverse
from accounts.models import CustomUser, UserVerification

# Create your tests here.


class AccountsTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="john", email="john@gmail.com", password='s3r3n1ty',)

    def test_signup(self):
        """Tests that a user can signup"""
        signupData = {'username': "john1", 'email': "john1@gmail.com", 'password1': 's3r3n1ty',
                      'password2': 's3r3n1ty', 'first_name': 'john', 'last_name': "doe",
                      'phone_number': '08167467782', 'address': '2, Cole Street Collins Road, Ikeja, Lagos'}
        url = reverse('accounts:rest_register')
        registerResponse = self.client.post(url, signupData, format='json')

        self.assertEqual(registerResponse.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh_token', registerResponse.data)
        self.assertIn('access_token', registerResponse.data)

    def test_login(self):
        """Tests that a user can login"""
        data = {'email': "john@gmail.com", 'password': 's3r3n1ty'}
        url = reverse('accounts:rest_login')
        loginResponse = self.client.post(url, data, format='json')

        self.assertEqual(loginResponse.status_code, status.HTTP_200_OK)
        self.assertIn('refresh_token', loginResponse.data)
        self.assertIn('access_token', loginResponse.data)

    def test_new_wallet_is_created(self):
        """Tests that a wallet is created after a user signup"""
        john = CustomUser.objects.get(username="john")
        self.assertTrue(john.wallet)

    def test_user_verification(self):
        """Tests that a user is verified after adding a userverification object"""
        UserVerification.objects.create(
            user=self.user, NIN='123', BVN='123', upload_id='ID', id_type='ID', bank_name='Standard Bank',
            account_number='3223092', account_name='bnk name')

        self.assertTrue(self.user.is_verified)

    def test_user_not_verified(self):
        """Tests that a user is not verified before adding a userverification object"""
        self.assertFalse(self.user.is_verified)
