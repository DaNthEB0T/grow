from unicodedata import name
from django.urls import path
from . import views

app_name = "media_handler"

urlpatterns = [
    #path("media", views.mh_view, name="media_test"),
    path("postu", views.post_handle_view, name="post_upload"),
    path("post/<slug:slug>", views.post_view, name="post"),
    path("post/<slug:slug>/toggle_save", views.post_save_view, name="post_save"),
    path("post/<slug:slug>/toggle_watch_later", views.watch_later_view, name="post_to_watchlist"),
    path("history", views.history_view, name="history"),
    path("saved", views.saved_view, name="saved"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("history/remove/<slug:slug>", views.remove_from_history_view, name="remove_from_history"),
    path("saved/remove/<slug:slug>", views.remove_from_saved_view, name="remove_from_saved"),
    path("watchlist/remove/<slug:slug>", views.remove_from_watchlist_view, name="remove_from_watchlist"),
]