from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.welcome_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("verification/<uidb64>/<token>", views.verification_view, name="verification"),
    path("forgot_password/", views.forgot_password_view, name="forgot_password"),
    path("password_reset/<uidb64>/<token>", views.password_reset_view, name="password_reset"),
]