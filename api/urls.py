from django.urls import path

from .views import (
    PatientListCreateView,
    PatientRetrieveUpdateDestroyView,
    StudyRetrieveUpdateDestroyView,
    StudytListCreateView,
)

urlpatterns = [
    path(
        'patients/',
        PatientListCreateView.as_view(),
        name='patient_list_create'),
    path(
        'patients/<int:pk>/',
        PatientRetrieveUpdateDestroyView.as_view(),
        name='patient_get_update_delete'),
    path(
        'patients/<int:patient_pk>/studies',
        StudytListCreateView.as_view(),
        name='study_list_create'),
    path(
        'patients/<int:patient_pk>/studies/<int:pk>/',
        StudyRetrieveUpdateDestroyView.as_view(),
        name='study_get_update_delete'),
]
