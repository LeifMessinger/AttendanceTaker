from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import MakeRoomForm

from .models import Classroom

#This is our homepage
def make_room(request):
	# if this is a POST request we need to process the form data
	if request.method == "POST":
		# create a form instance and populate it with data from the request:
		form = MakeRoomForm(request.POST or None) #This might create empty rooms, but it probably won't because of that request.method == "POST" line
		# check whether it's valid:
		if form.is_valid():	#Cleans the data too...? SQL Sanitization
			# process the data in form.cleaned_data as required
			# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
			if (form.cleaned_data["classCode"] == ""):	#if the class code is left blank
				newClassroom = form.save(commit=False)

				newClassroom.classCode = str(newClassroom.id) #The user isn't using the class code anyways, but it still needs to be unique

				newClassroom.save()

				request.session["room_id"] = str(newClassroom.id)
			else:
				#https://stackoverflow.com/a/65575242/10141528
				try:
					obj = Classroom.objects.get(classCode = form.cleaned_data["classCode"])
					#obj["classCode"] = classCode=form.cleaned_data["classCode"]	#Class code is the same anyways
					if form.cleaned_data["classList"]:
						obj["classList"] = form.cleaned_data["classList"] #Not form.object.cleaned_data, because we're looking for the form's data
						obj.save()

					request.session["room_id"] = str(obj.id)

				except Classroom.DoesNotExist: #it is the Classroom because we search the classrooms in the try block
					#This means we're in the clear, and we can create a new classroom.
					newClassroom = form.save()
					request.session["room_id"] = str(newClassroom.id)

			# redirect to a new URL:
			return HttpResponseRedirect(reverse("room")) #, args=[0])) #or , args={key: "value"}))
		else:	#The form isn't valid
			#Render the page again
			return render(request, "home.html", {"form": form})	#The form has a form.errors which will show on reload

	# if a GET (or any other method) we'll create a blank form
	form = MakeRoomForm()

	return render(request, "home.html", {"form": form})


# Import the required modules
from django.conf import settings
def room(request):
	room_code = request.session.get("room_id")
	#get_object_or_404(Classroom, id=room_code) #This definitely won't work first try

	text = room_code

	from cryptography.fernet import Fernet
	fernet = Fernet(settings.FERNET_KEY)

	# Define a string to encrypt and decrypt
	message = b"Hello, world!"

	# Encrypt the message
	encrypted = fernet.encrypt(message)
	text += "\n" + "Encrypted: " + encrypted.decode()

	# Decrypt the message
	decrypted = fernet.decrypt(encrypted)
	text += "\n" + "Decrypted: " + decrypted.decode()

	return HttpResponse(text)
