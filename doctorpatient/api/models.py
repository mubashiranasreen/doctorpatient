from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=255)
    diagnostics = models.TextField()
    location = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)


class PatientRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    diagnostics = models.TextField()
    observations = models.TextField()
    treatments = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
