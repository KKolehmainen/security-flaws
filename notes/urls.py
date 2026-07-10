from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:note_id>/", views.noteView, name="note"),
    path("register/", views.registerView, name="register"),
]