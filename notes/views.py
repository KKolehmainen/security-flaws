from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .db_v1 import search_notes, search_notes_safe

from .models import Note


def index(request):
    if request.user.is_authenticated:
        latest_notes = Note.objects.filter(owner=request.user).order_by("-pub_date")[:5]
    else:
        latest_notes = None
    context = {
        "latest_notes": latest_notes
    }
    return render(request, "notes/index.html", context)

@login_required
def noteView(request, note_id):

    # FLAW 3: Not checking for note owner 
    note = get_object_or_404(Note, pk=note_id)

    # Fix for FLAW 3: 
    #note = get_object_or_404(Note, pk=note_id, owner=request.user)

    return render(request, "notes/note.html", {"note": note})

# FLAW 2: Allow CSRF, comment decorator to fix
@csrf_exempt
def create_noteView(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        pub_date = timezone.now()

        new_note = Note.objects.create(
            title=title,
            content=content,
            pub_date=pub_date,
            owner=request.user,
        )
        new_note.save()
        return redirect("/notes/")
    
    if request.method == "GET":
        return render(request, "notes/create_note.html")

def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/notes/")
        else:
            messages.error(request, "Wrong username or password")
            return redirect("/notes/login/")
        
    if request.method == "GET":
        return render(request, "notes/login.html")
    
def logoutView(request):
    logout(request)
    return redirect("/notes/")

def registerView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("/notes/register")

        # Fix for FLAW 5:
        #if len(password1) < 1:
        #    messages.error(request, "Password too short")
        #    return redirect("/notes/register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "The username already exists")
            return redirect("/notes/register")

        user = User.objects.create_user(username, password=password1)
        user.save()
        return redirect("/notes/")
    
    if request.method == "GET":
        return render(request, "notes/register.html")

@login_required
def searchView(request):
    query = request.GET.get("query")

    # FLAW 1: Allow SQL injection, see db module for full function
    results = search_notes(query, request.user.id) if query else []

    # Fix for FLAW 1:
    #results = search_notes_safe(query, request.user)

    return render(request, "notes/search.html", {"results": results, "query": query})
    