from django.db import models
from berita.models import Berita

# Create your models here.
class Polling(models.Model):
    id = models.IntegerField(primary_key=True)
    polling_start = models.DateTimeField()
    polling_end = models.DateTimeField()
    total_responden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'polling'


class PollingBerita(models.Model):
    id_polling = models.ForeignKey(Polling, models.DO_NOTHING, db_column='id_polling', primary_key=True)
    url_berita = models.ForeignKey(Berita, models.DO_NOTHING, db_column='url_berita')

    class Meta:
        managed = False
        db_table = 'polling_berita'


class PollingBiasa(models.Model):
    id_polling = models.ForeignKey(Polling, models.DO_NOTHING, db_column='id_polling', primary_key=True)
    url = models.CharField(max_length=50)
    deskripsi = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'polling_biasa'

class Respon(models.Model):
    id_polling = models.ForeignKey(Polling, models.DO_NOTHING, db_column='id_polling', primary_key=True)
    jawaban = models.CharField(max_length=50)
    jumlah_dipilih = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'respon'
        unique_together = (('id_polling', 'jawaban'),)


class Responden(models.Model):
    id_polling = models.ForeignKey(Polling, models.DO_NOTHING, db_column='id_polling', primary_key=True)
    ip_address = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'responden'
        unique_together = (('id_polling', 'ip_address'),)