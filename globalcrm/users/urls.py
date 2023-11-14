from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from . import views


app_name = "users"

urlpatterns = [
    path(
        "register/",
        views.RegisterUser.as_view(template_name="users/register.html"),
        name="register",
    ),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path(
        "logout/",
        LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
