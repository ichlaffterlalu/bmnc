from django.db import models
from akun.models import Narasumber

# Create your models here.
class Honor(models.Model):
    id_narasumber = models.ForeignKey(Narasumber, models.DO_NOTHING, db_column='id_narasumber', primary_key=True)
    tgl_diberikan = models.DateTimeField()
    jumlah_berita = models.IntegerField()
    jumlah_gaji = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'honor'
        unique_together = (('id_narasumber', 'tgl_diberikan'),)


class Kupon(models.Model):
    tgl_diberikan = models.DateTimeField()
    tgl_kadaluarsa = models.DateTimeField()
    id_narasumber = models.ForeignKey(Narasumber, models.DO_NOTHING, db_column='id_narasumber')

    class Meta:
        managed = False
        db_table = 'kupon'