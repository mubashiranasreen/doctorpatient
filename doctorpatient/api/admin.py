from django.contrib import admin
from .models import Department, PatientRecord

# Register your models here.
admin.site.register(Department)
admin.site.register(PatientRecord)
