from django import forms
from .models import Classroom
import json

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
		template_name = "MakeRoomForm.html"
		widgets = {
			"template_name": "MakeRoomForm.html",
			#"classCode": forms.CharField(label="Class code", max_length=30, required=False),
			#"classList": forms.CharField(label="JSON class list", widget=forms.Textarea, required=False)
		}

class AttendanceForm(forms.Form):
	template_name = "TakeAttendanceForm.html"
	subject = forms.CharField(label="Your name", max_length=30, required=False)
	thisIsMe = forms.BooleanField(label="That is me", required=True)
