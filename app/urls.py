from django.urls import path
from . import views

urlpatterns = [

    # Auth & basic pages
    path("d",views.index,name="index"),
    path("auth/", views.auth, name="auth"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("", views.services, name="services"),
    path("dashbord/", views.dashbord, name="dashbord"),

    # Booking
    path("create-booking/", views.create_booking, name="create_booking"),
    path("success/", views.booking_success, name="booking_success"),

    # Admin panel (CUSTOM, not Django admin)
    path(
        "admin-panel/bookings/",
        views.admin_booking_list,
        name="admin_booking_list"
    ),

    path(
        "admin-panel/bookings/<int:booking_id>/",
        views.admin_booking_detail,
        name="admin_booking_detail"
    ),

    # Doctor
    path(
        "doctor/dashboard/",
        views.doctor_dashboard,
        name="doctor_dashboard"
    ),

    path(
        "doctor/booking/<int:booking_id>/<str:action>/",
        views.doctor_update_booking_status,
        name="doctor_update_booking_status"
    ),

    path(
        "admin-panel/notifications/",
        views.admin_new_booking_count,
        name="admin_new_booking_count"
    ),
    path(
        "doctor/notifications/",
        views.doctor_new_booking_count,
        name="doctor_new_booking_count"
    ),
    path(
        "doctor/profile/create/",
        views.doctor_create_profile,
        name="doctor_create_profile"
    ),
    path(
        "doctor/profile/",
        views.doctor_profile_view,
        name="doctor_profile_view"
    ),
    path("logout/", views.user_logout, name="logout"),
    path(
        "doctor/profile/",
        views.doctor_profile_edit,
        name="doctor_profile_edit"
    ),
    path("assign-doctor/", views.assign_doctor_page, name="assign_doctor"),
]
