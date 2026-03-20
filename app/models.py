from django.db import models
from django.contrib.auth.models import User

class DoctorBooking(models.Model):

    SERVICE_CHOICES = [
        ('Emergency', 'Emergency'),
        ('Non-Emergency', 'Non-Emergency'),
        ('Scheduled', 'Scheduled'),
    ]

    URGENCY_CHOICES = [
        ('Emergency', 'Immediate Emergency'),
        ('2 Hours', 'Within 2 Hours'),
        ('5 Hours', 'Within 5 Hours'),
        ('24 Hours', 'Within 24 Hours'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Visit'),
        ('QR', 'QR Payment'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    assigned_doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctor_bookings"
    )

    patient_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    medical_concern = models.TextField()

    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)


    # ===== LOCATION FIELDS =====
    address = models.TextField(help_text="Patient full address")

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    LOCATION_SOURCE_CHOICES = [
        ("GPS", "GPS"),
        ("MANUAL", "Manual"),
    ]

    location_source = models.CharField(
        max_length=30,
        choices=LOCATION_SOURCE_CHOICES,
        default="MANUAL"
    )

    # ... (created_at, __str__ etc)
    # 🔥 PAYMENT FIELDS (NEW)
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default='COD'
    )

    payment_status = models.CharField(
        max_length=15,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )

    payment_amount = models.PositiveIntegerField(default=499)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.payment_status}"

    def __str__(self):
        return self.patient_name

from django.db import models
from django.contrib.auth.models import User

class DoctorProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctorprofile"
    )

    # 🔵 PUBLIC PROFILE INFO
    profile_photo = models.ImageField(
        upload_to="doctor/profile_photos/",
        null=True,
        blank=True
    )

    full_name = models.CharField(max_length=100,null=True,blank=True)
    specialization = models.CharField(max_length=100,null=True,blank=True)

    qualification = models.CharField(
        max_length=150,null=True,blank=True,
        help_text="e.g. MBBS, MD"
    )

    experience_years = models.PositiveIntegerField(null=True,blank=True)

    languages = models.CharField(
        max_length=200,null=True,blank=True,
        help_text="Comma separated (English, Hindi, Gujarati)"
    )

    city = models.CharField(max_length=100,null=True,blank=True)

    bio = models.TextField(
        blank=True,null=True,
        help_text="Short professional introduction"
    )

    # 🔴 PRIVATE DOCUMENTS (ADMIN ONLY)
    aadhaar_card = models.FileField(
        upload_to="doctor/documents/aadhaar/",
        null=True,
        blank=True
    )

    pan_card = models.FileField(
        upload_to="doctor/documents/pan/",
        null=True,
        blank=True
    )

    degree_certificate = models.FileField(
        upload_to="doctor/documents/degree/",
        null=True,
        blank=True
    )

    # ⚙️ SYSTEM FLAGS
    is_profile_completed = models.BooleanField(default=False,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.specialization})"
