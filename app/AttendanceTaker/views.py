from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .encryption import serverEncrypt, serverDecrypt, encryptAtTime, decryptAtTime, RECIEPT_SALT
from .forms import MakeRoomForm

from .models import Classroom

ATTENDANCE_TAKER_VERSION = "v1.5"

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
			return render(request, "home.html", {"form": form, "submitText": "Create Room", "attendanceTakerVersion": ATTENDANCE_TAKER_VERSION})	#The form has a form.errors which will show on reload

	# if a GET (or any other method) we'll create a blank form
	form = MakeRoomForm()

	return render(request, "home.html", {"form": form, "submitText": "Create Room", "attendanceTakerVersion": ATTENDANCE_TAKER_VERSION})

#This is our homepage

#Reasons
	#[1, otherStudentName, otherId]	Cookies are the same
	#[2, otherStudentName, otherId]	IPs are the same
	#[3]	New cookie created
from .forms import AttendanceForm
def take_attendance(request, base64String):

	NUM_SECONDS_GOOD = 600 #10 minutes
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

	# if a GET (or any other method) we'll create a blank form
	import json
	classList = []
	try:
		classList = classroom.getClassList()
	except ValueError:
		pass	#pray

	form = AttendanceForm(request.POST or None, classListOnly=classroom.classListOnly, classList=classList);

	# if this is a POST request we need to process the form data
	if request.method == "POST":
		#Check that the link is still good
		#Theoretically, if someone could send a POST request, they'd have a ten minute window
		#But if they could write a custom post request in 10 minutes, they deserve to get counted for attendance.
		NUM_SECONDS_GOOD = 600 #10 minutes
		decodedString = decryptAtTime(base64String, NUM_SECONDS_GOOD)
		if(decodedString is None):
			return HttpResponseForbidden("You took too long to fill out the form. Does it really take you 10 minutes to type your name? Try again.")

		# check whether it's valid:
		if form.is_valid():	#Cleans the data too...? SQL Sanitization
			# process the data in form.cleaned_data as required
			# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

			reasons = []

			from ipware import get_client_ip
			ip, is_routable = get_client_ip(request)

			if request.session.get("studentCookie", None) != None:
				print(request.session.get("studentCookie", None));
				try:
					#For each student that has the same cookie, but not the same name.
					for otherStudent in Student.objects.all().filter(id=request.session["studentCookie"]).exclude(fullName=form.cleaned_data["fullName"]):
						reasons.append([1, otherStudent.fullName, str(otherStudent.id)])
				except Student.DoesNotExist:
					pass #Our bad lol

				try:
					#For each student that has the same ip address but not the same name
					for otherStudent in Student.objects.all().filter(ipAddr=ip).exclude(fullName=form.cleaned_data["fullName"]):
						reasons.append([2, otherStudent.fullName, str(otherStudent.id)])
				except Student.DoesNotExist:
					pass #Our bad lol
			else:
				try:
					#For each student that has the same ip address but not the same name
					for otherStudent in Student.objects.all().filter(ipAddr=ip).exclude(fullName=form.cleaned_data["fullName"]):
							reasons.append([2, otherStudent.fullName, str(otherStudent.id)])
				except Student.DoesNotExist:
					pass #Our bad lol
				reasons.append([3])

			student, created = Student.objects.get_or_create(fullName=form.cleaned_data["fullName"],
				defaults={"fullName": form.cleaned_data["fullName"]})

			note = student.attend(classroom, reasons)

			student.ipAddr = ip

			student.save()

			if request.session.get("studentCookie", None) == None:
				request.session["studentCookie"] = str(student.id)

			#request.session["receipt"] = serverDecrypt(serverEncrypt(str(note).encode(), RECIEPT_SALT).decode(), RECIEPT_SALT).decode()
			request.session["receipt"] = serverEncrypt(str(note).encode(), RECIEPT_SALT).decode()

			return HttpResponseRedirect(reverse("done"))

		else:	#The form isn't valid
			#Rerender
			return render(request, "TakeAttendance.html", {"form": form, "submitText": "Take Attendance", "attendanceTakerVersion": ATTENDANCE_TAKER_VERSION})	#The form has a form.errors which will show on reload
	else:
		#Check that the link is still good
		#Theoretically, if someone could send a POST request, they'd have a ten minute window
		#But if they could write a custom post request in 10 minutes, they deserve to get counted for attendance.
		NUM_SECONDS_GOOD = 5 #5 seconds
		decodedString = decryptAtTime(base64String, NUM_SECONDS_GOOD)
		if(decodedString is None):
			return HttpResponseForbidden("Took too long to scan the QR code. Try again")
		return render(request, "TakeAttendance.html", {"form": form, "submitText": "Take Attendance", "attendanceTakerVersion": ATTENDANCE_TAKER_VERSION})

