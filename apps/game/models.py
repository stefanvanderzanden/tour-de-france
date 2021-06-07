from django.db import models


# Create your models here.
class Rider(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey("game.Team", related_name="riders", on_delete=models.PROTECT)


class Team(models.Model):
    name = models.CharField(max_length=100)
