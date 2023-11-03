from django.db import models
from datetime import datetime
import os

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s-%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

class LostItemDetails(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=30) # null=True means optional
    category = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    location_lost = models.CharField(max_length=100, blank=True)
    datetime = models.DateTimeField(blank=True)
    item_image = models.ImageField(upload_to=filepath, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'lost_item'

class FoundItemDetails(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    location_found = models.CharField(max_length=100, blank=True)
    datetime = models.DateTimeField(blank=True)
    item_image = models.ImageField(upload_to=filepath, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'found_item'
