from .views import user_login , user_logout, user_signup, activate_account, update_info, change_password, verify_change_password_code, resend_code
from django.urls import path

urlpatterns = [
    path("login/" , user_login , name = "login"),

    path("signup/" , user_signup , name = "signup"),

    path("update-info/" , update_info , name = "update-info"),

    path("change-password/" , change_password , name = "change-password"),

    path("verify-change-password-code/" , verify_change_password_code , name = "verify-change-password-code"),

    path("resend-code/" , resend_code , name = "resend-code"),

    path("activate-account/<uuid:id>/<str:code>/" , activate_account , name = "activate-account"),

    path("logout/" , user_logout , name = "logout"),
]
