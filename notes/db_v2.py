from .models import Note

def search_notes(query, user):
    results = Note.objects.filter(owner=user, title__icontains=query) if query else []
    return results