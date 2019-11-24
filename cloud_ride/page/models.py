from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    File = models.FileField(upload_to = "../media/")
    access = models.BooleanField(default = False)
    author = models.ForeignKey(User, on_delete = models.CASCADE)