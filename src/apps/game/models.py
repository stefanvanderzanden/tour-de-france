from django.db import models

class Renner(models.Model):
    naam = models.CharField(max_length=100)
    nummer = models.IntegerField()
    team = models.ForeignKey('Team', related_name='renner_team')

    def __unicode__(self):
        return '%d %s'% (self.nummer, self.naam)
    

class Team(models.Model):
    naam = models.CharField(max_length=100)

    def __unicode__(self):
        return self.naam
    
class Etappe(models.Model):
    nummer = models.IntegerField()
    start = models.CharField(max_length=100)
    einde = models.CharField(max_length=100)

    def __unicode__(self):
        return 'Etappe %d' % (self.nummer)
