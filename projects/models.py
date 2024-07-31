# projects/models.py

from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=50)
    urlInsert = models.TextField(max_length = 200, blank=True)
    whatUrlSays = models.TextField(max_length=200,blank=True)
    image = models.FileField(upload_to="project_images/", blank = True)