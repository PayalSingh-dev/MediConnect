from django.urls import path
from .views import MappingListCreateView, MappingDetailOrPatientMappingsView

urlpatterns = [
    path('', MappingListCreateView.as_view(), name='mapping-list-create'),
    path('<int:pk>/', MappingDetailOrPatientMappingsView.as_view(), name='mapping-detail-or-patient'),
]
