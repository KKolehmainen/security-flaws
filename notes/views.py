from django.shortcuts import render
from django.http import Http404

from .models import Note
# Create your views here.

def index(request):
    latest_notes = Note.objects.order_by("-pub_date")[:5]
    context = {
        "latest_notes": latest_notes
    }
    return render(request, "notes/index.html", context)

def noteView(request, note_id):
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        raise Http404("Note doest not exist")
    return render(request, "notes/note.html", {"note": note})
