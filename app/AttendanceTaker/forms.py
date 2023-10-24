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
	classCode = forms.CharField(label="Class code", max_length=30, required=False)
	classCode.widget.attrs.update({
		'placeholder': 'optional'
	})
	classList = forms.CharField(label="Class list", widget=forms.Textarea, required=False)
	classList.widget.attrs.update({
		'placeholder': 'optional\n\n["Json", "string", "array"]\n\nComma,Separated,Values  or  Tab\tSeparated\tValues\n\nNewline\nSeparated\nValues'
	})

	def clean_classList(self):
		data = self.cleaned_data['classList']
		if data == "": #Allow data to be blank
			return data
		Classroom.cleanClassList(data)
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
	fullName = forms.CharField(label="Full name", max_length=100, required=True)
	fullName.widget.attrs.update({
		'autoComplete': 'on',
		'list': 'fullNameOptions',
		'placeholder': 'First Last'
	})
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
