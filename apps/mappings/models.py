from django.db import models
from django.conf import settings
from apps.patients.models import Patient
from apps.doctors.models import Doctor


class PatientDoctorMapping(models.Model):
    """
    Mapping model representing the assignment of a doctor to a patient.
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='doctor_mappings',
        help_text="The patient assigned to the doctor."
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='patient_mappings',
        help_text="The doctor assigned to the patient."
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_mappings',
        help_text="The authenticated user who created this assignment."
    )
    notes = models.TextField(
        blank=True,
        default='',
        help_text="Clinical or administrative notes for this assignment."
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Patient-Doctor Mapping'
        verbose_name_plural = 'Patient-Doctor Mappings'
        ordering = ['-assigned_at']
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'doctor'],
                name='unique_patient_doctor_mapping'
            )
        ]

    def __str__(self):
        return f"Patient: {self.patient.name} -> Doctor: Dr. {self.doctor.name}"
