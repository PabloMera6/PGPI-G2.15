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
            'email': 'test@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, '/', target_status_code=200)

        self.assertTrue(response.wsgi_request.user.is_authenticated)

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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_profile_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'full_name': 'Updated Name',
            'phone': '987654321',
            'address': 'Updated Address',
            'email': 'updated@example.com',
        }
        response = self.client.post(self.profile_url, data, follow=True)
        self.assertRedirects(response, '/')

        # Recargar el objeto desde la base de datos para obtener los cambios
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, data['full_name'])
        self.assertEqual(self.user.phone, data['phone'])
        self.assertEqual(self.user.address, data['address'])
        self.assertEqual(self.user.email, data['email'])

    def test_update_profile_unauthenticated_user(self):
        data = {
            'full_name': 'Updated Name',
            'phone': '987654321',
            'address': 'Updated Address',
            'email': 'updated@example.com',
        }
        response = self.client.post(self.profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_profile_duplicate_email(self):
        self.client.force_authenticate(user=self.user)
        other_user = UserProfile.objects.create_user(email='other@example.com', password='otherpassword')
        data = {
            'full_name': 'Updated Name',
            'phone': '987654321',
            'address': 'Updated Address',
            'email': other_user.email,  # Intentar actualizar con un correo electrónico ya existente
        }
        response = self.client.post(self.profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'El nuevo correo electrónico ya está en uso.')