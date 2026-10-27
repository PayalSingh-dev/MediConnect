from rest_framework import serializers
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from .models import PatientDoctorMapping


class NestedPatientSerializer(serializers.ModelSerializer):
    """Compact serializer for patient details in mapping views."""
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'contact_number']


class NestedDoctorSerializer(serializers.ModelSerializer):
    """Compact serializer for doctor details in mapping views."""
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'phone', 'email', 'years_of_experience']


class PatientDoctorMappingCreateSerializer(serializers.ModelSerializer):
    """Serializer for assigning a doctor to a patient."""

    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        help_text="ID of the patient."
    )
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        help_text="ID of the doctor."
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        default='',
        help_text="Optional assignment notes or instructions."
    )

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'notes', 'assigned_at']
        read_only_fields = ['id', 'assigned_at']

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')

        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError(
                f"Doctor '{doctor.name}' is already assigned to patient '{patient.name}'."
            )
        return attrs


class PatientDoctorMappingReadSerializer(serializers.ModelSerializer):
    """Serializer for reading patient-doctor mapping with expanded details."""

    patient = NestedPatientSerializer(read_only=True)
    doctor = NestedDoctorSerializer(read_only=True)
    assigned_by_email = serializers.EmailField(source='assigned_by.email', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id',
            'patient',
            'doctor',
            'notes',
            'assigned_by',
            'assigned_by_email',
            'assigned_at',
        ]
        read_only_fields = fields


class AssignedDoctorItemSerializer(serializers.Serializer):
    """Serializer representing an assigned doctor in a patient's mapping list."""

    mapping_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    name = serializers.CharField()
    specialization = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    years_of_experience = serializers.IntegerField()
    notes = serializers.CharField()
    assigned_at = serializers.DateTimeField()


class PatientAssignedDoctorsSerializer(serializers.Serializer):
    """Response serializer for GET /api/mappings/<patient_id>/."""

    patient_id = serializers.IntegerField()
    patient_name = serializers.CharField()
    patient_gender = serializers.CharField()
    patient_age = serializers.IntegerField()
    total_assigned_doctors = serializers.IntegerField()
    assigned_doctors = AssignedDoctorItemSerializer(many=True)
