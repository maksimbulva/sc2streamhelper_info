from django.db import models

# Create your models here.


class Players(models.Model):
    player_id = models.IntegerField(db_index=True)
    realm = models.IntegerField(db_index=True)
    region_code = models.IntegerField(db_index=True)
    display_name = models.CharField(max_length=32, db_index=True)
    profile_path = models.CharField(max_length=64)


class LaddersByPlayers(models.Model):
    player_id = models.IntegerField(db_index=True)
    realm = models.IntegerField(db_index=True)
    region_code = models.IntegerField(db_index=True)
    ladder_id = models.IntegerField()
