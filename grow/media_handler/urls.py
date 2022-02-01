from django.urls import path
from . import views

app_name = "media_handler"

urlpatterns = [
    path("media", views.mh_view, name="media_test"),
    path("postu", views.post_handle_view, name="post_test"),
    path("post/<slug:slug>", views.post_view, name="post")
]