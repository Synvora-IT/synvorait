from .views import user_login , user_logout, user_signup, activate_account, update_info
from django.urls import path

urlpatterns = [
    path("login/" , user_login , name = "login"),

    path("signup/" , user_signup , name = "signup"),

    path("update-info/" , update_info , name = "update-info"),

    path("activate-account/<uuid:id>/<str:code>/" , activate_account , name = "activate-account"),

    path("logout/" , user_logout , name = "logout"),
]
