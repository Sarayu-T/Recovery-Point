from django.db import models

# Create your models here.
class Item(models.Model):
  item_name = models.CharFields(max_length=255)
  description = models.TextField()
  location_lost = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)
