from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import UserProfile

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_successful_registration(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'full_name': 'Test User',
            'phone': '123456789',
            'address': 'Test Address',
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = UserProfile.objects.get(email=data['email'])
        self.assertIsNotNone(user)
        self.assertEqual(user.full_name, data['full_name'])
        self.assertEqual(user.phone, data['phone'])
        self.assertEqual(user.address, data['address'])

    def test_missing_email_or_password(self):
        data = {
            'email': '',
            'password': 'testpassword',
            'full_name': 'Test User',
            'phone': '123456789',
            'address': 'Test Address',
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_existing_email(self):
        UserProfile.objects.create_user(
            email='existing@example.com',
            password='existingpassword'
        )

        data = {
            'email': 'existing@example.com',
            'password': 'testpassword',
            'full_name': 'Test User',
            'phone': '123456789',
            'address': 'Test Address',
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'El correo electrónico ya está en uso.')

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'full_name': 'Test User',
            'phone': '123456789',
            'address': 'Test Address',
        }
        self.user = UserProfile.objects.create_user(**self.user_data)
        self.login_url = reverse('login')

    def test_get_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_successful_login(self):
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_pk', response.data)
        self.assertEqual(response.data['user_pk'], self.user.pk)

    def test_missing_email_or_password(self):
        data = {
            'email': '',
            'password': 'testpassword',
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_nonexistent_email(self):
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'El correo electrónico no existe.')

    def test_incorrect_password(self):
        data = {
            'email': self.user_data['email'],
            'password': 'incorrectpassword',
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Contraseña incorrecta.')
