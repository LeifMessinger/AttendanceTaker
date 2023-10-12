from django.urls import path

from . import views

urlpatterns = [
    path("MakeRoom/", views.make_room, name="home"),
    path("room/", views.room, name="room"),
]
