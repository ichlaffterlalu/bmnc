from django.db import models

# Create your models here.
class Universitas(models.Model):
    id = models.IntegerField(primary_key=True)
    jalan = models.CharField(max_length=100)
    kelurahan = models.CharField(max_length=50)
    provinsi = models.CharField(max_length=50)
    kodepos = models.CharField(max_length=10)
    website = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'universitas'

class Narasumber(models.Model):
    id = models.IntegerField(primary_key=True)
    nama = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    tempat = models.CharField(max_length=50)
    tanggal = models.CharField(max_length=50)
    no_hp = models.CharField(max_length=50)
    jumlah_berita = models.IntegerField()
    rerata_kata = models.IntegerField()
    id_universitas = models.ForeignKey(Universitas, models.DO_NOTHING, db_column='id_universitas')

    class Meta:
        managed = False
        db_table = 'narasumber'

class Dosen(models.Model):
    id_narasumber = models.ForeignKey(Narasumber, models.DO_NOTHING, db_column='id_narasumber', primary_key=True)
    nik_dosen = models.CharField(max_length=20)
    jurusan = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'dosen'

class Mahasiswa(models.Model):
    id_narasumber = models.ForeignKey(Narasumber, models.DO_NOTHING, db_column='id_narasumber', primary_key=True)
    npm = models.CharField(max_length=20)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'mahasiswa'

class Rekening(models.Model):
    nomor = models.CharField(primary_key=True, max_length=20)
    nama_bank = models.CharField(max_length=20)
    id_narasumber = models.ForeignKey(Narasumber, models.DO_NOTHING, db_column='id_narasumber')

    class Meta:
        managed = False
        db_table = 'rekening'

class Staf(models.Model):
    id_narasumber = models.ForeignKey(Narasumber, models.DO_NOTHING, db_column='id_narasumber', primary_key=True)
    nik_staf = models.CharField(max_length=20)
    posisi = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'staf'
