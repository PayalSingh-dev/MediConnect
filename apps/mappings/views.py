from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from apps.patients.models import Patient
from .models import PatientDoctorMapping
from .serializers import (
    PatientDoctorMappingCreateSerializer,
    PatientDoctorMappingReadSerializer,
    PatientAssignedDoctorsSerializer,
)


class MappingListCreateView(APIView):
    """
    POST /api/mappings/ - Assign a doctor to a patient.
    GET  /api/mappings/ - Retrieve all patient-doctor mappings.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Retrieve all patient-doctor mappings",
        description="Retrieves all mappings between patients and doctors. Can filter by patient_id or doctor_id.",
        parameters=[
            OpenApiParameter(name='patient_id', type=int, required=False, description='Filter by patient ID'),
            OpenApiParameter(name='doctor_id', type=int, required=False, description='Filter by doctor ID'),
        ],
        responses={200: PatientDoctorMappingReadSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        queryset = PatientDoctorMapping.objects.select_related('patient', 'doctor', 'assigned_by').all()

        patient_id = request.query_params.get('patient_id')
        doctor_id = request.query_params.get('doctor_id')

        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        serializer = PatientDoctorMappingReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Assign a doctor to a patient",
        description="Creates a new association between an existing patient and doctor.",
        request=PatientDoctorMappingCreateSerializer,
        responses={
            201: PatientDoctorMappingReadSerializer,
            400: OpenApiResponse(description="Validation error or mapping already exists"),
            401: OpenApiResponse(description="Unauthorized"),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = PatientDoctorMappingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mapping = serializer.save(assigned_by=request.user)

        response_serializer = PatientDoctorMappingReadSerializer(mapping)
        return Response(
            {
                'success': True,
                'message': f"Doctor '{mapping.doctor.name}' assigned to patient '{mapping.patient.name}' successfully.",
                'data': response_serializer.data,
            },
            status=status.HTTP_201_CREATED
        )


class MappingDetailOrPatientMappingsView(APIView):
    """
    GET    /api/mappings/<patient_id>/ - Get all doctors assigned to a specific patient.
    DELETE /api/mappings/<id>/         - Remove a doctor from a patient (delete mapping by mapping ID).
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get all doctors assigned to a specific patient",
        description="Retrieves a list of all doctors assigned to a given patient by patient_id.",
        responses={
            200: PatientAssignedDoctorsSerializer,
            404: OpenApiResponse(description="Patient not found"),
        }
    )
    def get(self, request, pk, *args, **kwargs):
        # First check if pk refers to a Patient
        patient = Patient.objects.filter(pk=pk).first()
        if patient is not None:
            mappings = PatientDoctorMapping.objects.filter(patient=patient).select_related('doctor')

            assigned_doctors = [
                {
                    'mapping_id': m.id,
                    'doctor_id': m.doctor.id,
                    'name': m.doctor.name,
                    'specialization': m.doctor.specialization,
                    'phone': m.doctor.phone,
                    'email': m.doctor.email,
                    'years_of_experience': m.doctor.years_of_experience,
                    'notes': m.notes,
                    'assigned_at': m.assigned_at,
                }
                for m in mappings
            ]

            payload = {
                'patient_id': patient.id,
                'patient_name': patient.name,
                'patient_gender': patient.gender,
                'patient_age': patient.age,
                'total_assigned_doctors': len(assigned_doctors),
                'assigned_doctors': assigned_doctors,
            }
            serializer = PatientAssignedDoctorsSerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Fallback: check if pk refers to a specific Mapping ID
        mapping = PatientDoctorMapping.objects.filter(pk=pk).select_related('patient', 'doctor', 'assigned_by').first()
        if mapping is not None:
            serializer = PatientDoctorMappingReadSerializer(mapping)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {
                'success': False,
                'message': f"No patient or mapping found with ID '{pk}'."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        summary="Remove a doctor from a patient",
        description="Deletes a patient-doctor mapping record by its mapping ID.",
        responses={
            204: OpenApiResponse(description="Mapping removed successfully"),
            404: OpenApiResponse(description="Mapping not found"),
        }
    )
    def delete(self, request, pk, *args, **kwargs):
        mapping = get_object_or_404(PatientDoctorMapping, pk=pk)
        patient_name = mapping.patient.name
        doctor_name = mapping.doctor.name
        mapping.delete()

        return Response(
            {
                'success': True,
                'message': f"Doctor '{doctor_name}' unassigned from patient '{patient_name}' successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )
