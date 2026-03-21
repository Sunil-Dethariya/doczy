from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import DoctorBooking, DoctorProfile
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta


if not User.objects.filter(username="doczy").exists():
    User.objects.create_superuser(
        username="doczy",
        email="doczy@gmail.com",
        password="143"
    )

# ---------- AUTH / BASIC PAGES ----------


def index(request):
    return render(request,"index.html")
def auth(request):
    return render(request, "auth.html")


def services(request):
    return render(request, "services.html")


def dashbord(request):
    return render(request, "dashboard.html")


# ---------- BOOKING CREATE ----------

@login_required
def create_booking(request):
    if request.method == "POST":
        DoctorBooking.objects.create(
            user=request.user,
            status="Pending",
            patient_name=request.POST.get("patient_name"),
            mobile=request.POST.get("mobile"),
            age=request.POST.get("age"),
            gender=request.POST.get("gender"),

            address=request.POST.get("address"),
            latitude=request.POST.get("latitude") or None,
            longitude=request.POST.get("longitude") or None,
            location_source=request.POST.get("location_source", "MANUAL"),


            medical_concern=request.POST.get("medical_concern"),
            service_type=request.POST.get("service_type"),
            urgency=request.POST.get("urgency"),

            payment_method=request.POST.get("payment_method"),  # COD / QR
            payment_status="Pending",
            payment_amount=499
        )
        return redirect("booking_success")


def booking_success(request):
    return render(request, "booking_success.html")


# ---------- ADMIN SIDE ----------

@staff_member_required
def admin_booking_list(request):
    """
    Admin ko sirf Pending bookings dikhengi
    """
    bookings = DoctorBooking.objects.filter(
        status="Pending"
    ).order_by("-created_at")

    return render(request, "admin/booking_list.html", {
        "bookings": bookings
    })


@staff_member_required
def admin_booking_detail(request, booking_id):
    booking = get_object_or_404(DoctorBooking, id=booking_id)

    doctors = User.objects.filter(doctorprofile__isnull=False)

    if request.method == "POST":

        # 🔥 PAYMENT UPDATE
        if request.POST.get("action") == "update_payment":
            booking.payment_status = request.POST.get("payment_status")
            booking.save()
            messages.success(request, "Payment status updated successfully.")
            return redirect("admin_booking_detail", booking_id=booking.id)

        # 🔥 DOCTOR ASSIGN
        doctor_id = request.POST.get("doctor_id")
        if doctor_id:
            booking.assigned_doctor_id = doctor_id
            booking.status = "Assigned"
            booking.save()
            return redirect("admin_booking_list")

    return render(request, "admin/booking_detail.html", {
        "booking": booking,
        "doctors": doctors
    })



# ---------- DOCTOR SIDE ----------
@login_required
def doctor_dashboard(request):

    # check doctor profile exists
    profile = DoctorProfile.objects.filter(user=request.user).first()

    # agar profile nahi hai ya incomplete hai
    if not profile or not profile.is_profile_completed:
        return redirect("doctor_create_profile")

    bookings = DoctorBooking.objects.filter(
        assigned_doctor=request.user
    ).order_by("-created_at")

    return render(request, "doctor/dashboard.html", {
        "bookings": bookings,
        "profile": profile
    })

@login_required
def doctor_create_profile(request):

    profile, created = DoctorProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        profile.full_name = request.POST.get("full_name")
        profile.specialization = request.POST.get("specialization")
        profile.qualification = request.POST.get("qualification")
        profile.experience_years = request.POST.get("experience_years")
        profile.languages = request.POST.get("languages")
        profile.city = request.POST.get("city")
        profile.bio = request.POST.get("bio")

        # FILE UPLOADS
        if request.FILES.get("profile_photo"):
            profile.profile_photo = request.FILES.get("profile_photo")

        if request.FILES.get("aadhaar_card"):
            profile.aadhaar_card = request.FILES.get("aadhaar_card")

        if request.FILES.get("pan_card"):
            profile.pan_card = request.FILES.get("pan_card")

        if request.FILES.get("degree_certificate"):
            profile.degree_certificate = request.FILES.get("degree_certificate")

        # mark profile complete
        profile.is_profile_completed = True
        profile.save()

        return redirect("doctor_dashboard")

    return render(request, "doctor/profile_create.html", {
        "profile": profile
    })

@login_required
def doctor_profile_view(request):
    profile = get_object_or_404(DoctorProfile, user=request.user)

    return render(request, "doctor/profile_view.html", {
        "profile": profile
    })

def doctor_profile_edit(request):

    # profile exists or not
    profile, created = DoctorProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        profile.specialization = request.POST.get("specialization")
        profile.experience_years = request.POST.get("experience_years")
        profile.qualification = request.POST.get("qualification")

        # files (optional on edit)
        if request.FILES.get("profile_photo"):
            profile.profile_photo = request.FILES.get("profile_photo")

        if request.FILES.get("aadhar_card"):
            profile.aadhar_card = request.FILES.get("aadhar_card")

        if request.FILES.get("pan_card"):
            profile.pan_card = request.FILES.get("pan_card")

        if request.FILES.get("degree_certificate"):
            profile.degree_certificate = request.FILES.get("degree_certificate")

        profile.save()

        return redirect("doctor_dashboard")

    return render(request, "doctor/profile_edit.html", {
        "profile": profile
    })

def user_logout(request):
    logout(request)
    return redirect("auth")   # auth = login/register page ka url name

@login_required
def doctor_update_booking_status(request, booking_id, action):
    booking = get_object_or_404(
        DoctorBooking,
        id=booking_id,
        assigned_doctor=request.user
    )

    if action == "accept":
        booking.status = "Accepted"

    elif action == "reject":
        booking.status = "Pending"
        booking.assigned_doctor = None

    booking.save()
    return redirect("doctor_dashboard")

def auth_page(request):
    return render(request, "auth.html")


def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect("auth")

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("auth")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid credentials")
            return redirect("auth")

        login(request, user)

        if DoctorProfile.objects.filter(user=user).exists():
            return redirect("doctor_dashboard")
        return redirect("services")

    # ---------- New Notification ----------

def admin_new_booking_count(request):
    """
    Last 1 minute me aayi Pending bookings ka count
    """
    last_minute = now() - timedelta(minutes=1)

    count = DoctorBooking.objects.filter(
        status="Pending",
        created_at__gte=last_minute
    ).count()

    return JsonResponse({"count": count})

def doctor_new_booking_count(request):
    if not request.user.is_authenticated:
        return JsonResponse({"count": 0})

    last_minute = now() - timedelta(minutes=1)

    count = DoctorBooking.objects.filter(
        assigned_doctor=request.user,
        status="Assigned",
        created_at__gte=last_minute
    ).count()

    return JsonResponse({"count": count})