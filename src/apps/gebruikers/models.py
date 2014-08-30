from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)

    punten = models.IntegerField()
    #Renners heeft alle id's van de renners, dit i.p.v. 27 losse velden
    renners = models.CharField(max_length=1000)
