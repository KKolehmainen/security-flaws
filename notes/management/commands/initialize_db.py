from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from notes.models import Note


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing database with users and data...")

        # Create user with unsafe password (FLAW 4)
        bob = User.objects.create(username="bob", password="squarepants")

        # Create user with hashed password (after FLAW 4 is fixed)
        #bob = User.objects.create_user(username="bob", password="squarepants")

        # Create user with unsafe password (FLAW 4)
        alice = User.objects.create(username="alice", password="redqueen")

        # Create user with hashed password (after FLAW 4 is fixed)
        #alice = User.objects.create_user(username="alice", password="redqueen")

        Note.objects.create(
            title="Bob's note",
            content = "Bob wrote this.",
            pub_date = timezone.now(),
            owner = bob
        )

        Note.objects.create(
            title="Alices's note",
            content = "Alice wrote this.",
            pub_date = timezone.now(),
            owner = alice
        )
        
