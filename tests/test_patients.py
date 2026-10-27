from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.patients.models import Patient

User = get_user_model()


class PatientAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@healthcare.com',
            password='Password123!',
            name='User One'
        )
        self.user2 = User.objects.create_user(
            email='user2@healthcare.com',
            password='Password123!',
            name='User Two'
        )

        self.patient_data = {
            'name': 'John Doe',
            'age': 35,
            'gender': 'Male',
            'contact_number': '+1-555-0199',
            'email': 'johndoe@example.com',
            'address': '123 Elm Street, Cityville',
            'medical_history': 'No known allergies. Mild hypertension.'
        }

        self.list_create_url = reverse('patient-list-create')

    def test_create_patient_unauthenticated_fails(self):
        """Unauthenticated user cannot create patient."""
        response = self.client.post(self.list_create_url, self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_patient_authenticated(self):
        """POST /api/patients/ - Add a new patient (Authenticated users only)."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.list_create_url, self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], self.patient_data['name'])
        self.assertEqual(response.data['data']['created_by'], self.user1.id)

        # Check in DB
        patient = Patient.objects.get(id=response.data['data']['id'])
        self.assertEqual(patient.created_by, self.user1)

    def test_get_patients_scoped_to_authenticated_user(self):
        """GET /api/patients/ - Retrieve all patients created by the authenticated user."""
        patient1 = Patient.objects.create(created_by=self.user1, **self.patient_data)
        patient2 = Patient.objects.create(
            created_by=self.user2,
            name='Jane Smith',
            age=29,
            gender='Female',
            contact_number='+1-555-0200',
            email='janesmith@example.com'
        )

        # Authenticate as User 1
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only see patient1
        patient_ids = [p['id'] for p in response.data]
        self.assertIn(patient1.id, patient_ids)
        self.assertNotIn(patient2.id, patient_ids)

    def test_get_patient_detail(self):
        """GET /api/patients/<id>/ - Get details of a specific patient."""
        patient = Patient.objects.create(created_by=self.user1, **self.patient_data)
        detail_url = reverse('patient-detail', kwargs={'pk': patient.id})

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], patient.id)
        self.assertEqual(response.data['name'], patient.name)

    def test_put_update_patient(self):
        """PUT /api/patients/<id>/ - Update patient details."""
        patient = Patient.objects.create(created_by=self.user1, **self.patient_data)
        detail_url = reverse('patient-detail', kwargs={'pk': patient.id})

        updated_data = self.patient_data.copy()
        updated_data['name'] = 'Johnathan Doe Updated'
        updated_data['age'] = 36

        self.client.force_authenticate(user=self.user1)
        response = self.client.put(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Johnathan Doe Updated')
        self.assertEqual(response.data['age'], 36)

        patient.refresh_from_db()
        self.assertEqual(patient.name, 'Johnathan Doe Updated')

    def test_delete_patient(self):
        """DELETE /api/patients/<id>/ - Delete a patient record."""
        patient = Patient.objects.create(created_by=self.user1, **self.patient_data)
        detail_url = reverse('patient-detail', kwargs={'pk': patient.id})

        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(id=patient.id).exists())

    def test_user_cannot_access_or_modify_other_user_patient(self):
        """User 2 should not be able to modify or delete User 1's patient."""
        patient = Patient.objects.create(created_by=self.user1, **self.patient_data)
        detail_url = reverse('patient-detail', kwargs={'pk': patient.id})

        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Patient.objects.filter(id=patient.id).exists())
