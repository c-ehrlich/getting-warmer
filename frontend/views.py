from django.shortcuts import render


def index(request):
    if request.method == "GET":
        context = {}
        return render(request, "frontend/index.html", context)

def json(request):
    if request.method == "GET":
        context = {}
        return render(request, "frontend/json.html")