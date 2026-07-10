from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import Note
# Create your views here.

def index(request):
    latest_notes = Note.objects.order_by("-pub_date")[:5]
    context = {
        "latest_notes": latest_notes
    }
    return render(request, "notes/index.html", context)

def noteView(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, "notes/note.html", {"note": note})

@csrf_exempt
def registerView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("/notes/register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "The username already exists")
            return redirect("/notes/register")

        user = User.objects.create_user(username, password=password1)
        user.save()
        return redirect("/notes/")
    
    if request.method == "GET":
        return render(request, "notes/register.html")
    