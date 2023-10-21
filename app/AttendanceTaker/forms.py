from django import forms
from .models import Classroom, Student
import json

from .encryption import serverDecrypt, RECIEPT_SALT

#class MakeRoomForm(forms.Form):
#	template_name = "MakeRoomForm.html"
#	classCode = forms.CharField(label="Class code", max_length=30, required=False)
#	classList = forms.CharField(label="JSON class list", widget=forms.Textarea, required=False)

class MakeRoomForm(forms.ModelForm):
	template_name = "MakeRoomForm.html"
	classCode = forms.CharField(label="Class code", max_length=30, required=False),
	classList = forms.CharField(label="JSON class list", widget=forms.Textarea, required=False)

	def clean_classList(self):
		data = self.cleaned_data['classList']
		if data == "": #Allow data to be blank
			return data
		try:
			loadedData = json.loads(data)
			if isinstance(loadedData, list):
				for string in loadedData:
					if not isinstance(string, str):
						raise forms.ValidationError("The JSON array wasn't entirely strings.")
			else:
				raise forms.ValidationError("The JSON data wasn't an array.")
		except json.JSONDecodeError:
			raise forms.ValidationError("The JSON data was invalid.")
		return data

	class Meta:
		model = Classroom
		fields = ["classCode", "classList"]
		widgets = {
			#"classCode": forms.CharField(label="Class code", max_length=30, required=False),
			#"classList": forms.CharField(label="JSON class list", widget=forms.Textarea, required=False)
		}

class AttendanceForm(forms.ModelForm):
	template_name = "TakeAttendanceForm.html"
	fullName = forms.CharField(label="Full name", max_length=30, required=True),
	thisIsMe = forms.BooleanField(label="That is me", required=True)

	class Meta:
		model = Student
		fields = ["fullName"]
		widgets = {
			#"classCode": forms.CharField(label="Class code", max_length=30, required=False),
			#"classList": forms.CharField(label="JSON class list", widget=forms.Textarea, required=False)
		}

class RecieptForm(forms.Form):
	template_name = "RecieptForm.html"
	reciept = forms.CharField(label="Reciept", help_text="A bunch of jumbled text you got when you took attendance.", widget=forms.Textarea, required=False)
	def clean_reciept(self):
		data = self.cleaned_data['reciept']
		#print("First character:", data[0], "Last character:", data[-1])	#Wow, django .trim()s whitespace
		import re
		if(not bool(re.match('^[a-zA-Z0-9_-]+$', data))):
			raise forms.ValidationError("The pasted text wasn't a url safe base64 string. Try again.")
		else:
			return data
