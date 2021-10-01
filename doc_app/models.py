from django.db import models
from django.apps import apps
from auth_app.models import *

class Project(models.Model):
    title = models.CharField(max_length=50, null=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    threshold = models.FloatField(null=True)
    report = models.FileField(verbose_name="report" , null=True)
    

    def __str__(self) -> str:
        return self.title

class Document(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self) -> str:
        return self.title

class Result(models.Model):
    document1 = models.ForeignKey(Document,related_name='document1', on_delete=models.SET_NULL,null=True)
    document2 = models.ForeignKey(Document,related_name='document2', on_delete=models.SET_NULL,null=True)
    similarity = models.FloatField(null=True)
    def __str__(self) -> str:
        return self.similarity