from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    POST /api/doctors/ - Add a new doctor (Authenticated users only).
    GET /api/doctors/  - Retrieve all doctors.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all().select_related('created_by')

    @extend_schema(
        summary="Retrieve all doctors",
        description="Returns a list of all doctors in the healthcare system.",
        responses={200: DoctorSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Add a new doctor",
        description="Creates a new doctor record in the system (Authenticated users only).",
        request=DoctorSerializer,
        responses={
            201: DoctorSerializer,
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
                'message': 'Doctor added successfully.',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/doctors/<id>/    - Get details of a specific doctor.
    PUT /api/doctors/<id>/    - Update doctor details.
    DELETE /api/doctors/<id>/ - Delete a doctor record.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all().select_related('created_by')
    lookup_field = 'pk'

    @extend_schema(
        summary="Get details of a specific doctor",
        description="Retrieves the full details of a doctor by their ID.",
        responses={
            200: DoctorSerializer,
            404: OpenApiResponse(description="Doctor not found"),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update doctor details",
        description="Updates details of a doctor record.",
        request=DoctorSerializer,
        responses={
            200: DoctorSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Doctor not found"),
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a doctor record",
        description="Deletes a doctor record by ID.",
        responses={
            204: OpenApiResponse(description="Doctor deleted successfully"),
            404: OpenApiResponse(description="Doctor not found"),
        }
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                'success': True,
                'message': 'Doctor record deleted successfully.'
            },
            status=status.HTTP_204_NO_CONTENT
        )
