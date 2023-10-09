from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import PatientRecord, Department
from .serializers import PatientRecordSerializer, DepartmentSerializer, PatientSerializer, DoctorSerializer, \
    UserSerializer
from .permissions import IsPatient, IsDoctor


class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Doctors')
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        serializer.save()


# View to retrieve, update, or delete a specific doctor
class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(groups__name='Doctors')
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]


# View to list all patients and create a new patient
class PatientListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Patients')
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        serializer.save()


# View to retrieve, update, or delete a specific patient
class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(groups__name='Patients')
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]


# View to list all patient records and create a new patient record
class PatientRecordListCreateView(generics.ListCreateAPIView):
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the patient field to the currently authenticated user (patient)
        serializer.save(patient=self.request.user)


# View to retrieve, update, or delete a specific patient record
class PatientRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Patients').exists():
            # Patients can only access their own records
            return PatientRecord.objects.filter(patient=user)
        elif user.groups.filter(name='Doctors').exists():
            # Doctors can access records of their patients
            return PatientRecord.objects.filter(department=user.doctorprofile.department)


# View to list all departments and create a new department
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


# View to retrieve, update, or delete a specific department
class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


# View to list all doctors in a specific department
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def department_doctors(request, pk):
    department = generics.get_object_or_404(Department, pk=pk)
    doctors = User.objects.filter(groups__name='Doctors', doctorprofile__department=department)
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


# View to list all patients in a specific department
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def department_patients(request, pk):
    department = generics.get_object_or_404(Department, pk=pk)
    patients = User.objects.filter(groups__name='Patients', patientprofile__department=department)
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


# View to log in and obtain an authentication token
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(Q(username=username) | Q(email=username)).first()
    if user is not None and user.check_password(password):
        login(request, user)
        # Generate and return an authentication token
        return Response({'token': user.auth_token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=401)


# View to register a new user (patient or doctor)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Set the user's password and group based on their role
        if 'is_doctor' in request.data and request.data['is_doctor']:
            user.set_password(request.data['password'])
            user.groups.add(Group.objects.get(name='Doctors'))
        else:
            user.set_password(request.data['password'])
            user.groups.add(Group.objects.get(name='Patients'))
        user.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# View to log out and invalidate the authentication token
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=200)
