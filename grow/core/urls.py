from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
    path("", views.index_view, name='home'),
    path("er404/", views.error_404_view, name='404')
]