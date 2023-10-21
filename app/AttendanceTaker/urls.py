from django.urls import path, re_path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'attendance', views.AttendanceNoteViewSet)	#Update me
router.register(r'students', views.StudentViewSet)
router.register(r'classroom', views.ClassroomViewSet)

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("MakeRoom/", views.make_room, name="home"),
    path("room/", views.room, name="room"),
    path("done/", views.done, name="done"),
    path("verifyReciept/", views.verifyReciept, name="verifyReciept"),
    path("ClassroomQRCode/", views.ClassroomQRCode.as_view(), name="ClassroomQRCode"),
    path("ClassroomAttendanceList/", views.ClassroomAttendanceList.as_view(), name="ClassroomAttendanceList"),
    path("ClassroomAbsenceList/", views.ClassroomAbsenceList.as_view(), name="ClassroomAbsenceList"),
    re_path(r"^(?P<base64String>[-_A-Za-z0-9+=]{50,})/?", views.take_attendance, name="take_attendance"),
    path('', include(router.urls)),
] + static(settings.STATIC_URL + "AttendanceTaker/", document_root=settings.STATIC_ROOT)
