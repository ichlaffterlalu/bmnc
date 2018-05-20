from django.db import models
from akun.models import Narasumber, Universitas

# Create your models here.
class Berita(models.Model):
    url = models.CharField(primary_key=True, max_length=50)
    judul = models.CharField(max_length=100)
    topik = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    jumlah_kata = models.IntegerField()
    rerata_rating = models.FloatField()
    id_universitas = models.ForeignKey(Universitas, models.DO_NOTHING, db_column='id_universitas')

    class Meta:
        managed = False
        db_table = 'berita'

class Komentar(models.Model):
    id = models.IntegerField(primary_key=True)
    tanggal = models.DateTimeField()
    jam = models.TimeField()
    konten = models.CharField(max_length=100)
    nama_user = models.CharField(max_length=50)
    email_user = models.CharField(max_length=50)
    url_user = models.CharField(max_length=50)
    url_berita = models.ForeignKey(Berita, models.DO_NOTHING, db_column='url_berita')

    class Meta:
        managed = False
        db_table = 'komentar'

class NarasumberBerita(models.Model):
    url_berita = models.ForeignKey(Berita, models.DO_NOTHING, db_column='url_berita', primary_key=True)
    id_narasumber = models.ForeignKey(Narasumber, models.DO_NOTHING, db_column='id_narasumber')

    class Meta:
        managed = False
        db_table = 'narasumber_berita'
        unique_together = (('url_berita', 'id_narasumber'),)

class Rating(models.Model):
    url_berita = models.ForeignKey(Berita, models.DO_NOTHING, db_column='url_berita', primary_key=True)
    ip_address = models.CharField(max_length=100)
    nilai = models.FloatField()

    class Meta:
        managed = False
        db_table = 'rating'
        unique_together = (('url_berita', 'ip_address'),)

class Riwayat(models.Model):
    url_berita = models.ForeignKey(Berita, models.DO_NOTHING, db_column='url_berita', primary_key=True)
    id_riwayat = models.IntegerField()
    waktu_revisi = models.DateTimeField()
    konten = models.TextField()

    class Meta:
        managed = False
        db_table = 'riwayat'
        unique_together = (('url_berita', 'id_riwayat'),)

class Tag(models.Model):
    url_berita = models.ForeignKey(Berita, models.DO_NOTHING, db_column='url_berita', primary_key=True)
    tag = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tag'
        unique_together = (('url_berita', 'tag'),)