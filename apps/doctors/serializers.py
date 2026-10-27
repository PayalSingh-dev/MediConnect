import re
from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor records."""

    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'specialization',
            'phone',
            'email',
            'years_of_experience',
            'created_by',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_by_email', 'created_at', 'updated_at']

    def validate_name(self, value):
        stripped = value.strip()
        if not stripped:
            raise serializers.ValidationError('Doctor name cannot be blank.')
        return stripped

    def validate_specialization(self, value):
        stripped = value.strip()
        if not stripped:
            raise serializers.ValidationError('Specialization cannot be blank.')
        return stripped

    def validate_phone(self, value):
        stripped = value.strip()
        if not re.match(r'^\+?[0-9\s\-]{7,20}$', stripped):
            raise serializers.ValidationError('Enter a valid phone number.')
        return stripped

    def validate_email(self, value):
        normalized = value.strip().lower()
        query = Doctor.objects.filter(email=normalized)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError('A doctor with this email address already exists.')
        return normalized

    def validate_years_of_experience(self, value):
        if value < 0 or value > 80:
            raise serializers.ValidationError('Years of experience must be between 0 and 80.')
        return value
