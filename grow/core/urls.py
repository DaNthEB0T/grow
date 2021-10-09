from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
    path("er404/", views.error_404_view, name='404'),
    path("dashboard/", views.index_view, name='dashboard'),
]