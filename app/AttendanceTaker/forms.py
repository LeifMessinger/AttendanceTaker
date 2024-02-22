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
		'placeholder': 'Enter the room name. Optional'
	})
	classList = forms.CharField(label="Class list - optional", widget=forms.Textarea, required=False)
	classList.widget.attrs.update({
		'placeholder': 'optional\nEnter your list in one of these formats:\n["Json", "string", "array"]\nComma,Separated,Values\nTab\tSeparated\tValues\n\nNewline\nSeparated\nValues'
	})
	message = forms.CharField(label="Room Message", max_length=100, required=False)
	message.widget.attrs.update({
		'placeholder': 'Some text you want to display. Optional'
	})
	classListOnly = forms.BooleanField(label="Only allow names in the class list", required=False)

	def clean_classList(self):
		data = self.cleaned_data['classList']
		if data == "": #Allow data to be blank
			return data
		Classroom.cleanClassList(data)
		return data

	class Meta:
		model = Classroom
		fields = ["classCode", "classList", "classListOnly", "message"]
		widgets = {
			#"classCode": forms.CharField(label="Class code", max_length=30, required=False),
			#"classList": forms.CharField(label="JSON class list", widget=forms.Textarea, required=False)
		}

class AttendanceForm(forms.ModelForm):
	template_name = "TakeAttendanceForm.html"
	#fullName = forms.CharField(label="Full name", max_length=100, required=True)
	thisIsMe = forms.BooleanField(label="That is me", required=True)

	def classListOnly(self, classListOnly, choices):
		#print(classListOnly, choices)
		if classListOnly:
			choices = [(item, item) for item in choices]
			choices.insert(0, (None, "--Please Select Your Name --"))
			self.fields["fullName"].widget = forms.ChoiceField(choices=choices).widget
			self.fields["fullName"].widget.attrs.update({
				'autoComplete': 'on'
			})
		else:
			self.fields['fullName'] = forms.CharField(label="Full name", max_length=100, required=True)
			self.fields['fullName'].widget.attrs.update({
				'autoComplete': 'on',
				'list': 'fullNameOptions',
				'placeholder': 'First Last'
			})
			self.fields['fullName'].options = choices

	def __init__(self, *args, classListOnly=False, classList=[], **kwargs):
		super(AttendanceForm, self).__init__(*args, **kwargs)
		self.classListOnly(classListOnly, classList)

	class Meta:
		model = Student
		fields = ["fullName"]
		widgets = {
			#"classCode": forms.CharField(label="Class code", max_length=30, required=False),
			#"classList": forms.CharField(label="JSON class list", widget=forms.Textarea, required=False)
		}

class ReceiptForm(forms.Form):
	template_name = "ReceiptForm.html"
	receipt = forms.CharField(label="Receipt", help_text="A bunch of jumbled text you got when you took attendance.", widget=forms.Textarea, required=False)
	def clean_receipt(self):
		data = self.cleaned_data['receipt']
		#print("First character:", data[0], "Last character:", data[-1])	#Wow, django .trim()s whitespace
		import re
		if(not bool(re.match('^([\\w=_-])+$', data))):
			raise forms.ValidationError("The pasted text wasn't a url safe base64 string. Try again.")
		else:
			return data
