from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("chat/", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]
