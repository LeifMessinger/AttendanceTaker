import uuid
from django.db import models

# Create your models here.

class AttendanceNote(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False)
	studentId = models.UUIDField(
		#default = uuid.uuid4,	#We should set this ourselves when making an attendance object
                editable = False)
	studentFullName = models.CharField(max_length=200)
	classroomId = models.UUIDField(
		#default = uuid.uuid4,	#We should set this ourselves when making an attendance object
                editable = False)
	takenTime = models.DateTimeField(verbose_name = "attendance taken date")
	def inTimeRange(self, start, stop):
		pass #TODO
#The manager class is automatically made. It's called Attendance.objects


class Classroom(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False)
	classCode = models.CharField(max_length=30, blank=True)
	classList = models.TextField(blank=True) #JSON string

class Student(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False)
	student_fullname = models.CharField(max_length=200)
	classList = models.TextField() #JSON string
	def isTheSame(self, otherStudent):
		pass #TODO probably just compare `id` keys
	@staticmethod
	def areTheSame(a, b):
		return a.isTheSame(b)
	def apply(self, otherStudent):
		pass #TODO apply attributes from 
