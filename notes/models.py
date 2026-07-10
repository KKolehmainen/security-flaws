from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    pub_date = models.DateTimeField("date published")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + "\n" + self.content