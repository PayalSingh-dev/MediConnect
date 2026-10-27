from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Patient(models.Model):
    """
    Patient model representing patient records created and managed by users.
    """
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    name = models.CharField(max_length=200, db_index=True)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(130)],
        help_text="Patient's age in years (0-130)"
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=25)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, default='')
    medical_history = models.TextField(
        blank=True,
        default='',
        help_text="Patient's medical history, preexisting conditions, or relevant clinical notes."
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patients',
        help_text="User who created and manages this patient record."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (Age: {self.age}, {self.gender})"
