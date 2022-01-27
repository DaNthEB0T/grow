from django.urls import path
from . import views

app_name = "media_handler"

urlpatterns = [
    path("", views.mh_view, name="media_test"),
]