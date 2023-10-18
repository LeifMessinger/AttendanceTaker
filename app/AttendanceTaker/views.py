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
			return render(request, "home.html", {"form": form, "submitText": "Create Room"})	#The form has a form.errors which will show on reload

	# if a GET (or any other method) we'll create a blank form
	form = MakeRoomForm()

	return render(request, "home.html", {"form": form, "submitText": "Create Room"})

#Takes a binary string, returns a binary string, which means you probably gotta .encode() it
def encryptAtTime(binaryString):
	from django.conf import settings
	from cryptography.fernet import Fernet
	fernet = Fernet(settings.FERNET_KEY)

	import time
	urlSafeB64String = fernet.encrypt_at_time(binaryString, int(time.time()))

	return encryptedString

#Takes a binary string, returns a binary string, which means you probably gotta .encode() it
#Returns None if it is a bad key
def decryptAtTime(binaryString, numSecondsGood=1000000):
	from django.conf import settings
	from cryptography.fernet import Fernet
	fernet = Fernet(settings.FERNET_KEY)

	import time
	import cryptography
	try:
		return fernet.decrypt_at_time(binaryString, numSecondsGood, int(time.time()))
	except cryptography.fernet.InvalidToken:
		return None
#Maybe do it without the time later

def testEncryption(request):
	#Encrypt a string
	urlSafeB64String = encryptAtTime(b"Bruhh")
	text += "\n" + "Encoded: " + urlSafeB64String.decode()

	#Decrypt a string
	try:
		decodedString = decryptAtTime(urlSafeB64String, NUM_SECONDS_GOOD)
		text += "\n" + "Decoded: " + decodedString.decode()
	except cryptography.fernet.InvalidToken:
		text += "\n" + "Decoded: " + "TOOK TOO LONG BUDDY BOYYY"

	return HttpResponse(text)

#This is our homepage
from .forms import AttendanceForm
def take_attendance(request, base64String):

	# if this is a POST request we need to process the form data
	if request.method == "POST":
		# create a form instance and populate it with data from the request:
		form = AttendanceForm(request.POST or None) #This might create empty rooms, but it probably won't because of that request.method == "POST" line
		# check whether it's valid:
		if form.is_valid():	#Cleans the data too...? SQL Sanitization
			# process the data in form.cleaned_data as required
			# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

			# if a GET (or any other method) we'll create a blank form
			#Check that the link is still good
			import cryptography #for the error to catch
			NUM_SECONDS_GOOD = 600 #10 minutes
			#Theoretically, if someone could send a POST request, they'd have a ten minute window
			#But if they could write a custom post request in 10 minutes, they deserve to get counted for attendance.

			decodedString = decryptAtTime(base64String, NUM_SECONDS_GOOD)
			if(decodedString is None):
				return HttpResponseForbidden("You took too long to fill out the form. Does it really take you 10 minutes to type your name? Try again.")

			#The link is good
			#Check that the classroom exists
			try:
				classroom = Classroom.objects.get(id = decodedString.decode())
				#The classroom exists


			except Classroom.DoesNotExist: #it is the Classroom because we search the classrooms in the try block
				from django.http import HttpResponseNotFound
				return HttpResponseNotFound("We couldn't find the classroom in our database.")

			student, created = Student.objects.get_or_create(fullName=form.cleaned_data["fullName"],
				defaults={"fullName": form.cleaned_data["fullName"]})

			student.attend(classroom)

			from ipware import get_client_ip
			ip, is_routable = get_client_ip(request)
			student.ipAddr = ip

			student.save()

			# redirect to a new URL:
			return HttpResponseRedirect(reverse("done")) #, args=[0])) #or , args={key: "value"}))

		else:	#The form isn't valid
			#Render the page again

			# if a GET (or any other method) we'll create a blank form
			#Check that the link is still good
			import cryptography #for the error to catch
			NUM_SECONDS_GOOD = 600 #10 minutes

			decodedString = decryptAtTime(base64String, NUM_SECONDS_GOOD)
			if(decodedString is None):
				return HttpResponseForbidden("You somehow messed up the form, and it took 10 minutes, which is too long. Try again.")

			return render(request, "home.html", {"form": form, "submitText": "Take Attendance"})	#The form has a form.errors which will show on reload
	else:
		# if a GET (or any other method) we'll create a blank form
		#Check that the link is still good
		import cryptography #for the error to catch
		NUM_SECONDS_GOOD = 10

		decodedString = decryptAtTime(base64String, NUM_SECONDS_GOOD)
		if(decodedString is None):
			return HttpResponseForbidden("You took too long to scan the QR code, or the QR code messed up when you scanned it. Try again.")

		form = AttendanceForm()

		return render(request, "home.html", {"form": form, "submitText": "Take Attendance"})

from django.http import HttpResponse
def done(request):
	return HttpResponse("You have taken your own attendance!")

def room(request):
	room_code = request.session.get("room_id")
	return render(request, "room.html", { "room_code": room_code })


# API stuff

from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
class ClassroomQRCode(APIView):
	def get(self, request):
		room_code = request.session.get("room_id")
		if room_code == None:
			return HttpResponseRedirect(reverse("home"))
		#get_object_or_404(Classroom, id=room_code) #This definitely won't work first try

		text = room_code

		from cryptography.fernet import Fernet
		fernet = Fernet(settings.FERNET_KEY)

		import time
		urlSafeB64String = fernet.encrypt_at_time(text.encode(), int(time.time()))

		return Response(urlSafeB64String.decode())

from .models import Classroom
class ClassroomAttendanceList(APIView):
	def get(self, request):
		room_code = request.session.get("room_id")
		if room_code is None:
			return Response([])

		try:
			obj = Classroom.objects.get(id=room_code)
			#obj["classCode"] = classCode=form.cleaned_data["classCode"]	#Class code is the same anyways

			students = []

			for attendanceNote in obj.attendanceNotes.all():
				students.append(attendanceNote.studentFullName)

			return Response(students)

		except Classroom.DoesNotExist: #it is the Classroom because we search the classrooms in the try block
			#This means we're in the clear, and we can create a new classroom.
			newClassroom = form.save()
			request.session["room_id"] = str(newClassroom.id)

from .models import AttendanceNote, Student, Classroom
from .serializers import AttendanceNoteSerializer, StudentSerializer, ClassroomSerializer
from rest_framework import viewsets

class AttendanceNoteViewSet(viewsets.ModelViewSet):
	queryset = AttendanceNote.objects.all()
	serializer_class = AttendanceNoteSerializer

class StudentViewSet(viewsets.ModelViewSet):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer

class ClassroomViewSet(viewsets.ModelViewSet):
	queryset = Classroom.objects.all()
	serializer_class = ClassroomSerializer

def debugView(request):
	raise Exception("Lol")
