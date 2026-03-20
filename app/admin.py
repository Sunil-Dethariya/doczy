from django.contrib import admin
from .models import *
# Register your models here.

class DoctorBookingAdmin(admin.ModelAdmin):
    list_display = ["user","assigned_doctor","patient_name","mobile","gender","medical_concern","service_type","urgency","status","location_source",'payment_method','payment_status','payment_amount',"created_at"]
    search_fields = ("patient_name", "address")
    list_filter = ('payment_method', 'payment_status', 'status')
admin.site.register(DoctorBooking,DoctorBookingAdmin)

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ["user","profile_photo","full_name","specialization","qualification","experience_years","languages","city","bio","aadhaar_card","pan_card","degree_certificate","is_profile_completed","created_at"]

admin.site.register(DoctorProfile,DoctorProfileAdmin)