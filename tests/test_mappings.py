from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.mappings.models import PatientDoctorMapping

User = get_user_model()


class MappingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='coordinator@healthcare.com',
            password='Password123!',
            name='Care Coordinator'
        )

        self.patient = Patient.objects.create(
            name='Robert Chase',
            age=32,
            gender='Male',
            contact_number='+1-555-0456',
            created_by=self.user
        )

        self.doctor1 = Doctor.objects.create(
            name='Allison Cameron',
            specialization='Immunology',
            phone='+1-555-0789',
            email='cameron@healthcare.com',
            years_of_experience=8
        )

        self.doctor2 = Doctor.objects.create(
            name='Eric Foreman',
            specialization='Neurology',
            phone='+1-555-0790',
            email='foreman@healthcare.com',
            years_of_experience=10
        )

        self.mapping_list_url = reverse('mapping-list-create')

    def test_assign_doctor_to_patient_success(self):
        """POST /api/mappings/ - Assign a doctor to a patient."""
        self.client.force_authenticate(user=self.user)
        payload = {
            'patient': self.patient.id,
            'doctor': self.doctor1.id,
            'notes': 'Initial neurological consultation.'
        }
        response = self.client.post(self.mapping_list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get('success'))
        self.assertEqual(response.data['data']['patient']['id'], self.patient.id)
        self.assertEqual(response.data['data']['doctor']['id'], self.doctor1.id)

        # Verify record in database
        self.assertTrue(
            PatientDoctorMapping.objects.filter(patient=self.patient, doctor=self.doctor1).exists()
        )

    def test_assign_duplicate_doctor_to_patient_fails(self):
        """Cannot assign the same doctor to the same patient twice."""
        PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor1,
            assigned_by=self.user
        )
        self.client.force_authenticate(user=self.user)
        payload = {
            'patient': self.patient.id,
            'doctor': self.doctor1.id
        }
        response = self.client.post(self.mapping_list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_mappings(self):
        """GET /api/mappings/ - Retrieve all patient-doctor mappings."""
        PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor1,
            assigned_by=self.user
        )
        PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor2,
            assigned_by=self.user
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.mapping_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_doctors_assigned_to_specific_patient(self):
        """GET /api/mappings/<patient_id>/ - Get all doctors assigned to a specific patient."""
        m1 = PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor1,
            notes='Allergy treatment plan',
            assigned_by=self.user
        )
        m2 = PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor2,
            notes='Neurological exam',
            assigned_by=self.user
        )

        patient_mapping_url = reverse('mapping-detail-or-patient', kwargs={'pk': self.patient.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(patient_mapping_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patient_id'], self.patient.id)
        self.assertEqual(response.data['total_assigned_doctors'], 2)

        assigned_doctor_ids = [d['doctor_id'] for d in response.data['assigned_doctors']]
        self.assertIn(self.doctor1.id, assigned_doctor_ids)
        self.assertIn(self.doctor2.id, assigned_doctor_ids)

        mapping_ids = [d['mapping_id'] for d in response.data['assigned_doctors']]
        self.assertIn(m1.id, mapping_ids)
        self.assertIn(m2.id, mapping_ids)

    def test_delete_mapping_removes_doctor_from_patient(self):
        """DELETE /api/mappings/<id>/ - Remove a doctor from a patient."""
        mapping = PatientDoctorMapping.objects.create(
            patient=self.patient,
            doctor=self.doctor1,
            assigned_by=self.user
        )
        delete_url = reverse('mapping-detail-or-patient', kwargs={'pk': mapping.id})

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Mapping should no longer exist
        self.assertFalse(PatientDoctorMapping.objects.filter(id=mapping.id).exists())

    def test_unauthenticated_requests_blocked(self):
        """Unauthenticated requests must be rejected with 401."""
        response = self.client.get(self.mapping_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
