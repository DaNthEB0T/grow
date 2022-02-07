from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
    path("dashboard/", views.dashboard_view, name='dashboard'),
    path("unvalidated/", views.unvalidated_view, name='unvalidated'),
    path("cookies", views.cookie_view, name='cookies')
]
