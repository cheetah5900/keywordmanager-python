from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import datetime
    
     
# TempLinkOfWorkModel
class TempLinkOfWorkModel(models.Model):
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.link
    
# TempLinkOfHouseModel
class TempLinkOfHouseModel(models.Model):
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.link
    
# ListOfWork
class ListOfWorkModel(models.Model):
    header = models.CharField(default='',max_length=255)
    date = models.DateTimeField(default=datetime.now, blank=True)
    content = models.TextField(default='')
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.header
   
    
# ListOfHouse
class ListOfHouseModel(models.Model):
    header = models.CharField(default='',max_length=255)
    date = models.DateTimeField(default=datetime.now, blank=True)
    content = models.TextField(default='')
    link = models.CharField(default='',max_length=255)

    def __str__(self):
        return self.header

