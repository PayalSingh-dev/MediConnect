from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.refresh_url = reverse('auth-token-refresh')

        self.user_data = {
            'name': 'Dr. Alice Smith',
            'email': 'alice@healthcare.com',
            'password': 'SecurePassword123!',
        }

    def test_register_user_success(self):
        """Test registering a new user with name, email, and password."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get('success'))
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        self.assertEqual(response.data['user']['name'], self.user_data['name'])

        # Check user exists in database
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

    def test_register_duplicate_email(self):
        """Test that registering with duplicate email returns 400 Bad Request."""
        User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            name=self.user_data['name']
        )
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_fields(self):
        """Test registration validation with missing required fields."""
        response = self.client.post(self.register_url, {'email': 'test@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_too_short(self):
        """Test registration with password shorter than minimum length."""
        bad_data = {
            'name': 'Bob',
            'email': 'bob@example.com',
            'password': '123'
        }
        response = self.client.post(self.register_url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """Test logging in an existing user returns JWT tokens."""
        User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            name=self.user_data['name']
        )
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('success'))
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertEqual(response.data['user']['email'], self.user_data['email'])

    def test_login_invalid_password(self):
        """Test logging in with incorrect password returns 400."""
        User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            name=self.user_data['name']
        )
        login_data = {
            'email': self.user_data['email'],
            'password': 'WrongPassword999!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        """Test logging in with email that does not exist returns 400."""
        login_data = {
            'email': 'ghost@healthcare.com',
            'password': 'SomePassword123!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_refresh(self):
        """Test refreshing access token using refresh token."""
        user = User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            name=self.user_data['name']
        )
        login_resp = self.client.post(
            self.login_url,
            {'email': self.user_data['email'], 'password': self.user_data['password']},
            format='json'
        )
        refresh_token = login_resp.data['tokens']['refresh']

        refresh_resp = self.client.post(self.refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(refresh_resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_resp.data)
