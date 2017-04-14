from django.db import models

# Create your models here.


class Players(models.Model):
    player_id = models.IntegerField(primary_key=True)
    region_code = models.IntegerField(db_index=True)
    display_name = models.CharField(max_length=32, db_index=True)
    profile_path = models.CharField(max_length=64)
