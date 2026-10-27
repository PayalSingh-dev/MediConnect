from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Doctor(models.Model):
    """
    Doctor model representing medical practitioners in the healthcare system.
    """
    name = models.CharField(max_length=200, db_index=True)
    specialization = models.CharField(max_length=150, db_index=True)
    phone = models.CharField(max_length=25)
    email = models.EmailField(unique=True, db_index=True)
    years_of_experience = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Years of professional clinical experience."
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctors_created',
        help_text="User who added this doctor record."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        ordering = ['name']

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"
