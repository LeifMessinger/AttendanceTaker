import uuid
from django.db import models

# Create your models here.

class Student(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False)
	fullName = models.CharField(max_length=200)
	ipAddr = models.CharField(max_length=42, null=True)	#Can be null
	#Probably store more data about the student
	def isTheSame(self, otherStudent):
		pass #TODO probably just compare `id` keys
	@staticmethod
	def areTheSame(a, b):
		return a.isTheSame(b)
	def apply(self, otherStudent):
		pass #TODO apply attributes from 
	def attend(self, classroom):
		#Create AttendanceNote
		from django.utils import timezone
		import pytz	#Python Timezone
		note = AttendanceNote(studentId=self,
			studentFullName=self.fullName,
			classroomId=classroom,
			takenTime=timezone.localtime(timezone=pytz.timezone("America/Panama"))	#Central time
		)
		#Save attendance note
		note.save()
		#Add attendance note to classroom
		classroom.attendanceNotes.add(note)
		classroom.save()

		#return nothing (the classroom was changed by reference and the caller should save the classroom)
		return note
#The student manager class is automatically made. It's called Student.objects

class AttendanceNote(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False)
	#Python forwards declarations suckkk so I gotta do this v
	studentId = models.ForeignKey('AttendanceTaker.Student', on_delete=models.CASCADE)	#Many to one
	studentFullName = models.CharField(max_length=200)
	classroomId = models.ForeignKey('AttendanceTaker.Classroom', on_delete=models.CASCADE)	#Maybe just SET_NULL or SET(AttendanceNote(someFillerOpts)). SET_NULL requires null=True for the foreign key tho.
	takenTime = models.DateTimeField(verbose_name = "attendance taken date")
	def inTimeRange(self, start, stop):
		pass #TODO
	def __str__(self):
		return 'Student {} attended class at {} in classroom '.format(self.studentFullName, self.takenTime, self.classroomId.classCode)

class Classroom(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False)
	classCode = models.CharField(max_length=30, blank=True)
	classList = models.TextField(blank=True) #JSON string
	attendanceNotes = models.ManyToManyField(AttendanceNote)
