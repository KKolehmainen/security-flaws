from .models import Note

def search_notes(query, user_id):
    """This is a dangerous function allowing SQL injections."""
    import sqlite3
    sql = f"SELECT id, title FROM notes_note WHERE title LIKE '%{query}%' AND owner_id={user_id}"
    con = sqlite3.connect("db.sqlite3")
    con.row_factory = sqlite3.Row
    result = con.execute(sql).fetchall()
    con.close()
    return result

def search_notes_safe(query, user):
    results = Note.objects.filter(owner=user, title__icontains=query) if query else []
    return results