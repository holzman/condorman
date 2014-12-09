from django.db import models
from datetime import datetime
from reversion.helpers import patch_admin


# Create your models here.
class CondorUser(models.Model):
    def __unicode__(self):
        return self.username
    class Meta:
        ordering = ['username']
    username = models.CharField(max_length=255, unique=True)
    isAdmin = models.BooleanField()

class PrioFactor(models.Model):
    def __unicode__(self):
        return "%s" % self.factor
    
    user = models.ForeignKey(CondorUser)
    factor = models.FloatField(max_length=200)
    start_date = models.DateTimeField('Start Date')
    end_date = models.DateTimeField('End Date')

    def expired(self):
        return (datetime.now() > self.end_date)

class LogAction(models.Model):
    def __unicode__(self):
        return '%s, %s, %s' % (self.action_date, self.authuser, self.action)

    authuser = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    action_date = models.DateTimeField('Action Date')
    

