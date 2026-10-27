import re
from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for patient records."""

    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'age',
            'gender',
            'contact_number',
            'email',
            'address',
            'medical_history',
            'created_by',
            'created_by_email',
            'created_by_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_by_email', 'created_by_name', 'created_at', 'updated_at']

    def validate_name(self, value):
        stripped = value.strip()
        if not stripped:
            raise serializers.ValidationError('Patient name cannot be blank.')
        return stripped

    def validate_contact_number(self, value):
        stripped = value.strip()
        # Accept digits, optional leading +, dashes, spaces
        if not re.match(r'^\+?[0-9\s\-]{7,20}$', stripped):
            raise serializers.ValidationError('Enter a valid contact phone number.')
        return stripped

    def validate_age(self, value):
        if value < 0 or value > 130:
            raise serializers.ValidationError('Age must be between 0 and 130.')
        return value
