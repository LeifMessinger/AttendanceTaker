from django.shortcuts import render

def index(request):
	return render(request, "index.html", None)

def bruh(request):
	return render(request, "bruh.html", None)
