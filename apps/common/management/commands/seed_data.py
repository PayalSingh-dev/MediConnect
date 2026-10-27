from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.mappings.models import PatientDoctorMapping

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds sample healthcare data (admin, users, doctors, patients, and mappings).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting healthcare data seeding...'))

        # 1. Create Demo Admin & Care Users
        admin_user, _ = User.objects.get_or_create(
            email='admin@healthcare.com',
            defaults={
                'name': 'System Administrator',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('AdminPassword123!')
        admin_user.save()

        user1, _ = User.objects.get_or_create(
            email='dr.sarah@healthcare.com',
            defaults={'name': 'Dr. Sarah Connor'}
        )
        user1.set_password('DoctorPass123!')
        user1.save()

        user2, _ = User.objects.get_or_create(
            email='nurse.john@healthcare.com',
            defaults={'name': 'Nurse John Miller'}
        )
        user2.set_password('NursePass123!')
        user2.save()

        self.stdout.write(self.style.SUCCESS('✓ Created users: admin@healthcare.com, dr.sarah@healthcare.com, nurse.john@healthcare.com (password for all: see logs or AdminPassword123! / DoctorPass123!)'))

        # 2. Create Doctors
        doctors_data = [
            {
                'name': 'Gregory House',
                'specialization': 'Diagnostic Medicine & Nephrology',
                'phone': '+1-555-0101',
                'email': 'house@diagnostics.org',
                'years_of_experience': 22,
                'created_by': user1,
            },
            {
                'name': 'James Wilson',
                'specialization': 'Oncology',
                'phone': '+1-555-0102',
                'email': 'wilson@oncology.org',
                'years_of_experience': 19,
                'created_by': user1,
            },
            {
                'name': 'Lisa Cuddy',
                'specialization': 'Endocrinology & Hospital Administration',
                'phone': '+1-555-0103',
                'email': 'cuddy@princetonplainsboro.org',
                'years_of_experience': 16,
                'created_by': user1,
            },
            {
                'name': 'Allison Cameron',
                'specialization': 'Immunology',
                'phone': '+1-555-0104',
                'email': 'cameron@immunology.org',
                'years_of_experience': 9,
                'created_by': user2,
            },
            {
                'name': 'Eric Foreman',
                'specialization': 'Neurology',
                'phone': '+1-555-0105',
                'email': 'foreman@neurology.org',
                'years_of_experience': 11,
                'created_by': user2,
            },
        ]

        created_doctors = []
        for d in doctors_data:
            doc, _ = Doctor.objects.update_or_create(
                email=d['email'],
                defaults=d
            )
            created_doctors.append(doc)

        self.stdout.write(self.style.SUCCESS(f'✓ Created/Updated {len(created_doctors)} doctors.'))

        # 3. Create Patients
        patients_data = [
            {
                'name': 'Robert Chase',
                'age': 34,
                'gender': 'Male',
                'contact_number': '+1-555-0201',
                'email': 'robert.chase@example.com',
                'address': '452 Pine Hill Rd, Princeton, NJ',
                'medical_history': 'Prior acute pancreatitis, recovered. No drug allergies.',
                'created_by': user1,
            },
            {
                'name': 'Remy Hadley',
                'age': 30,
                'gender': 'Female',
                'contact_number': '+1-555-0202',
                'email': 'remy.hadley@example.com',
                'address': '78 Oak Ridge Ave, Princeton, NJ',
                'medical_history': "Huntington's disease gene positive; quarterly neuro-monitoring required.",
                'created_by': user1,
            },
            {
                'name': 'Christopher Taub',
                'age': 48,
                'gender': 'Male',
                'contact_number': '+1-555-0203',
                'email': 'chris.taub@example.com',
                'address': '12 Maple Court, Plainsboro, NJ',
                'medical_history': 'Essential hypertension, managed with ACE inhibitors.',
                'created_by': user2,
            },
            {
                'name': 'Martha Masters',
                'age': 25,
                'gender': 'Female',
                'contact_number': '+1-555-0204',
                'email': 'martha.masters@example.com',
                'address': '99 College Rd, Princeton, NJ',
                'medical_history': 'Seasonal allergic rhinitis. Penicillin allergy.',
                'created_by': user2,
            },
        ]

        created_patients = []
        for p in patients_data:
            pat, _ = Patient.objects.update_or_create(
                name=p['name'],
                created_by=p['created_by'],
                defaults=p
            )
            created_patients.append(pat)

        self.stdout.write(self.style.SUCCESS(f'✓ Created/Updated {len(created_patients)} patients.'))

        # 4. Create Mappings
        mappings_data = [
            (created_patients[0], created_doctors[0], 'Primary diagnostic lead'),
            (created_patients[0], created_doctors[4], 'Neurology consult'),
            (created_patients[1], created_doctors[4], 'Neurological evaluation and progression monitoring'),
            (created_patients[1], created_doctors[1], 'Oncology screening'),
            (created_patients[2], created_doctors[2], 'Endocrine workup'),
            (created_patients[3], created_doctors[3], 'Allergy and immunological desensitization'),
        ]

        assigned_count = 0
        for patient, doctor, notes in mappings_data:
            mapping, created = PatientDoctorMapping.objects.get_or_create(
                patient=patient,
                doctor=doctor,
                defaults={'notes': notes, 'assigned_by': user1}
            )
            if created:
                assigned_count += 1

        self.stdout.write(self.style.SUCCESS(f'✓ Assigned doctors to patients ({assigned_count} new mappings).'))
        self.stdout.write(self.style.SUCCESS('Healthcare data seeded successfully!'))
