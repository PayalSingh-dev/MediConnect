from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Patient
from .serializers import PatientSerializer
from .permissions import IsCreatorOrAdmin


class PatientListCreateView(generics.ListCreateAPIView):
    """
    POST /api/patients/ - Add a new patient (Authenticated users only).
    GET /api/patients/  - Retrieve all patients created by the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Patient.objects.all().select_related('created_by')
        return Patient.objects.filter(created_by=user).select_related('created_by')

    @extend_schema(
        summary="List all patients created by authenticated user",
        description="Retrieves a list of all patient records created by the currently authenticated user.",
        responses={200: PatientSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Add a new patient",
        description="Creates a new patient record associated with the authenticated user.",
        request=PatientSerializer,
        responses={
            201: PatientSerializer,
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Unauthorized"),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'success': True,
                'message': 'Patient created successfully.',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/patients/<id>/    - Get details of a specific patient.
    PUT /api/patients/<id>/    - Update patient details.
    DELETE /api/patients/<id>/ - Delete a patient record.
    """
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrAdmin]
    serializer_class = PatientSerializer
    queryset = Patient.objects.all().select_related('created_by')
    lookup_field = 'pk'

    @extend_schema(
        summary="Get details of a specific patient",
        description="Retrieves the details of a patient by ID. Accessible only by the creator or an admin.",
        responses={
            200: PatientSerializer,
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not found")
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update patient details",
        description="Updates patient details for the given patient ID.",
        request=PatientSerializer,
        responses={
            200: PatientSerializer,
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not found")
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a patient record",
        description="Deletes a patient record by ID. Only the creator or admin can delete.",
        responses={
            204: OpenApiResponse(description="Patient deleted successfully"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Not found")
        }
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                'success': True,
                'message': 'Patient record deleted successfully.'
            },
            status=status.HTTP_204_NO_CONTENT
        )
