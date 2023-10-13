from rest_framework_json_api import serializers
from .models import AttendanceNote, Student, Classroom

class AttendanceNoteSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = AttendanceNote
		fields = '__all__'
		#fields = ('name', 'address', 'dish_set') #Whitelist
		#exclude = ['id'] #Blacklist

class StudentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Student
		fields = '__all__'

class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Classroom
		fields = '__all__'
