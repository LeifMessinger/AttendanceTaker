from django import forms
from .models import Classroom

#class MakeRoomForm(forms.Form):
#	template_name = "MakeRoomForm.html"
#	classCode = forms.CharField(label="Class code", max_length=30, required=False)
#	classList = forms.CharField(label="JSON class list", widget=forms.Textarea, required=False)

class MakeRoomForm(forms.ModelForm):
	template_name = "MakeRoomForm.html"
	class Meta:
		model = Classroom
		fields = ["classCode", "classList"]
		widgets = {
			classCode = forms.CharField(label="Class code", max_length=30, required=False),
			classList = forms.CharField(label="JSON class list", widget=forms.Textarea, required=False)
		}

class AttendanceForm(forms.Form):
	template_name = "TakeAttendanceForm.html"
	subject = forms.CharField(label="Your name", max_length=30, required=False)
	thisIsMe = forms.BooleanField(label="That is me", required=True)
