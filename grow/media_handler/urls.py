from django.urls import path
from . import views

app_name = "media_handler"

urlpatterns = [
    path("", views.index, name="login"),
]