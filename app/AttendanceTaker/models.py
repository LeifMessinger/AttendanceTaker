from django.db import models

# Create your models here.

class Attendance(models.Model):
	student_fullname = models.CharField(max_length=200)
	taken = models.DateTimeField(verbose_name = "attendance taken date")
