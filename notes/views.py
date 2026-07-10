from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import Note
# Create your views here.

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
    note = get_object_or_404(Note, pk=note_id, owner=request.user)
    return render(request, "notes/note.html", {"note": note})

@csrf_exempt
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
    
def search_notes(query, user_id):
    """This is a dangerous function allowing SQL injections."""
    import sqlite3
    sql = f"SELECT id, title FROM notes_note WHERE title LIKE '%{query}%' AND owner_id={user_id}"
    con = sqlite3.connect("db.sqlite3")
    con.row_factory = sqlite3.Row
    result = con.execute(sql).fetchall()
    con.close()
    return result


@login_required
def searchView(request):
    query = request.GET.get("query")

    # Dangerous:
    results = search_notes(query, request.user.id) if query else []

    # Safe:
    #results = Note.objects.filter(owner=request.user, title__icontains=query) if query else []

    return render(request, "notes/search.html", {"results": results, "query": query})
    