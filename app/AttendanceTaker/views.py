from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import MakeRoomForm

from app_name.models import Classroom

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

			#https://stackoverflow.com/a/65575242/10141528
			try:
				obj = Classroom.objects.get(classCode = form.cleaned_data["classCode"])
				#obj["classCode"] = classCode=form.cleaned_data["classCode"]	#Class code is the same anyways
				if form.cleaned_data["classList"]:
					obj["classList"] = classCode=form.cleaned_data["classList"] #Not form.object.cleaned_data, because we're looking for the form's data
					obj.save()

				request.session["room_id"] = obj["id"]

			except Classroom.DoesNotExist: #it is the Classroom because we search the classrooms in the try block
				#This means we're in the clear, and we can create a new classroom.
				newClassroom = form.save()
				request.session["room_id"] = newClassroom["id"]

			# redirect to a new URL:
			return HttpResponseRedirect(reverse("room")) #, args=[0])) #or , args={key: "value"}))

	# if a GET (or any other method) we'll create a blank form
	form = MakeRoomForm()

	return render(request, "home.html", {"form": form})

def room(request):
	room_code = request.session.get("room_id")
	#get_object_or_404(Classroom, id=room_code) #This definitely won't work first try
	return HttpResponse(str(room_code))
