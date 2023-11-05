from django.db import models

# Create your models here.

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)
    subject = models.CharField(max_length=100)
    issue = models.CharField(max_length=300)

    class Meta:
        db_table = 'ticket'