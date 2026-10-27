from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.doctors.models import Doctor

User = get_user_model()


class DoctorAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='admin@healthcare.com',
            password='Password123!',
            name='Hospital Admin'
        )

        self.doctor_data = {
            'name': 'Gregory House',
            'specialization': 'Diagnostic Medicine',
            'phone': '+1-555-0321',
            'email': 'house@princetonplainsboro.com',
            'years_of_experience': 20,
        }

        self.list_create_url = reverse('doctor-list-create')

    def test_create_doctor_unauthenticated_fails(self):
        """Unauthenticated user cannot create a doctor."""
        response = self.client.post(self.list_create_url, self.doctor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_doctor_authenticated(self):
        """POST /api/doctors/ - Add a new doctor (Authenticated users only)."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_create_url, self.doctor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], self.doctor_data['name'])
        self.assertEqual(response.data['data']['specialization'], self.doctor_data['specialization'])

        # Check DB
        self.assertTrue(Doctor.objects.filter(email=self.doctor_data['email']).exists())

    def test_get_all_doctors(self):
        """GET /api/doctors/ - Retrieve all doctors."""
        Doctor.objects.create(**self.doctor_data)
        Doctor.objects.create(
            name='James Wilson',
            specialization='Oncology',
            phone='+1-555-0322',
            email='wilson@princetonplainsboro.com',
            years_of_experience=18
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_doctor_detail(self):
        """GET /api/doctors/<id>/ - Get details of a specific doctor."""
        doctor = Doctor.objects.create(**self.doctor_data)
        detail_url = reverse('doctor-detail', kwargs={'pk': doctor.id})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], doctor.id)
        self.assertEqual(response.data['email'], doctor.email)

    def test_put_update_doctor(self):
        """PUT /api/doctors/<id>/ - Update doctor details."""
        doctor = Doctor.objects.create(**self.doctor_data)
        detail_url = reverse('doctor-detail', kwargs={'pk': doctor.id})

        updated_data = self.doctor_data.copy()
        updated_data['years_of_experience'] = 22
        updated_data['specialization'] = 'Infectious Diseases & Nephrology'

        self.client.force_authenticate(user=self.user)
        response = self.client.put(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['years_of_experience'], 22)
        self.assertEqual(response.data['specialization'], 'Infectious Diseases & Nephrology')

        doctor.refresh_from_db()
        self.assertEqual(doctor.years_of_experience, 22)

    def test_delete_doctor(self):
        """DELETE /api/doctors/<id>/ - Delete a doctor record."""
        doctor = Doctor.objects.create(**self.doctor_data)
        detail_url = reverse('doctor-detail', kwargs={'pk': doctor.id})

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(id=doctor.id).exists())

    def test_duplicate_doctor_email_rejected(self):
        """Test creating doctor with duplicate email fails."""
        Doctor.objects.create(**self.doctor_data)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_create_url, self.doctor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
