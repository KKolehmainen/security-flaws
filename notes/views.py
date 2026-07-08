from django.shortcuts import render
from django.http import HttpResponse

from .models import Note
# Create your views here.

def index(request):
    latest_notes = Note.objects.order_by("-pub_date")[:5]
    context = {
        "latest_notes": latest_notes
    }
    return render(request, "notes/index.html", context)
