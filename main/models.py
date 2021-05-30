from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Assignments(models.Model):
    assignment1 = models.FileField(upload_to=None,blank=True, editable=True)
    assignment2 = models.FileField(upload_to=None,blank=True, editable=True)
    assignment3 = models.FileField(upload_to=None,blank=True, editable=True)
    assignment4 = models.FileField(upload_to=None,blank=True, editable=True)
    assignment5 = models.FileField(upload_to=None,blank=True, editable=True)
    assignment6 = models.FileField(upload_to=None,blank=True, editable=True)
    assignment7 = models.FileField(upload_to=None,blank=True, editable=True)
    assignment8 = models.FileField(upload_to=None,blank=True, editable=True)

    status_1 = models.BooleanField(default=False)
    status_2 = models.BooleanField(default=False)
    status_3 = models.BooleanField(default=False)
    status_4 = models.BooleanField(default=False)
    status_5 = models.BooleanField(default=False)
    status_6 = models.BooleanField(default=False)
    status_7 = models.BooleanField(default=False)
    status_8 = models.BooleanField(default=False)


    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Assignment_structure(models.Model):
    assn_no = models.IntegerField(primary_key=True,unique=True)
    assn_name = models.CharField(max_length=200)
    assn_description = models.TextField()
    due_date = models.DateTimeField()
    author = models.CharField(max_length=25)


