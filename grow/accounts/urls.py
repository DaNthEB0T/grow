from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.registration_view, name="register"),
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("verification/<uidb64>/<token>", views.verification_view, name="verification")
]