from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'attendance', views.AttendanceNoteViewSet)	#Update me
router.register(r'students', views.StudentViewSet)
router.register(r'classroom', views.ClassroomViewSet)

urlpatterns = [
    path("MakeRoom/", views.make_room, name="home"),
    path("room/", views.room, name="room"),
    path("ClassroomQRCode/", views.ClassroomQRCode.as_view(), name="ClassroomQRCode"),
    path('', include(router.urls)),
]