from django.http import HttpResponse
def done(request):
	return render(request, "done.html", {"receipt": request.session.get("receipt", "Your phone probably doesn't like cookies. No reciept for you."), "attendanceTakerVersion": ATTENDANCE_TAKER_VERSION})

def room(request):
	room_code = request.session.get("room_id")

	try:
		obj = Classroom.objects.get(classCode = room_code)
		return render(request, "room.html", { "room_code": room_code, "attendanceTakerVersion": ATTENDANCE_TAKER_VERSION, "message": obj.message})	#Message has a default value.

	except Classroom.DoesNotExist: #it is the Classroom because we search the classrooms in the try block
		return render(request, "room.html", { "room_code": room_code, "attendanceTakerVersion": ATTENDANCE_TAKER_VERSION})


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


from .models import Classroom
class ClassroomAttendanceDetails(APIView):
	def get(self, request):
		room_code = request.session.get("room_id")
		if room_code is None:
			return Response([])

		try:
			obj = Classroom.objects.get(id=room_code)
			#obj["classCode"] = classCode=form.cleaned_data["classCode"]	#Class code is the same anyways

			students = {}

			for attendanceNote in obj.attendanceNotes.all():
				#print("Reasons list: ", attendanceNote.reasons);
				import json
				try:
					students[attendanceNote.studentFullName] = json.loads(attendanceNote.reasons);
				except json.JSONDecodeError:
					return Response({"Error parsing JSON": []})

			return Response(students)

		except Classroom.DoesNotExist: #it is the Classroom because we search the classrooms in the try block
			#This means we're in the clear, and we can create a new classroom.
			newClassroom = form.save()
			request.session["room_id"] = str(newClassroom.id)
			return Response([])

from .models import Classroom
class ClassroomAbsenceList(APIView):
	def get(self, request):
		room_code = request.session.get("room_id")
		if room_code is None:
			return Response([])

		try:
			obj = Classroom.objects.get(id=room_code)
			#obj["classCode"] = classCode=form.cleaned_data["classCode"]	#Class code is the same anyways

			if obj.classList == "":
				return Response([])

			absenceList = obj.getClassList()
			if absenceList is None:
				return Response(["Server error"]) #Shouldn't get here

			for attendanceNote in obj.attendanceNotes.all():
				studentFullName = attendanceNote.studentFullName
				if studentFullName in absenceList:
					absenceList.remove(studentFullName)
			return Response(absenceList)

			return Response([])

		except Classroom.DoesNotExist: #it is the Classroom because we search the classrooms in the try block
			#This means we're in the clear, and we can create a new classroom.
			newClassroom = form.save()
			request.session["room_id"] = str(newClassroom.id)
			return Response([])

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

#Verify a receipt
from .forms import ReceiptForm
def verifyReceipt(request):
	# if this is a POST request we need to process the form data
	if request.method == "POST":
		# create a form instance and populate it with data from the request:
		form = ReceiptForm(request.POST)
		# check whether it's valid:
		if form.is_valid():	#Cleans the data too...? SQL Sanitization
			decrypted = serverDecrypt((form.cleaned_data["receipt"]).strip().encode(), RECIEPT_SALT);
			if(decrypted is None):
				return HttpResponse("It failed to decrypt the receipt. It's probably not geniuine, but maybe if you try it again you'll have better luck.");
			return HttpResponse(decrypted.decode());
		else:	#The form isn't valid. Probably shouldn't get here.
			return render(request, "VerifyReceipt.html", {"form": form, "submitText": "Verify Reciept", "attendanceTakerVersion": ATTENDANCE_TAKER_VERSION})	#The form has a form.errors which will show on reload
	else:
		form = ReceiptForm()
		return render(request, "VerifyReceipt.html", {"form": form, "submitText": "Verify Receipt", "attendanceTakerVersion": ATTENDANCE_TAKER_VERSION})
