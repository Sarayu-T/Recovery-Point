from django.db import models

# Create your models here.

class users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=10, unique= True)

    class Meta:
        managed = False
        db_table = "users"
