# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Berita(models.Model):
    url = models.CharField(primary_key=True, max_length=50)
    judul = models.CharField(max_length=100)
    topik = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    jumlah_kata = models.IntegerField()
    rerata_rating = models.FloatField()
    id_universitas = models.ForeignKey('Universitas', models.DO_NOTHING, db_column='id_universitas')

    class Meta:
        managed = False
        db_table = 'berita'


class Dosen(models.Model):
    id_narasumber = models.ForeignKey('Narasumber', models.DO_NOTHING, db_column='id_narasumber', primary_key=True)
    nik_dosen = models.CharField(max_length=20)
    jurusan = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'dosen'


class Honor(models.Model):
    id_narasumber = models.ForeignKey('Narasumber', models.DO_NOTHING, db_column='id_narasumber', primary_key=True)
    tgl_diberikan = models.DateTimeField()
    jumlah_berita = models.IntegerField()
    jumlah_gaji = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'honor'
        unique_together = (('id_narasumber', 'tgl_diberikan'),)


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


class Kupon(models.Model):
    tgl_diberikan = models.DateTimeField()
    tgl_kadaluarsa = models.DateTimeField()
    id_narasumber = models.ForeignKey('Narasumber', models.DO_NOTHING, db_column='id_narasumber')

    class Meta:
        managed = False
        db_table = 'kupon'


class Mahasiswa(models.Model):
    id_narasumber = models.ForeignKey('Narasumber', models.DO_NOTHING, db_column='id_narasumber', primary_key=True)
    npm = models.CharField(max_length=20)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'mahasiswa'


class Narasumber(models.Model):
    id = models.IntegerField(primary_key=True)
    nama = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    tempat = models.CharField(max_length=50)
    tanggal = models.CharField(max_length=50)
    no_hp = models.CharField(max_length=50)
    jumlah_berita = models.IntegerField()
    rerata_kata = models.IntegerField()
    id_universitas = models.ForeignKey('Universitas', models.DO_NOTHING, db_column='id_universitas')

    class Meta:
        managed = False
        db_table = 'narasumber'


class NarasumberBerita(models.Model):
    url_berita = models.ForeignKey(Berita, models.DO_NOTHING, db_column='url_berita', primary_key=True)
    id_narasumber = models.ForeignKey(Narasumber, models.DO_NOTHING, db_column='id_narasumber')

    class Meta:
        managed = False
        db_table = 'narasumber_berita'
        unique_together = (('url_berita', 'id_narasumber'),)


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


class Rating(models.Model):
    url_berita = models.ForeignKey(Berita, models.DO_NOTHING, db_column='url_berita', primary_key=True)
    ip_address = models.CharField(max_length=100)
    nilai = models.FloatField()

    class Meta:
        managed = False
        db_table = 'rating'
        unique_together = (('url_berita', 'ip_address'),)


class Rekening(models.Model):
    nomor = models.CharField(primary_key=True, max_length=20)
    nama_bank = models.CharField(max_length=20)
    id_narasumber = models.ForeignKey(Narasumber, models.DO_NOTHING, db_column='id_narasumber')

    class Meta:
        managed = False
        db_table = 'rekening'


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


class Riwayat(models.Model):
    url_berita = models.ForeignKey(Berita, models.DO_NOTHING, db_column='url_berita', primary_key=True)
    id_riwayat = models.IntegerField()
    waktu_revisi = models.DateTimeField()
    konten = models.TextField()

    class Meta:
        managed = False
        db_table = 'riwayat'
        unique_together = (('url_berita', 'id_riwayat'),)


class Staf(models.Model):
    id_narasumber = models.ForeignKey(Narasumber, models.DO_NOTHING, db_column='id_narasumber', primary_key=True)
    nik_staf = models.CharField(max_length=20)
    posisi = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'staf'


class Tag(models.Model):
    url_berita = models.ForeignKey(Berita, models.DO_NOTHING, db_column='url_berita', primary_key=True)
    tag = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tag'
        unique_together = (('url_berita', 'tag'),)


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
