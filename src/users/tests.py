from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import UserProfile
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

        response = self.client.post(reverse('register'), data, follow=True) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(response, reverse('initial'), target_status_code=200)

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

        response = self.client.post(reverse('register'), data, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(response, reverse('register'), target_status_code=200)
        self.assertContains(response, 'Correo electrónico y contraseña son obligatorios.')

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

        response = self.client.post(reverse('register'), data, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(response, reverse('register'), target_status_code=200)
        self.assertContains(response, f'El correo electrónico {data["email"]} ya está registrado.')



class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')

    def test_get_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_successful_login(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'full_name': 'Test User',
            'phone': '123456789',
            'address': 'Test Address',
        }
        UserProfile.objects.create_user(**user_data)

        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, '/', target_status_code=200)

        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_missing_email_or_password(self):
        data = {
            'email': '',
            'password': 'testpassword',
        }

        response = self.client.post(reverse('login'), data, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(response, reverse('login'), target_status_code=200)
        self.assertContains(response, 'Correo electrónico y contraseña son obligatorios.')

    def test_nonexistent_email(self):
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(reverse('login'), data, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(response, reverse('login'), target_status_code=200)
        self.assertContains(response, f'El correo electrónico {data["email"]} no está registrado.')
    
    def test_incorrect_password(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'full_name': 'Test User',
            'phone': '123456789',
            'address': 'Test Address',
        }
        UserProfile.objects.create_user(**user_data)

        data = {
            'email': 'test@example.com',
            'password': 'incorrectpassword',
        }

        response = self.client.post(reverse('login'), data, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(response, reverse('login'), target_status_code=200)
        self.assertContains(response, 'Contraseña incorrecta.')

class UserProfileViewTest(TestCase):
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
        self.profile_url = reverse('profile')

    def test_get_profile_view_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_get_profile_view_unauthenticated_user(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_update_profile_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'full_name': 'Updated Name',
            'phone': '987654321',
            'address': 'Updated Address',
        }
        response = self.client.post(self.profile_url, data, follow=True)
        self.assertRedirects(response, '/')

        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, data['full_name'])
        self.assertEqual(self.user.phone, data['phone'])
        self.assertEqual(self.user.address, data['address'])

    def test_update_profile_unauthenticated_user(self):
        data = {
            'full_name': 'Updated Name',
            'phone': '987654321',
            'address': 'Updated Address',
            'email': 'updated@example.com',
        }
        response = self.client.post(self.profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
