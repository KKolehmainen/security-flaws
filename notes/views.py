from django.shortcuts import render, get_object_or_404

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
