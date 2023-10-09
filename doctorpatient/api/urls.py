from django.urls import path
from .views import DoctorListCreateView, DoctorDetailView, PatientListCreateView, PatientDetailView, \
    PatientRecordListCreateView, PatientRecordDetailView, DepartmentListCreateView, DepartmentDetailView, \
    department_doctors, department_patients, login_view, register_view, logout_view

urlpatterns = [
    path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('patient_records/', PatientRecordListCreateView.as_view(), name='patient-record-list-create'),
    path('patient_records/<int:pk>/', PatientRecordDetailView.as_view(), name='patient-record-detail'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('departments/<int:pk>/doctors/', department_doctors, name='department-doctor-list'),
    path('departments/<int:pk>/patients/', department_patients, name='department-patient-list'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
