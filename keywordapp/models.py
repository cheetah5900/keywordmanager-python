from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
    
# TempListOfWork
class TempListOfWorkModel(models.Model):
    header = models.CharField(default='',max_length=255)
    date = models.CharField(default='',max_length=255)
    content = models.TextField(default='')
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.header
    
# TempListOfHouse
class TempListOfHouseModel(models.Model):
    header = models.CharField(default='',max_length=255)
    date = models.CharField(default='',max_length=255)
    content = models.TextField(default='')
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.header

