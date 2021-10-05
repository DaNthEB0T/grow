from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registration_view, name="accounts-register"),
    path("login/", views.login_view, name="accounts-login"),
    path("logout/", views.logout_view, name="accounts-logout"),
]